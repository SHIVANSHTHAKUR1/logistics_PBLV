from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date
from .db import get_db_session
from .orm_models import Driver, Vehicle, Trip, Expense


router = APIRouter()


# Dashboard endpoints used by frontend
@router.get('/dashboard/stats')
def dashboard_stats(db: Session = Depends(get_db_session)):
    total_trips = db.query(Trip).count()
    active_trips = db.query(Trip).filter(Trip.status.in_(['scheduled', 'in_progress', 'assigned'])).count()
    available_drivers = db.query(Driver).filter(Driver.availability_status == 'available').count()
    total_expenses = float(db.query(Expense).with_entities((Expense.amount_inr)).all() and sum([e[0] or 0 for e in db.query(Expense.amount_inr).all()]) or 0)

    # Rough revenue estimation as cargo_value sum (placeholder)
    total_revenue = float(db.query(Trip).with_entities((Trip.cargo_value_inr)).all() and sum([t[0] or 0 for t in db.query(Trip.cargo_value_inr).all()]) or 0)

    # Fleet utilization heuristic
    total_vehicles = db.query(Vehicle).count()
    fleet_utilization = 0
    if total_vehicles:
        busy = db.query(Trip.vehicle_id).filter(Trip.status.in_(['in_progress', 'assigned'])).distinct().count()
        fleet_utilization = round((busy / total_vehicles) * 100, 2)

    return {
        'totalTrips': total_trips,
        'activeTrips': active_trips,
        'availableDrivers': available_drivers,
        'totalRevenue': total_revenue,
        'totalExpenses': total_expenses,
        'fleetUtilization': fleet_utilization,
    }


@router.get('/dashboard/activities')
def dashboard_activities(db: Session = Depends(get_db_session)):
    # Simple recent activities feed from trips & expenses
    activities = []
    for t in db.query(Trip).order_by(Trip.updated_at.desc()).limit(10).all():
        activities.append({
            'type': 'trip',
            'id': t.id,
            'status': t.status,
            'pickup': t.pickup_location,
            'delivery': t.delivery_location,
            'updated_at': t.updated_at.isoformat() if t.updated_at else None,
        })
    for e in db.query(Expense).order_by(Expense.updated_at.desc()).limit(10).all():
        activities.append({
            'type': 'expense',
            'id': e.id,
            'trip_id': e.trip_id,
            'amount': e.amount_inr,
            'date': e.expense_date.isoformat() if e.expense_date else None,
        })
    return activities[:20]


# Drivers
@router.get('/drivers')
def list_drivers(db: Session = Depends(get_db_session)):
    return [
        {
            'id': d.id,
            'name': d.name,
            'phone': d.phone,
            'email': d.email,
            'license_number': d.license_number,
            'experience_years': d.experience_years,
            'rating': d.rating,
            'status': d.availability_status,
            'current_location': {
                'lat': d.current_location_lat,
                'lng': d.current_location_lng,
            },
            'vehicle_type': d.vehicle_type,
        }
        for d in db.query(Driver).all()
    ]


# Vehicles
@router.get('/vehicles')
def list_vehicles(db: Session = Depends(get_db_session)):
    return [
        {
            'id': v.id,
            'registration_number': v.registration_number,
            'vehicle_type': v.vehicle_type,
            'capacity_tons': v.capacity_tons,
            'status': v.status,
            'driver_id': v.driver_id,
        }
        for v in db.query(Vehicle).all()
    ]


# Trips
@router.get('/trips')
def list_trips(
    status: Optional[str] = None,
    driver_id: Optional[str] = None,
    db: Session = Depends(get_db_session),
):
    q = db.query(Trip)
    if status:
        q = q.filter(Trip.status == status)
    if driver_id:
        q = q.filter(Trip.driver_id == driver_id)
    trips = q.order_by(Trip.created_at.desc()).all()
    out = []
    for t in trips:
        out.append({
            'id': t.id,
            'pickup_location': t.pickup_location,
            'delivery_location': t.delivery_location,
            'pickup_datetime': t.pickup_date.isoformat() if t.pickup_date else None,
            'delivery_datetime': t.delivery_date.isoformat() if t.delivery_date else None,
            'status': t.status,
            'driver_id': t.driver_id,
            'vehicle_id': t.vehicle_id,
            'load_details': {
                'weight': t.cargo_weight_tons,
                'type': t.cargo_type,
                'value': t.cargo_value_inr,
            },
            'route_optimization': {
                'distance': t.distance_km,
                'fuel_cost': t.estimated_fuel_cost,
            },
            'created_at': t.created_at.isoformat() if t.created_at else None,
        })
    return out


# Expenses
@router.get('/expenses')
def list_expenses(
    trip_id: Optional[str] = None,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db_session),
):
    q = db.query(Expense)
    if trip_id:
        q = q.filter(Expense.trip_id == trip_id)
    if start_date:
        q = q.filter(Expense.expense_date >= start_date)
    if end_date:
        q = q.filter(Expense.expense_date <= end_date)
    items = q.order_by(Expense.expense_date.desc()).all()
    return [
        {
            'id': e.id,
            'trip_id': e.trip_id,
            'driver_id': e.driver_id,
            'expense_type': e.expense_type,
            'amount_inr': e.amount_inr,
            'description': e.description,
            'expense_date': e.expense_date.isoformat() if e.expense_date else None,
            'approved_status': e.approved_status,
        }
        for e in items
    ]


@router.get('/expenses/analytics')
def expenses_analytics(db: Session = Depends(get_db_session)):
    # Simple grouping by expense_type
    rows = db.query(Expense.expense_type, Expense.amount_inr).all()
    summary = {}
    for etype, amt in rows:
        summary[etype] = summary.get(etype, 0) + float(amt or 0)
    return { 'byType': summary, 'total': sum(summary.values()) }
