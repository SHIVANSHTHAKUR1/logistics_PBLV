from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from ..models.trip import Trip, TripCreate, TripUpdate, TripStatus
from ..database import get_supabase_client
from supabase import Client

router = APIRouter(prefix="/trips", tags=["trips"])

@router.post("/", response_model=Trip, status_code=status.HTTP_201_CREATED)
async def create_trip(
    trip: TripCreate,
    supabase: Client = Depends(get_supabase_client)
):
    """Create a new trip"""
    try:
        # Add created_at timestamp
        trip_data = trip.dict()
        trip_data["created_at"] = datetime.utcnow().isoformat()
        
        result = supabase.table("trips").insert(trip_data).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create trip"
            )
        
        return Trip(**result.data[0])
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating trip: {str(e)}"
        )

@router.get("/", response_model=List[Trip])
async def get_trips(
    skip: int = 0,
    limit: int = 100,
    status: Optional[TripStatus] = None,
    driver_id: Optional[UUID] = None,
    vehicle_id: Optional[UUID] = None,
    supabase: Client = Depends(get_supabase_client)
):
    """Get all trips with optional filtering"""
    try:
        query = supabase.table("trips").select("*")
        
        # Apply filters
        if status:
            query = query.eq("status", status.value)
        if driver_id:
            query = query.eq("driver_id", str(driver_id))
        if vehicle_id:
            query = query.eq("vehicle_id", str(vehicle_id))
        
        # Apply pagination and order by created_at
        result = query.order("created_at", desc=True).range(skip, skip + limit - 1).execute()
        
        return [Trip(**trip) for trip in result.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching trips: {str(e)}"
        )

@router.get("/{trip_id}", response_model=Trip)
async def get_trip(
    trip_id: UUID,
    supabase: Client = Depends(get_supabase_client)
):
    """Get a specific trip by ID"""
    try:
        result = supabase.table("trips").select("*").eq("id", str(trip_id)).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found"
            )
        
        return Trip(**result.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching trip: {str(e)}"
        )

@router.put("/{trip_id}", response_model=Trip)
async def update_trip(
    trip_id: UUID,
    trip_update: TripUpdate,
    supabase: Client = Depends(get_supabase_client)
):
    """Update a trip"""
    try:
        # Only update fields that are provided
        update_data = {k: v for k, v in trip_update.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields to update"
            )
        
        # Add updated_at timestamp
        update_data["updated_at"] = datetime.utcnow().isoformat()
        
        result = supabase.table("trips").update(update_data).eq("id", str(trip_id)).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found"
            )
        
        return Trip(**result.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating trip: {str(e)}"
        )

@router.patch("/{trip_id}/status")
async def update_trip_status(
    trip_id: UUID,
    new_status: TripStatus,
    supabase: Client = Depends(get_supabase_client)
):
    """Update trip status (used by WhatsApp bot and drivers)"""
    try:
        update_data = {
            "status": new_status.value,
            "updated_at": datetime.utcnow().isoformat()
        }
        
        # Set completion time for completed trips
        if new_status == TripStatus.COMPLETED:
            update_data["completed_at"] = datetime.utcnow().isoformat()
        
        result = supabase.table("trips").update(update_data).eq("id", str(trip_id)).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found"
            )
        
        return {
            "message": f"Trip status updated to {new_status.value}",
            "trip": Trip(**result.data[0])
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating trip status: {str(e)}"
        )

@router.patch("/{trip_id}/assign-driver")
async def assign_driver_to_trip(
    trip_id: UUID,
    driver_id: UUID,
    supabase: Client = Depends(get_supabase_client)
):
    """Assign a driver to a trip"""
    try:
        # Check if driver exists and is available
        driver_result = supabase.table("drivers").select("*").eq("id", str(driver_id)).execute()
        
        if not driver_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )
        
        driver = driver_result.data[0]
        if not driver.get("is_available", False):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Driver is not available"
            )
        
        # Update trip with driver assignment
        trip_update = {
            "driver_id": str(driver_id),
            "status": TripStatus.ASSIGNED.value,
            "updated_at": datetime.utcnow().isoformat()
        }
        
        trip_result = supabase.table("trips").update(trip_update).eq("id", str(trip_id)).execute()
        
        if not trip_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found"
            )
        
        # Mark driver as busy
        supabase.table("drivers").update({"is_available": False}).eq("id", str(driver_id)).execute()
        
        return {
            "message": "Driver assigned to trip successfully",
            "trip": Trip(**trip_result.data[0])
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error assigning driver to trip: {str(e)}"
        )

@router.get("/driver/{driver_id}", response_model=List[Trip])
async def get_driver_trips(
    driver_id: UUID,
    status: Optional[TripStatus] = None,
    supabase: Client = Depends(get_supabase_client)
):
    """Get all trips for a specific driver"""
    try:
        query = supabase.table("trips").select("*").eq("driver_id", str(driver_id))
        
        if status:
            query = query.eq("status", status.value)
        
        result = query.order("created_at", desc=True).execute()
        
        return [Trip(**trip) for trip in result.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching driver trips: {str(e)}"
        )

@router.delete("/{trip_id}")
async def delete_trip(
    trip_id: UUID,
    supabase: Client = Depends(get_supabase_client)
):
    """Delete a trip (only for pending trips)"""
    try:
        # First check if trip exists and is in pending status
        trip_result = supabase.table("trips").select("*").eq("id", str(trip_id)).execute()
        
        if not trip_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found"
            )
        
        trip = trip_result.data[0]
        if trip.get("status") not in [TripStatus.PENDING.value, TripStatus.CANCELLED.value]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete trip that is in progress or completed"
            )
        
        result = supabase.table("trips").delete().eq("id", str(trip_id)).execute()
        
        return {"message": "Trip deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting trip: {str(e)}"
        )
