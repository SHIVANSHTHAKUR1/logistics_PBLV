from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from uuid import UUID
from ..models.driver import Driver, DriverCreate, DriverUpdate
from ..database import get_supabase_client
from supabase import Client

router = APIRouter(prefix="/drivers", tags=["drivers"])

@router.post("/", response_model=Driver, status_code=status.HTTP_201_CREATED)
async def create_driver(
    driver: DriverCreate,
    supabase: Client = Depends(get_supabase_client)
):
    """Create a new driver"""
    try:
        # Insert driver into database
        result = supabase.table("drivers").insert(driver.dict()).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create driver"
            )
        
        return Driver(**result.data[0])
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating driver: {str(e)}"
        )

@router.get("/", response_model=List[Driver])
async def get_drivers(
    skip: int = 0,
    limit: int = 100,
    is_available: Optional[bool] = None,
    supabase: Client = Depends(get_supabase_client)
):
    """Get all drivers with optional filtering"""
    try:
        query = supabase.table("drivers").select("*")
        
        # Apply filters
        if is_available is not None:
            query = query.eq("is_available", is_available)
        
        # Apply pagination
        result = query.range(skip, skip + limit - 1).execute()
        
        return [Driver(**driver) for driver in result.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching drivers: {str(e)}"
        )

@router.get("/{driver_id}", response_model=Driver)
async def get_driver(
    driver_id: UUID,
    supabase: Client = Depends(get_supabase_client)
):
    """Get a specific driver by ID"""
    try:
        result = supabase.table("drivers").select("*").eq("id", str(driver_id)).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )
        
        return Driver(**result.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching driver: {str(e)}"
        )

@router.put("/{driver_id}", response_model=Driver)
async def update_driver(
    driver_id: UUID,
    driver_update: DriverUpdate,
    supabase: Client = Depends(get_supabase_client)
):
    """Update a driver"""
    try:
        # Only update fields that are provided
        update_data = {k: v for k, v in driver_update.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields to update"
            )
        
        result = supabase.table("drivers").update(update_data).eq("id", str(driver_id)).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )
        
        return Driver(**result.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating driver: {str(e)}"
        )

@router.delete("/{driver_id}")
async def delete_driver(
    driver_id: UUID,
    supabase: Client = Depends(get_supabase_client)
):
    """Delete a driver"""
    try:
        result = supabase.table("drivers").delete().eq("id", str(driver_id)).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )
        
        return {"message": "Driver deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting driver: {str(e)}"
        )

@router.patch("/{driver_id}/availability")
async def update_driver_availability(
    driver_id: UUID,
    is_available: bool,
    current_location: Optional[str] = None,
    supabase: Client = Depends(get_supabase_client)
):
    """Update driver availability status (used by WhatsApp bot)"""
    try:
        update_data = {"is_available": is_available}
        if current_location:
            update_data["current_location"] = current_location
        
        result = supabase.table("drivers").update(update_data).eq("id", str(driver_id)).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )
        
        return {
            "message": f"Driver availability updated to {'available' if is_available else 'busy'}",
            "driver": Driver(**result.data[0])
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating driver availability: {str(e)}"
        )

@router.get("/phone/{phone_number}", response_model=Driver)
async def get_driver_by_phone(
    phone_number: str,
    supabase: Client = Depends(get_supabase_client)
):
    """Get driver by phone number (used by WhatsApp bot)"""
    try:
        result = supabase.table("drivers").select("*").eq("phone", phone_number).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found with this phone number"
            )
        
        return Driver(**result.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching driver by phone: {str(e)}"
        )

