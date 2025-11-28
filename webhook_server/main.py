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
from database.db import update_call_status, save_report, update_financial_data
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="FinanceBot Webhook Server")


class PixpocCallback(BaseModel):
    """Pixpoc callback payload"""
    callId: str
    callSid: Optional[str] = None
    contactId: str
    status: str
    duration: Optional[int] = None


async def process_completed_call(call_id: str, contact_id: str):
    """
    Background task to process completed call.
    
    1. Fetch Pixpoc data
    2. Run AI agent
    3. Generate PDF
    4. Save to database
    """
    try:
        logger.info(f"Processing call: {call_id}")
        
        # Initialize services
        pixpoc_client = PixpocClient(
            base_url=os.getenv("PIXPOC_API_BASE_URL"),
            api_key=os.getenv("PIXPOC_API_KEY")
        )
        
        agent_service = AgentService()
        report_service = ReportService(storage_path=os.getenv("REPORTS_PATH", "./reports"))
        
        # Fetch all Pixpoc data
        logger.info("Fetching Pixpoc data...")
        pixpoc_data = await pixpoc_client.get_full_call_data(call_id, contact_id)
        
        phone_number = pixpoc_data.get("metadata", {}).get("phoneNumber", "unknown")
        
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
    Receive Pixpoc callbacks
    """
    logger.info(f"Received webhook: {payload.dict()}")
    
    if payload.status != "COMPLETED":
        logger.warning(f"Call not completed: {payload.status}")
        return {"success": True, "message": "Call not completed"}
    
    # Process in background
    background_tasks.add_task(
        process_completed_call,
        call_id=payload.callId,
        contact_id=payload.contactId
    )
    
    return {
        "success": True,
        "message": "Processing started",
        "callId": payload.callId
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

