# API Documentation

## Overview
This document describes the REST API endpoints for the AI-powered logistics management system.

**Base URL:** `http://localhost:8000/api/v1`
**Authentication:** Bearer Token (JWT)

---

## Authentication Endpoints

### POST /auth/register
Register a new user (owner or driver).

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "role": "owner" | "driver",
  "phone": "string",
  "name": "string"
}
```

**Response:**
```json
{
  "user": {
    "id": "uuid",
    "username": "string",
    "email": "string",
    "role": "string",
    "created_at": "datetime"
  },
  "token": "jwt_token",
  "message": "User registered successfully"
}
```

### POST /auth/login
Authenticate user and get access token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "user": {
    "id": "uuid",
    "username": "string",
    "email": "string",
    "role": "string"
  },
  "token": "jwt_token",
  "expires_in": 3600
}
```

---

## Driver Management

### GET /drivers
Get list of all drivers for the authenticated owner.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `available`: boolean (filter by availability)
- `limit`: integer (pagination limit)
- `offset`: integer (pagination offset)

**Response:**
```json
{
  "drivers": [
    {
      "id": "uuid",
      "name": "string",
      "phone": "string",
      "license_number": "string",
      "is_available": boolean,
      "current_location": "string",
      "vehicle_id": "uuid",
      "created_at": "datetime"
    }
  ],
  "total": 10,
  "limit": 20,
  "offset": 0
}
```

### POST /drivers
Create a new driver.

**Request Body:**
```json
{
  "name": "string",
  "phone": "string",
  "license_number": "string",
  "email": "string"
}
```

### PUT /drivers/{driver_id}/availability
Update driver availability status.

**Request Body:**
```json
{
  "is_available": boolean,
  "current_location": "string"
}
```

---

## Trip Management

### GET /trips
Get list of trips.

**Query Parameters:**
- `status`: string (pending, in_progress, completed, cancelled)
- `driver_id`: uuid
- `date_from`: date
- `date_to`: date

**Response:**
```json
{
  "trips": [
    {
      "id": "uuid",
      "pickup_location": "string",
      "delivery_location": "string",
      "pickup_datetime": "datetime",
      "delivery_datetime": "datetime",
      "status": "string",
      "driver_id": "uuid",
      "vehicle_id": "uuid",
      "load_details": {
        "weight": "number",
        "type": "string",
        "value": "number"
      },
      "route_optimization": {
        "distance": "number",
        "estimated_time": "number",
        "fuel_cost": "number"
      },
      "created_at": "datetime"
    }
  ]
}
```

### POST /trips
Create a new trip.

**Request Body:**
```json
{
  "pickup_location": "string",
  "delivery_location": "string",
  "pickup_datetime": "datetime",
  "load_details": {
    "weight": "number",
    "type": "string",
    "description": "string",
    "value": "number"
  },
  "preferences": {
    "preferred_driver": "uuid",
    "max_cost": "number",
    "priority": "normal" | "high" | "urgent"
  }
}
```

### PUT /trips/{trip_id}/status
Update trip status.

**Request Body:**
```json
{
  "status": "in_progress" | "completed" | "cancelled",
  "location": "string",
  "notes": "string"
}
```

---

## Vehicle Management

### GET /vehicles
Get list of vehicles.

**Response:**
```json
{
  "vehicles": [
    {
      "id": "uuid",
      "registration_number": "string",
      "type": "string",
      "capacity": "number",
      "fuel_type": "string",
      "is_available": boolean,
      "current_driver": "uuid",
      "maintenance": {
        "last_service": "date",
        "next_service": "date",
        "status": "good" | "needs_attention" | "out_of_service"
      }
    }
  ]
}
```

### POST /vehicles
Add a new vehicle.

**Request Body:**
```json
{
  "registration_number": "string",
  "type": "truck" | "van" | "trailer",
  "capacity": "number",
  "fuel_type": "diesel" | "petrol" | "electric",
  "model": "string",
  "year": "number"
}
```

---

## Expense Management

### GET /expenses
Get expense records.

**Query Parameters:**
- `trip_id`: uuid
- `category`: string
- `date_from`: date
- `date_to`: date

**Response:**
```json
{
  "expenses": [
    {
      "id": "uuid",
      "trip_id": "uuid",
      "category": "fuel" | "toll" | "maintenance" | "food" | "other",
      "amount": "number",
      "description": "string",
      "receipt_url": "string",
      "created_at": "datetime",
      "approved": boolean
    }
  ],
  "total_amount": "number"
}
```

### POST /expenses
Record a new expense.

**Request Body:**
```json
{
  "trip_id": "uuid",
  "category": "string",
  "amount": "number",
  "description": "string",
  "receipt_image": "base64_string"
}
```

---

## AI Agent Endpoints

### POST /ai/route-optimization
Get AI-powered route optimization.

**Request Body:**
```json
{
  "pickup_location": "string",
  "delivery_location": "string",
  "vehicle_type": "string",
  "preferences": {
    "avoid_tolls": boolean,
    "fastest_route": boolean,
    "fuel_efficient": boolean
  }
}
```

**Response:**
```json
{
  "optimized_route": {
    "waypoints": ["string"],
    "total_distance": "number",
    "estimated_time": "number",
    "estimated_fuel_cost": "number",
    "toll_cost": "number"
  },
  "alternative_routes": [
    {
      "distance": "number",
      "time": "number",
      "cost": "number",
      "description": "string"
    }
  ]
}
```

### POST /ai/driver-assignment
Get AI recommendation for driver assignment.

**Request Body:**
```json
{
  "trip_id": "uuid",
  "pickup_location": "string",
  "requirements": {
    "experience_level": "string",
    "vehicle_type": "string",
    "urgency": "string"
  }
}
```

**Response:**
```json
{
  "recommended_drivers": [
    {
      "driver_id": "uuid",
      "score": "number",
      "reasons": ["string"],
      "availability": "datetime",
      "distance_from_pickup": "number"
    }
  ]
}
```

### POST /ai/document-digitizer
Process and extract information from documents.

**Request Body:**
```json
{
  "document_type": "receipt" | "bill" | "permit",
  "image": "base64_string"
}
```

**Response:**
```json
{
  "extracted_data": {
    "amount": "number",
    "date": "date",
    "vendor": "string",
    "category": "string",
    "items": [
      {
        "description": "string",
        "quantity": "number",
        "price": "number"
      }
    ]
  },
  "confidence": "number"
}
```

---

## Analytics & Reporting

### GET /analytics/dashboard
Get dashboard metrics.

**Response:**
```json
{
  "metrics": {
    "total_trips": "number",
    "active_trips": "number",
    "available_drivers": "number",
    "total_revenue": "number",
    "monthly_profit": "number"
  },
  "trends": {
    "revenue_trend": [
      {"date": "date", "amount": "number"}
    ],
    "trip_volume": [
      {"date": "date", "count": "number"}
    ]
  }
}
```

### GET /analytics/performance
Get performance analytics.

**Query Parameters:**
- `period`: "week" | "month" | "quarter"
- `driver_id`: uuid (optional)

**Response:**
```json
{
  "performance": {
    "driver_efficiency": [
      {
        "driver_id": "uuid",
        "trips_completed": "number",
        "avg_rating": "number",
        "on_time_percentage": "number"
      }
    ],
    "vehicle_utilization": [
      {
        "vehicle_id": "uuid",
        "utilization_percentage": "number",
        "fuel_efficiency": "number"
      }
    ],
    "route_efficiency": {
      "avg_time_saved": "number",
      "fuel_cost_reduction": "number"
    }
  }
}
```

---

## WhatsApp Integration

### POST /whatsapp/webhook
Webhook endpoint for WhatsApp messages.

**Request Body:**
```json
{
  "from": "phone_number",
  "message": "string",
  "message_type": "text" | "image" | "location",
  "timestamp": "datetime"
}
```

### POST /whatsapp/send-message
Send message via WhatsApp.

**Request Body:**
```json
{
  "to": "phone_number",
  "message": "string",
  "type": "text" | "template"
}
```

---

## Error Responses

All endpoints may return these error responses:

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "Invalid input data",
  "details": {
    "field": "error description"
  }
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
  "error": "Forbidden",
  "message": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```

---

## Rate Limiting

API requests are limited to:
- 100 requests per minute per user
- 1000 requests per hour per user

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

---

## Webhook Events

The system can send webhook notifications for various events:

### Trip Status Changes
```json
{
  "event": "trip.status_changed",
  "data": {
    "trip_id": "uuid",
    "status": "string",
    "timestamp": "datetime"
  }
}
```

### Driver Availability Changes
```json
{
  "event": "driver.availability_changed",
  "data": {
    "driver_id": "uuid",
    "is_available": boolean,
    "location": "string",
    "timestamp": "datetime"
  }
}
```
