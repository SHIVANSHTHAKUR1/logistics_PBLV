from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from typing import List, Optional
from uuid import UUID
from datetime import datetime, date
from ..models.expense import Expense, ExpenseCreate, ExpenseUpdate, ExpenseCategory
from ..database import get_supabase_client
from supabase import Client
import base64

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/", response_model=Expense, status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense: ExpenseCreate,
    supabase: Client = Depends(get_supabase_client)
):
    """Create a new expense"""
    try:
        # Add created_at timestamp
        expense_data = expense.dict()
        expense_data["created_at"] = datetime.utcnow().isoformat()
        
        result = supabase.table("expenses").insert(expense_data).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create expense"
            )
        
        return Expense(**result.data[0])
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating expense: {str(e)}"
        )

@router.post("/upload-receipt/", response_model=Expense, status_code=status.HTTP_201_CREATED)
async def create_expense_with_receipt(
    trip_id: UUID,
    category: ExpenseCategory,
    description: str,
    receipt: UploadFile = File(...),
    supabase: Client = Depends(get_supabase_client)
):
    """Create expense with receipt image upload"""
    try:
        # Read and encode the uploaded image
        image_data = await receipt.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # TODO: Implement OCR to extract amount from receipt
        # For now, we'll set amount to 0 and require manual entry
        extracted_amount = 0.0  # This would be extracted using OCR
        
        expense_data = {
            "trip_id": str(trip_id),
            "category": category.value,
            "amount": extracted_amount,
            "description": description,
            "receipt_image": image_base64,
            "created_at": datetime.utcnow().isoformat()
        }
        
        result = supabase.table("expenses").insert(expense_data).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create expense with receipt"
            )
        
        return Expense(**result.data[0])
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating expense with receipt: {str(e)}"
        )

@router.get("/", response_model=List[Expense])
async def get_expenses(
    skip: int = 0,
    limit: int = 100,
    category: Optional[ExpenseCategory] = None,
    trip_id: Optional[UUID] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    supabase: Client = Depends(get_supabase_client)
):
    """Get all expenses with optional filtering"""
    try:
        query = supabase.table("expenses").select("*")
        
        # Apply filters
        if category:
            query = query.eq("category", category.value)
        if trip_id:
            query = query.eq("trip_id", str(trip_id))
        if start_date:
            query = query.gte("expense_date", start_date.isoformat())
        if end_date:
            query = query.lte("expense_date", end_date.isoformat())
        
        # Apply pagination and order by expense_date
        result = query.order("expense_date", desc=True).range(skip, skip + limit - 1).execute()
        
        return [Expense(**expense) for expense in result.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching expenses: {str(e)}"
        )

@router.get("/{expense_id}", response_model=Expense)
async def get_expense(
    expense_id: UUID,
    supabase: Client = Depends(get_supabase_client)
):
    """Get a specific expense by ID"""
    try:
        result = supabase.table("expenses").select("*").eq("id", str(expense_id)).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )
        
        return Expense(**result.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching expense: {str(e)}"
        )

@router.put("/{expense_id}", response_model=Expense)
async def update_expense(
    expense_id: UUID,
    expense_update: ExpenseUpdate,
    supabase: Client = Depends(get_supabase_client)
):
    """Update an expense"""
    try:
        # Only update fields that are provided
        update_data = {k: v for k, v in expense_update.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields to update"
            )
        
        result = supabase.table("expenses").update(update_data).eq("id", str(expense_id)).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )
        
        return Expense(**result.data[0])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating expense: {str(e)}"
        )

@router.delete("/{expense_id}")
async def delete_expense(
    expense_id: UUID,
    supabase: Client = Depends(get_supabase_client)
):
    """Delete an expense"""
    try:
        result = supabase.table("expenses").delete().eq("id", str(expense_id)).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )
        
        return {"message": "Expense deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting expense: {str(e)}"
        )

@router.get("/trip/{trip_id}", response_model=List[Expense])
async def get_trip_expenses(
    trip_id: UUID,
    category: Optional[ExpenseCategory] = None,
    supabase: Client = Depends(get_supabase_client)
):
    """Get all expenses for a specific trip"""
    try:
        query = supabase.table("expenses").select("*").eq("trip_id", str(trip_id))
        
        if category:
            query = query.eq("category", category.value)
        
        result = query.order("expense_date", desc=True).execute()
        
        return [Expense(**expense) for expense in result.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching trip expenses: {str(e)}"
        )

@router.get("/summary/by-category")
async def get_expense_summary_by_category(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    supabase: Client = Depends(get_supabase_client)
):
    """Get expense summary grouped by category"""
    try:
        query = supabase.table("expenses").select("category, amount")
        
        if start_date:
            query = query.gte("expense_date", start_date.isoformat())
        if end_date:
            query = query.lte("expense_date", end_date.isoformat())
        
        result = query.execute()
        
        # Group by category and sum amounts
        category_totals = {}
        for expense in result.data:
            category = expense["category"]
            amount = float(expense["amount"])
            category_totals[category] = category_totals.get(category, 0) + amount
        
        return {
            "summary": category_totals,
            "total": sum(category_totals.values()),
            "period": {
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating expense summary: {str(e)}"
        )

@router.get("/summary/by-trip")
async def get_expense_summary_by_trip(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    supabase: Client = Depends(get_supabase_client)
):
    """Get expense summary grouped by trip"""
    try:
        query = supabase.table("expenses").select("trip_id, amount")
        
        if start_date:
            query = query.gte("expense_date", start_date.isoformat())
        if end_date:
            query = query.lte("expense_date", end_date.isoformat())
        
        result = query.execute()
        
        # Group by trip and sum amounts
        trip_totals = {}
        for expense in result.data:
            trip_id = expense["trip_id"]
            amount = float(expense["amount"])
            trip_totals[trip_id] = trip_totals.get(trip_id, 0) + amount
        
        return {
            "summary": trip_totals,
            "total": sum(trip_totals.values()),
            "period": {
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating trip expense summary: {str(e)}"
        )
