"""
WhatsApp message processing logic for logistics automation
Enhanced with AI agents for intelligent responses
"""
from typing import Optional, Dict, Any
from uuid import UUID
from supabase import Client
import re

# Import AI agents
try:
    from ..agents.availability_agent import AvailabilityAgent
    availability_agent = AvailabilityAgent()
except ImportError:
    availability_agent = None

async def process_whatsapp_message(
    from_number: str, 
    message_text: str, 
    supabase: Client
) -> str:
    """
    Main message processing function with AI enhancement
    Routes messages to appropriate handlers based on content
    """
    try:
        # Clean up the message text
        message_text = message_text.upper().strip()
        
        # Use AI agent for availability updates if available
        if availability_agent and message_text in ["FREE", "AVAILABLE", "READY", "BUSY", "OCCUPIED", "NOT AVAILABLE"]:
            result = await availability_agent.update_driver_availability(
                phone_number=from_number,
                status=message_text
            )
            
            if result.get("success"):
                response = result.get("message", "Status updated successfully")
                
                # Add trip suggestion if available
                if result.get("action") == "trip_suggestion" and result.get("suggested_trip"):
                    trip = result["suggested_trip"]
                    response += f"\n\n🚛 **New Trip Opportunity!**\n"
                    response += f"From: {trip.get('pickup_location', 'N/A')}\n"
                    response += f"To: {trip.get('destination', 'N/A')}\n"
                    response += f"Reply YES to accept or NO to decline"
                
                return response
            else:
                return result.get("message", "Failed to update status")
        
        # Fallback to original logic
        return await process_whatsapp_message_original(from_number, message_text, supabase)
    
    except Exception as e:
        print(f"Error in AI-enhanced message processing: {e}")
        # Fallback to original processing
        return await process_whatsapp_message_original(from_number, message_text, supabase)

async def process_whatsapp_message_original(
    from_number: str, 
    message_text: str, 
    supabase: Client
) -> str:
    """
    Main message processing function
    Routes messages to appropriate handlers based on content
    """
    try:
        # Clean up the message text
        message_text = message_text.upper().strip()
        
        # Find driver by phone number
        driver = await get_driver_by_phone(from_number, supabase)
        
        if not driver:
            return "❌ Driver not found. Please contact admin to register your phone number."
        
        # Route message to appropriate handler
        if message_text in ["FREE", "AVAILABLE", "READY"]:
            return await handle_driver_availability(driver["id"], True, supabase)
        
        elif message_text in ["BUSY", "OCCUPIED", "NOT AVAILABLE"]:
            return await handle_driver_availability(driver["id"], False, supabase)
        
        elif message_text in ["YES", "ACCEPT", "OK"]:
            return await handle_trip_acceptance(driver["id"], supabase)
        
        elif message_text in ["NO", "DECLINE", "REJECT"]:
            return await handle_trip_rejection(driver["id"], supabase)
        
        elif message_text.startswith("LOCATION"):
            # Extract location from message like "LOCATION Mumbai Central"
            location = message_text.replace("LOCATION", "").strip()
            return await handle_location_update(driver["id"], location, supabase)
        
        elif message_text in ["STATUS", "INFO"]:
            return await handle_status_request(driver["id"], supabase)
        
        elif message_text in ["HELP", "COMMANDS"]:
            return get_help_message()
        
        else:
            return get_unknown_command_message()
    
    except Exception as e:
        print(f"Error processing WhatsApp message: {e}")
        return "❌ Sorry, there was an error processing your message. Please try again."

async def get_driver_by_phone(phone_number: str, supabase: Client) -> Optional[Dict[str, Any]]:
    """
    Get driver information by phone number
    """
    try:
        result = supabase.table("drivers").select("*").eq("phone", phone_number).execute()
        
        if result.data:
            return result.data[0]
        return None
    
    except Exception as e:
        print(f"Error fetching driver by phone: {e}")
        return None

async def handle_driver_availability(
    driver_id: str, 
    is_available: bool, 
    supabase: Client
) -> str:
    """
    Update driver availability status
    """
    try:
        result = supabase.table("drivers").update({
            "is_available": is_available
        }).eq("id", driver_id).execute()
        
        if result.data:
            status = "available" if is_available else "busy"
            return f"✅ Your status has been updated to: {status.upper()}"
        else:
            return "❌ Failed to update your status. Please try again."
    
    except Exception as e:
        print(f"Error updating driver availability: {e}")
        return "❌ Error updating your status. Please try again."

async def handle_location_update(
    driver_id: str, 
    location: str, 
    supabase: Client
) -> str:
    """
    Update driver's current location
    """
    try:
        if not location:
            return "❌ Please provide a location. Example: LOCATION Mumbai Central"
        
        result = supabase.table("drivers").update({
            "current_location": location
        }).eq("id", driver_id).execute()
        
        if result.data:
            return f"✅ Your location has been updated to: {location}"
        else:
            return "❌ Failed to update your location. Please try again."
    
    except Exception as e:
        print(f"Error updating driver location: {e}")
        return "❌ Error updating your location. Please try again."

async def handle_trip_acceptance(driver_id: str, supabase: Client) -> str:
    """
    Handle driver accepting a trip
    """
    try:
        # Find pending trip assigned to this driver
        trip_result = supabase.table("trips").select("*").eq("driver_id", driver_id).eq("status", "assigned").execute()
        
        if not trip_result.data:
            return "❌ No pending trip assignment found."
        
        trip = trip_result.data[0]
        
        # Update trip status to in_progress
        update_result = supabase.table("trips").update({
            "status": "in_progress"
        }).eq("id", trip["id"]).execute()
        
        if update_result.data:
            return f"✅ Trip accepted! From: {trip['pickup_location']} To: {trip['destination']} Please proceed to pickup location."
        else:
            return "❌ Failed to accept trip. Please try again."
    
    except Exception as e:
        print(f"Error handling trip acceptance: {e}")
        return "❌ Error accepting trip. Please try again."

async def handle_trip_rejection(driver_id: str, supabase: Client) -> str:
    """
    Handle driver rejecting a trip
    """
    try:
        # Find pending trip assigned to this driver
        trip_result = supabase.table("trips").select("*").eq("driver_id", driver_id).eq("status", "assigned").execute()
        
        if not trip_result.data:
            return "❌ No pending trip assignment found."
        
        trip = trip_result.data[0]
        
        # Update trip back to pending and remove driver assignment
        update_result = supabase.table("trips").update({
            "status": "pending",
            "driver_id": None
        }).eq("id", trip["id"]).execute()
        
        if update_result.data:
            # Make driver available again
            supabase.table("drivers").update({
                "is_available": True
            }).eq("id", driver_id).execute()
            
            return "✅ Trip declined. You are now available for new assignments."
        else:
            return "❌ Failed to decline trip. Please try again."
    
    except Exception as e:
        print(f"Error handling trip rejection: {e}")
        return "❌ Error declining trip. Please try again."

async def handle_status_request(driver_id: str, supabase: Client) -> str:
    """
    Get current driver status and active trips
    """
    try:
        # Get driver info
        driver_result = supabase.table("drivers").select("*").eq("id", driver_id).execute()
        
        if not driver_result.data:
            return "❌ Driver not found."
        
        driver = driver_result.data[0]
        
        # Get active trips
        trip_result = supabase.table("trips").select("*").eq("driver_id", driver_id).in_("status", ["assigned", "in_progress"]).execute()
        
        status_message = f"👤 Driver: {driver['name']}\n"
        status_message += f"📍 Status: {'Available' if driver['is_available'] else 'Busy'}\n"
        
        if driver.get('current_location'):
            status_message += f"🗺️ Location: {driver['current_location']}\n"
        
        if trip_result.data:
            trip = trip_result.data[0]
            status_message += f"\n🚛 Active Trip:\n"
            status_message += f"From: {trip['pickup_location']}\n"
            status_message += f"To: {trip['destination']}\n"
            status_message += f"Status: {trip['status'].title()}"
        else:
            status_message += "\n✅ No active trips"
        
        return status_message
    
    except Exception as e:
        print(f"Error handling status request: {e}")
        return "❌ Error getting your status. Please try again."

def get_help_message() -> str:
    """
    Return help message with available commands
    """
    return """
🤖 **Logistics Bot Commands:**

📱 **Availability:**
• FREE / AVAILABLE - Mark yourself as available
• BUSY / OCCUPIED - Mark yourself as busy

📍 **Location:**
• LOCATION [place] - Update your location
  Example: LOCATION Mumbai Central

🚛 **Trip Management:**
• YES / ACCEPT - Accept assigned trip
• NO / DECLINE - Decline assigned trip

ℹ️ **Information:**
• STATUS / INFO - Get your current status
• HELP / COMMANDS - Show this help

Need assistance? Contact support.
    """.strip()

def get_unknown_command_message() -> str:
    """
    Return message for unknown commands
    """
    return "❓ Unknown command. Send HELP to see available commands."
