"""
Pixpoc.ai API Client
Handles all interactions with Pixpoc Call Manager platform

API Reference: https://app.pixpoc.ai
"""

import httpx
import asyncio
from typing import Dict, Any, Optional
from loguru import logger


class PixpocClient:
    """Client for Pixpoc.ai Call Manager API integration"""
    
    def __init__(self, base_url: str = "https://app.pixpoc.ai", api_key: str = ""):
        """
        Initialize Pixpoc client.
        
        Args:
            base_url: Pixpoc API base URL (default: https://app.pixpoc.ai)
            api_key: API key for authentication (X-API-Key header)
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
    
    def initiate_call_sync(
        self, 
        phone_number: str, 
        agent_id: str,
        contact_name: Optional[str] = None,
        contact_data: Optional[Dict[str, Any]] = None,
        from_number_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Initiate a single outbound call (synchronous for Streamlit).
        
        Endpoint: POST /api/v1/calls
        
        Args:
            phone_number: Phone number in E.164 format (e.g., +1234567890)
            agent_id: UUID of the AI agent to use
            contact_name: Name of the contact (for personalization)
            contact_data: Additional contact data as key-value pairs
            from_number_id: Optional specific from number UUID to use
            
        Returns:
            Response with call, contact, and campaign details
        """
        try:
            import requests
            
            # Ensure phone number is in E.164 format
            if not phone_number.startswith('+'):
                # Assume Indian number if no country code
                phone_number = f"+91{phone_number.lstrip('0')}"
            
            url = f"{self.base_url}/api/v1/calls"
            
            payload = {
                "toNumber": phone_number,
                "agentId": agent_id,
            }
            
            if contact_name:
                payload["contactName"] = contact_name
            if contact_data:
                payload["contactData"] = contact_data
            if from_number_id:
                payload["fromNumberId"] = from_number_id
            
            logger.info(f"Initiating call to {phone_number} with agent {agent_id}")
            
            response = requests.post(
                url, 
                json=payload, 
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    logger.info(f"Call initiated successfully: {result['data']['call']['id']}")
                    return result["data"]
                else:
                    error_msg = f"API returned success=false: {result.get('message')}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
            else:
                error_msg = f"Failed to initiate call: HTTP {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error initiating call: {e}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Error initiating call: {e}"
            logger.error(error_msg)
            raise
    async def get_call_details(self, call_id: str) -> Dict[str, Any]:
        """
        Get details of a specific call.
        
        Endpoint: GET /api/v1/calls/{callId}
        
        Args:
            call_id: Call UUID or callSid
            
        Returns:
            Full call details including status, duration, transcript
        """
        url = f"{self.base_url}/api/v1/calls/{call_id}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                if data.get("success"):
                    logger.info(f"Retrieved call details for {call_id}")
                    return data["data"]["call"]
                else:
                    raise Exception(data.get("error", "Unknown error"))
        except Exception as e:
            logger.error(f"Failed to get call details: {e}")
            raise
    
    async def get_call_analysis(self, call_id: str) -> Dict[str, Any]:
        """
        Get AI-generated analysis for a call.
        
        Endpoint: GET /api/v1/calls/{callId}/analysis
        
        Args:
            call_id: Call UUID or callSid
            
        Returns:
            CallAnalysis object with sentiment, metadata, rawResponse
        """
        url = f"{self.base_url}/api/v1/calls/{call_id}/analysis"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                if data.get("success"):
                    logger.info(f"Retrieved analysis for call {call_id}")
                    return data["data"]
                else:
                    raise Exception(data.get("error", "Unknown error"))
        except Exception as e:
            logger.error(f"Failed to get call analysis: {e}")
            raise
    
    async def get_call_transcript(self, call_id: str) -> Dict[str, Any]:
        """
        Get full text transcript of a call.
        
        Endpoint: GET /api/v1/calls/{callId}/transcript
        
        Args:
            call_id: Call UUID or callSid
            
        Returns:
            CallTranscript object with transcript text and metadata
        """
        url = f"{self.base_url}/api/v1/calls/{call_id}/transcript"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                if data.get("success"):
                    logger.info(f"Retrieved transcript for call {call_id}")
                    return data["data"]
                else:
                    raise Exception(data.get("error", "Unknown error"))
        except Exception as e:
            logger.error(f"Failed to get call transcript: {e}")
            raise
    
    async def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information including credits and usage.
        
        Endpoint: GET /api/v1/account
        
        Returns:
            Account details with user info, credits, and usage stats
        """
        url = f"{self.base_url}/api/v1/account"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                if data.get("success"):
                    logger.info("Retrieved account information")
                    return data["data"]["account"]
                else:
                    raise Exception(data.get("error", "Unknown error"))
        except Exception as e:
            logger.error(f"Failed to get account info: {e}")
            raise
    
    async def get_inbound_call(self, call_id: str) -> Dict[str, Any]:
        """
        Get details of an inbound call.
        
        Endpoint: GET /api/v1/inbound-calls/{callId}
        
        Args:
            call_id: Inbound call UUID
            
        Returns:
            Inbound call details with agent, analysis, and routing info
        """
        url = f"{self.base_url}/api/v1/inbound-calls/{call_id}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                if data.get("success"):
                    logger.info(f"Retrieved inbound call {call_id}")
                    return data["data"]["inboundCall"]
                else:
                    raise Exception(data.get("error", "Unknown error"))
        except Exception as e:
            logger.error(f"Failed to get inbound call: {e}")
            raise
    
    async def get_full_call_data(self, call_id: str) -> Dict[str, Any]:
        """
        Fetch all data for a completed call (details, analysis, transcript).
        
        Args:
            call_id: Call UUID or callSid
            
        Returns:
            Combined data with call details, analysis, and transcript
        """
        try:
            # Fetch all data in parallel
            call_details, analysis, transcript = await asyncio.gather(
                self.get_call_details(call_id),
                self.get_call_analysis(call_id),
                self.get_call_transcript(call_id),
                return_exceptions=True
            )
            
            # Handle any errors
            if isinstance(call_details, Exception):
                logger.error(f"Call details fetch error: {call_details}")
                call_details = None
            if isinstance(analysis, Exception):
                logger.error(f"Analysis fetch error: {analysis}")
                analysis = None
            if isinstance(transcript, Exception):
                logger.error(f"Transcript fetch error: {transcript}")
                transcript = None
            
            return {
                "callId": call_id,
                "call": call_details,
                "analysis": analysis,
                "transcript": transcript.get("transcript") if transcript else None,
                "transcriptData": transcript,
                # Extract memory/metadata from analysis if available
                "memory": analysis.get("metadata", {}) if analysis else {}
            }
        except Exception as e:
            logger.error(f"Failed to fetch full call data: {e}")
            raise
