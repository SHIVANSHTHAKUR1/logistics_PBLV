import csv
import os
from datetime import datetime, date
from sqlalchemy.orm import Session
from .db import Base, engine
from .orm_models import Driver, Vehicle, Trip, Expense


def _parse_date(value: str):
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except Exception:
            continue
    return None


def init_db():
    Base.metadata.create_all(bind=engine)


def seed_from_csvs(db: Session, project_root: str):
    raw_dir = os.path.join(project_root, 'data', 'raw')

    # Seed drivers
    drivers_csv = os.path.join(raw_dir, 'drivers.csv')
    if os.path.exists(drivers_csv):
        with open(drivers_csv, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not db.get(Driver, row['driver_id']):
                    db.add(Driver(
                        id=row['driver_id'],
                        name=row.get('name'),
                        phone=row.get('phone'),
                        email=row.get('email'),
                        license_number=row.get('license_number'),
                        experience_years=int(row.get('experience_years') or 0),
                        rating=float(row.get('rating') or 0.0),
                        current_location_lat=float(row.get('current_location_lat') or 0) or None,
                        current_location_lng=float(row.get('current_location_lng') or 0) or None,
                        availability_status=row.get('availability_status') or 'available',
                        preferred_routes=row.get('preferred_routes') or None,
                        vehicle_type=row.get('vehicle_type') or None,
                    ))

    # Seed vehicles
    vehicles_csv = os.path.join(raw_dir, 'vehicles.csv')
    if os.path.exists(vehicles_csv):
        with open(vehicles_csv, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not db.get(Vehicle, row['vehicle_id']):
                    db.add(Vehicle(
                        id=row['vehicle_id'],
                        registration_number=row.get('registration_number'),
                        vehicle_type=row.get('vehicle_type'),
                        capacity_tons=float(row.get('capacity_tons') or 0) or None,
                        fuel_type=row.get('fuel_type'),
                        mileage_kmpl=float(row.get('mileage_kmpl') or 0) or None,
                        owner_id=row.get('owner_id'),
                        driver_id=row.get('driver_id') or None,
                        current_location_lat=float(row.get('current_location_lat') or 0) or None,
                        current_location_lng=float(row.get('current_location_lng') or 0) or None,
                        status=row.get('status') or 'active',
                        last_maintenance_date=_parse_date(row.get('last_maintenance_date') or ''),
                    ))

    # Seed trips
    trips_csv = os.path.join(raw_dir, 'trips.csv')
    if os.path.exists(trips_csv):
        with open(trips_csv, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not db.get(Trip, row['trip_id']):
                    db.add(Trip(
                        id=row['trip_id'],
                        driver_id=row.get('driver_id'),
                        vehicle_id=row.get('vehicle_id'),
                        pickup_location=row.get('pickup_location'),
                        pickup_lat=float(row.get('pickup_lat') or 0) or None,
                        pickup_lng=float(row.get('pickup_lng') or 0) or None,
                        delivery_location=row.get('delivery_location'),
                        delivery_lat=float(row.get('delivery_lat') or 0) or None,
                        delivery_lng=float(row.get('delivery_lng') or 0) or None,
                        cargo_type=row.get('cargo_type'),
                        cargo_weight_tons=float(row.get('cargo_weight_tons') or 0) or None,
                        cargo_value_inr=float(row.get('cargo_value_inr') or 0) or None,
                        pickup_date=_parse_date(row.get('pickup_date') or ''),
                        delivery_date=_parse_date(row.get('delivery_date') or ''),
                        status=row.get('status') or 'scheduled',
                        distance_km=float(row.get('distance_km') or 0) or None,
                        estimated_fuel_cost=float(row.get('estimated_fuel_cost') or 0) or None,
                        actual_fuel_cost=float(row.get('actual_fuel_cost') or 0) or None,
                    ))

    # Seed expenses
    expenses_csv = os.path.join(raw_dir, 'expenses.csv')
    if os.path.exists(expenses_csv):
        with open(expenses_csv, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not db.get(Expense, row['expense_id']):
                    db.add(Expense(
                        id=row['expense_id'],
                        trip_id=row.get('trip_id'),
                        driver_id=row.get('driver_id'),
                        expense_type=row.get('expense_type'),
                        amount_inr=float(row.get('amount_inr') or 0) or None,
                        description=row.get('description') or None,
                        receipt_number=row.get('receipt_number') or None,
                        expense_date=_parse_date(row.get('expense_date') or ''),
                        location=row.get('location') or None,
                        payment_method=row.get('payment_method') or None,
                        approved_status=row.get('approved_status') or 'pending',
                    ))

    db.commit()
