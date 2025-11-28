"""
Simple FastAPI Webhook Server
Receives callbacks from Pixpoc and processes them
"""

from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os
from pathlib import Path
from loguru import logger

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.pixpoc_client import PixpocClient
from services.agent_service import AgentService
from services.report_service import ReportService
from database.db import update_call_status, save_report, update_financial_data, get_call_by_tracking_id, get_call_by_id
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="FinanceBot Webhook Server")


class PixpocCallback(BaseModel):
    """
    Pixpoc callback payload.
    Pixpoc may send either callId or callSid (tracking_id).
    """
    callId: Optional[str] = None  # UUID call ID
    callSid: Optional[str] = None  # Tracking ID (this is what Pixpoc typically sends)
    trackingId: Optional[str] = None  # Alternative field name
    contactId: Optional[str] = None
    status: str
    duration: Optional[int] = None


async def process_completed_call(call_id: str, contact_id: str, phone_number: str):
    """
    Background task to process completed call.
    
    1. Fetch Pixpoc data (using tracking_id/call_id)
    2. Run AI agent
    3. Generate PDF
    4. Save to database
    
    Args:
        call_id: Pixpoc call UUID or tracking ID
        contact_id: Pixpoc contact ID
        phone_number: User's phone number (from database lookup)
    """
    try:
        logger.info(f"Processing call: {call_id} for {phone_number}")
        
        # Initialize services
        pixpoc_client = PixpocClient(
            base_url=os.getenv("PIXPOC_API_BASE_URL"),
            api_key=os.getenv("PIXPOC_API_KEY")
        )
        
        agent_service = AgentService()
        report_service = ReportService(storage_path=os.getenv("REPORTS_PATH", "./reports"))
        
        # Fetch all Pixpoc data using the call_id (tracking_id works too)
        logger.info(f"Fetching Pixpoc data for call {call_id}...")
        pixpoc_data = await pixpoc_client.get_full_call_data(call_id)
        
        # Determine agent type
        agent_type = "financial_planning"  # Default
        summary = pixpoc_data.get("analysis", {}).get("metadata", {}).get("summary", "").lower()
        if "tax" in summary:
            agent_type = "tax_planning"
        
        logger.info(f"Running {agent_type} agent...")
        
        # Run agent
        markdown_report = await agent_service.process_call_and_generate_report(
            pixpoc_data=pixpoc_data,
            agent_type=agent_type
        )
        
        # Generate PDF
        logger.info("Generating PDF...")
        report_metadata = await report_service.save_report(
            phone_number=phone_number,
            report_content=markdown_report,
            report_type=agent_type,
            call_id=call_id
        )
        
        # Update database
        logger.info("Updating database...")
        update_call_status(call_id, "completed")
        
        save_report(
            phone_number=phone_number,
            report_id=report_metadata['id'],
            call_id=call_id,
            report_type=agent_type,
            filename=report_metadata['pdf_filename'],
            file_path=report_metadata['pdf_path']
        )
        
        # Extract and save financial data
        memory = pixpoc_data.get("memory", {})
        financials = memory.get("financials", {})
        income_data = financials.get("income", {})
        expense_data = financials.get("expenses", {})
        
        monthly_income = income_data.get("monthly_salary", 0)
        monthly_expenses = expense_data.get("monthly_fixed", 0) + expense_data.get("monthly_variable", 0)
        savings = monthly_income - monthly_expenses
        
        update_financial_data(
            phone_number=phone_number,
            income=monthly_income,
            savings=savings,
            expenses=monthly_expenses,
            data_dict=memory
        )
        
        logger.info(f"✅ Call processing completed: {call_id}")
        
    except Exception as e:
        logger.error(f"❌ Failed to process call {call_id}: {e}")
        update_call_status(call_id, "failed")


@app.post("/webhook/pixpoc")
async def pixpoc_webhook(payload: PixpocCallback, background_tasks: BackgroundTasks):
    """
    Receive Pixpoc callbacks.
    Pixpoc sends tracking_id (callSid) in callbacks, not the UUID call_id.
    We need to look up the call in our database to get the full details.
    """
    logger.info("="*70)
    logger.info("📞 RECEIVED PIXPOC WEBHOOK CALLBACK")
    logger.info("="*70)
    logger.info(f"Full Payload: {payload.dict()}")
    logger.info(f"Call ID: {payload.callId}")
    logger.info(f"Call SID: {payload.callSid}")
    logger.info(f"Tracking ID: {payload.trackingId}")
    logger.info(f"Contact ID: {payload.contactId}")
    logger.info(f"Status: {payload.status}")
    logger.info(f"Duration: {payload.duration}")
    logger.info("="*70)
    
    if payload.status != "COMPLETED":
        logger.warning(f"Call not completed: {payload.status}")
        update_call_status(payload.callId or payload.callSid or payload.trackingId, payload.status)
        return {"success": True, "message": f"Call status: {payload.status}"}
    
    # Extract the identifier (could be callId, callSid, or trackingId)
    tracking_id = payload.callSid or payload.trackingId
    call_uuid = payload.callId
    contact_id = payload.contactId
    
    logger.info(f"Looking up call - UUID: {call_uuid}, Tracking: {tracking_id}")
    
    # Try to find the call in database using tracking_id or call_id
    call_data = None
    
    if tracking_id:
        call_data = get_call_by_tracking_id(tracking_id)
        logger.info(f"Lookup by tracking_id ({tracking_id}): {call_data is not None}")
    
    if not call_data and call_uuid:
        call_data = get_call_by_id(call_uuid)
        logger.info(f"Lookup by call_id ({call_uuid}): {call_data is not None}")
    
    if not call_data:
        logger.error(f"❌ Call not found in database! Tracking: {tracking_id}, UUID: {call_uuid}")
        return {
            "success": False,
            "error": "Call not found in database",
            "tracking_id": tracking_id,
            "call_id": call_uuid
        }
    
    phone_number = call_data['phone_number']
    actual_call_id = call_data['call_id']  # Use the UUID from database
    actual_contact_id = contact_id or call_data['contact_id']
    
    logger.info(f"✅ Call found: {actual_call_id} for {phone_number}")
    
    # Process in background with correct IDs
    background_tasks.add_task(
        process_completed_call,
        call_id=actual_call_id,
        contact_id=actual_contact_id,
        phone_number=phone_number
    )
    
    return {
        "success": True,
        "message": "Processing started",
        "callId": actual_call_id,
        "trackingId": tracking_id,
        "phoneNumber": phone_number
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy", "service": "financebot-webhook"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "FinanceBot Webhook Server",
        "version": "1.0.0",
        "endpoints": {
            "webhook": "/webhook/pixpoc",
            "health": "/health"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("WEBHOOK_HOST", "0.0.0.0"),
        port=int(os.getenv("WEBHOOK_PORT", 8000))
    )

