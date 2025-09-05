from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime, date
from enum import Enum

class ExpenseCategory(str, Enum):
    FUEL = "fuel"
    MAINTENANCE = "maintenance"
    TOLL = "toll"
    FOOD = "food"
    PARKING = "parking"
    OTHER = "other"

class ExpenseBase(BaseModel):
    trip_id: UUID
    category: ExpenseCategory
    amount: float = Field(..., gt=0, description="Amount must be positive")
    description: Optional[str] = None
    expense_date: Optional[date] = None
    receipt_image: Optional[str] = None  # Base64 encoded image

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    category: Optional[ExpenseCategory] = None
    amount: Optional[float] = Field(None, gt=0, description="Amount must be positive")
    description: Optional[str] = None
    expense_date: Optional[date] = None
    receipt_image: Optional[str] = None

class Expense(ExpenseBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
