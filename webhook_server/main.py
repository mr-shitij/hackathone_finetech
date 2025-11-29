"""
Simple FastAPI Webhook Server
Receives callbacks from Pixpoc and processes them
"""

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

# Add CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalysisData(BaseModel):
    """Analysis data from Pixpoc"""
    status: str
    metadata: Optional[dict] = None
    rawResponse: Optional[str] = None


class PixpocCallback(BaseModel):
    """
    Pixpoc callback payload - actual format from their system.
    
    This is sent when analysis completes after a call.
    """
    event: str  # 'analysis_completed'
    callSid: str  # Tracking ID from telephony provider
    callId: str  # Call UUID
    callType: str  # 'inbound' | 'outbound'
    status: str  # 'success' | 'failed' | 'disabled' | 'no_transcript'
    analysis: Optional[AnalysisData] = None
    error: Optional[str] = None
    timestamp: str  # ISO timestamp


async def process_completed_call(
    call_id: str, 
    contact_id: str, 
    phone_number: str,
    analysis_data: Optional[dict] = None
):
    """
    Background task to process completed call.
    
    1. Pass analysis data directly to AI agent
    2. Generate report using AI agent
    3. Generate PDF and save
    
    Args:
        call_id: Pixpoc call UUID
        contact_id: Pixpoc contact ID
        phone_number: User's phone number
        analysis_data: Analysis data from webhook callback
    """
    try:
        logger.info(f"Processing call: {call_id} for {phone_number}")
        
        # Initialize services
        agent_service = AgentService()
        
        # Use absolute path for reports to ensure they're in the project root
        reports_path = os.getenv("REPORTS_PATH", "./reports")
        if not os.path.isabs(reports_path):
            # Convert relative path to absolute from project root
            project_root = Path(__file__).parent.parent
            reports_path = project_root / reports_path
        
        report_service = ReportService(storage_path=str(reports_path))
        
        # Pass analysis data directly to agent
        if not analysis_data:
            logger.error("No analysis data provided")
            raise ValueError("Analysis data is required")
        
        logger.info(f"Analysis data received: {list(analysis_data.keys())}")
        
        # Use comprehensive planning (financial + tax)
        agent_type = "comprehensive_planning"
        logger.info(f"Running {agent_type} agent...")
        
        # Run agent with analysis data
        markdown_report = await agent_service.process_call_and_generate_report(
            pixpoc_data=analysis_data,
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
        
        # Update database - only store report info
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
        
        logger.info(f"✅ Call processing completed: {call_id}")
        
    except Exception as e:
        logger.error(f"❌ Failed to process call {call_id}: {e}")
        update_call_status(call_id, "failed")


@app.post("/webhook/pixpoc")
async def pixpoc_webhook(payload: PixpocCallback, background_tasks: BackgroundTasks):
    """
    Receive Pixpoc callbacks when analysis completes.
    
    Payload format:
    {
      "event": "analysis_completed",
      "callSid": "call-tracking-id",
      "callId": "uuid",
      "callType": "outbound",
      "status": "success",
      "analysis": {
        "status": "COMPLETED",
        "metadata": {...},
        "rawResponse": "..."
      },
      "timestamp": "2024-01-01T12:00:00Z"
    }
    """
    logger.info("="*70)
    logger.info("📞 RECEIVED PIXPOC WEBHOOK CALLBACK")
    logger.info("="*70)
    logger.info(f"Event: {payload.event}")
    logger.info(f"Call ID: {payload.callId}")
    logger.info(f"Call SID: {payload.callSid}")
    logger.info(f"Call Type: {payload.callType}")
    logger.info(f"Status: {payload.status}")
    logger.info(f"Timestamp: {payload.timestamp}")
    
    if payload.analysis:
        logger.info(f"Analysis Status: {payload.analysis.status}")
        logger.info(f"Analysis Metadata: {payload.analysis.metadata}")
    
    if payload.error:
        logger.error(f"Error: {payload.error}")
    
    logger.info(f"Full Payload: {payload.dict()}")
    logger.info("="*70)
    
    # Check if analysis was successful
    if payload.status != "success":
        logger.warning(f"Analysis not successful: {payload.status}")
        if payload.error:
            logger.error(f"Error: {payload.error}")
        
        # Update call status
        update_call_status(payload.callId, f"analysis_{payload.status}")
        
        return {
            "success": True, 
            "message": f"Analysis status: {payload.status}",
            "error": payload.error
        }
    
    # Look up call in database using tracking_id (callSid) or call_id
    call_data = None
    
    # Try tracking_id first (most reliable)
    if payload.callSid:
        call_data = get_call_by_tracking_id(payload.callSid)
        logger.info(f"Lookup by callSid ({payload.callSid}): {call_data is not None}")
    
    # Fallback to call_id
    if not call_data and payload.callId:
        call_data = get_call_by_id(payload.callId)
        logger.info(f"Lookup by callId ({payload.callId}): {call_data is not None}")
    
    if not call_data:
        logger.error(f"❌ Call not found in database! SID: {payload.callSid}, ID: {payload.callId}")
        return {
            "success": False,
            "error": "Call not found in database",
            "callSid": payload.callSid,
            "callId": payload.callId
        }
    
    phone_number = call_data['phone_number']
    actual_call_id = call_data['call_id']
    contact_id = call_data['contact_id']
    
    logger.info(f"✅ Call found: {actual_call_id} for {phone_number}")
    logger.info(f"📊 Starting background processing...")
    
    # Process in background
    background_tasks.add_task(
        process_completed_call,
        call_id=actual_call_id,
        contact_id=contact_id,
        phone_number=phone_number,
        analysis_data=payload.analysis.dict() if payload.analysis else None
    )
    
    return {
        "success": True,
        "message": "Processing started",
        "callId": actual_call_id,
        "callSid": payload.callSid,
        "phoneNumber": phone_number
    }


class SaveCallRequest(BaseModel):
    """Request model for saving call details"""
    phone: str
    call_id: str
    contact_id: Optional[str] = None
    tracking_id: Optional[str] = None
    campaign_id: Optional[str] = None


@app.post("/api/calls/save")
async def save_call(request: SaveCallRequest):
    """
    Save call details to database after initiating via frontend.
    Called by Next.js after Pixpoc call is initiated.
    """
    try:
        logger.info(f"Saving call to database: {request.call_id} for {request.phone}")
        
        db_save_call(
            phone_number=request.phone,
            call_id=request.call_id,
            contact_id=request.contact_id,
            tracking_id=request.tracking_id,
            campaign_id=request.campaign_id
        )
        
        return {
            "success": True,
            "message": "Call saved successfully",
            "call_id": request.call_id
        }
        
    except Exception as e:
        logger.error(f"Error saving call: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error saving call: {str(e)}"
        )


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

