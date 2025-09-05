from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DriverBase(BaseModel):
    name: str
    phone: str
    license_number: str
    vehicle_id: Optional[str] = None

class DriverCreate(DriverBase):
    user_id: str

class DriverUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    license_number: Optional[str] = None
    is_available: Optional[bool] = None
    current_location: Optional[str] = None
    vehicle_id: Optional[str] = None

class DriverInDB(DriverBase):
    id: str
    user_id: str
    is_available: bool = False
    current_location: Optional[str] = None
    created_at: datetime

class Driver(DriverBase):
    id: str
    user_id: str
    is_available: bool
    current_location: Optional[str] = None
    created_at: datetime
