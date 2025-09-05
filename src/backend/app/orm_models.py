from sqlalchemy import Column, String, Integer, Float, Date, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base


class Driver(Base):
    __tablename__ = 'drivers'

    id = Column(String, primary_key=True, index=True)  # use CSV driver_id
    name = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)
    license_number = Column(String)
    experience_years = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    current_location_lat = Column(Float, nullable=True)
    current_location_lng = Column(Float, nullable=True)
    availability_status = Column(String, default='available')
    preferred_routes = Column(Text, nullable=True)
    vehicle_type = Column(String, nullable=True)

    trips = relationship('Trip', back_populates='driver')


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(String, primary_key=True, index=True)  # use CSV vehicle_id
    registration_number = Column(String)
    vehicle_type = Column(String)
    capacity_tons = Column(Float)
    fuel_type = Column(String)
    mileage_kmpl = Column(Float)
    owner_id = Column(String)
    driver_id = Column(String, ForeignKey('drivers.id'), nullable=True)
    current_location_lat = Column(Float, nullable=True)
    current_location_lng = Column(Float, nullable=True)
    status = Column(String, default='active')
    last_maintenance_date = Column(Date, nullable=True)

    driver = relationship('Driver')
    trips = relationship('Trip', back_populates='vehicle')


class Trip(Base):
    __tablename__ = 'trips'

    id = Column(String, primary_key=True, index=True)  # use CSV trip_id
    driver_id = Column(String, ForeignKey('drivers.id'))
    vehicle_id = Column(String, ForeignKey('vehicles.id'))
    pickup_location = Column(String)
    pickup_lat = Column(Float)
    pickup_lng = Column(Float)
    delivery_location = Column(String)
    delivery_lat = Column(Float)
    delivery_lng = Column(Float)
    cargo_type = Column(String)
    cargo_weight_tons = Column(Float)
    cargo_value_inr = Column(Float)
    pickup_date = Column(Date)
    delivery_date = Column(Date, nullable=True)
    status = Column(String, default='scheduled')
    distance_km = Column(Float, nullable=True)
    estimated_fuel_cost = Column(Float, nullable=True)
    actual_fuel_cost = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    driver = relationship('Driver', back_populates='trips')
    vehicle = relationship('Vehicle', back_populates='trips')
    expenses = relationship('Expense', back_populates='trip')


class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(String, primary_key=True, index=True)  # use CSV expense_id
    trip_id = Column(String, ForeignKey('trips.id'))
    driver_id = Column(String, ForeignKey('drivers.id'))
    expense_type = Column(String)
    amount_inr = Column(Float)
    description = Column(Text, nullable=True)
    receipt_number = Column(String, nullable=True)
    expense_date = Column(Date)
    location = Column(String, nullable=True)
    payment_method = Column(String, nullable=True)
    approved_status = Column(String, default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    trip = relationship('Trip', back_populates='expenses')
