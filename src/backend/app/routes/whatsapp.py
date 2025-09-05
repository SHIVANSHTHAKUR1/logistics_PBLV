from fastapi import APIRouter, Request, HTTPException, Depends
from typing import Dict, Any
import json
from ..database import get_supabase_client
from supabase import Client
from .message_processor import process_whatsapp_message

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])

@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = None,
    hub_challenge: str = None,
    hub_verify_token: str = None
):
    """
    Webhook verification endpoint for WhatsApp Business API
    """
    # Replace with your actual verify token
    VERIFY_TOKEN = "your_webhook_verify_token"
    
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)
    else:
        raise HTTPException(status_code=403, detail="Forbidden")

@router.post("/webhook")
async def whatsapp_webhook(
    request: Request,
    supabase: Client = Depends(get_supabase_client)
):
    """
    Main webhook endpoint to receive WhatsApp messages
    """
    try:
        data = await request.json()
        
        # Log the incoming webhook data for debugging
        print(f"Received WhatsApp webhook: {json.dumps(data, indent=2)}")
        
        # Extract message data from WhatsApp webhook format
        if "entry" in data:
            for entry in data["entry"]:
                if "changes" in entry:
                    for change in entry["changes"]:
                        if change.get("field") == "messages":
                            value = change.get("value", {})
                            
                            # Process incoming messages
                            if "messages" in value:
                                for message in value["messages"]:
                                    await process_incoming_message(message, supabase)
                            
                            # Process message status updates
                            if "statuses" in value:
                                for status in value["statuses"]:
                                    await process_message_status(status, supabase)
        
        return {"status": "processed"}
    
    except Exception as e:
        print(f"Error processing WhatsApp webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def process_incoming_message(message: Dict[str, Any], supabase: Client):
    """
    Process incoming WhatsApp message
    """
    try:
        from_number = message.get("from", "")
        message_type = message.get("type", "")
        
        if message_type == "text":
            message_text = message.get("text", {}).get("body", "").upper().strip()
            
            # Process the message using our message processor
            response = await process_whatsapp_message(from_number, message_text, supabase)
            
            # Log the processing result
            print(f"Processed message from {from_number}: {message_text} -> {response}")
        
        elif message_type == "image":
            # Handle image messages (receipts, etc.)
            await process_image_message(message, supabase)
        
        else:
            print(f"Unsupported message type: {message_type}")
    
    except Exception as e:
        print(f"Error processing incoming message: {e}")

async def process_message_status(status: Dict[str, Any], supabase: Client):
    """
    Process WhatsApp message status updates (sent, delivered, read, failed)
    """
    try:
        message_id = status.get("id", "")
        status_type = status.get("status", "")
        
        # Log status updates for monitoring
        print(f"Message {message_id} status: {status_type}")
        
        # You can implement status tracking in database here
        # For example, update message delivery status in a messages table
        
    except Exception as e:
        print(f"Error processing message status: {e}")

async def process_image_message(message: Dict[str, Any], supabase: Client):
    """
    Process image messages (potential expense receipts)
    """
    try:
        from_number = message.get("from", "")
        image_data = message.get("image", {})
        image_id = image_data.get("id", "")
        
        print(f"Received image from {from_number}, image ID: {image_id}")
        
        # TODO: Download image using WhatsApp Business API
        # TODO: Process with OCR for expense receipt extraction
        # TODO: Create expense record automatically
        
        # For now, just log the event
        print("Image processing not yet implemented")
        
    except Exception as e:
        print(f"Error processing image message: {e}")
