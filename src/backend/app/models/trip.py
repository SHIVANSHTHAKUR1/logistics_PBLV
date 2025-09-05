from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class TripStatus(str, Enum):
    ASSIGNED = "assigned"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TripBase(BaseModel):
    driver_id: str
    load_id: str
    pickup_location: str
    delivery_location: str
    freight_amount: float
    pickup_date: datetime

class TripCreate(TripBase):
    pass

class TripUpdate(BaseModel):
    status: Optional[TripStatus] = None
    pickup_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None

class TripInDB(TripBase):
    id: str
    status: TripStatus = TripStatus.ASSIGNED
    delivery_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class Trip(TripBase):
    id: str
    status: TripStatus
    delivery_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
