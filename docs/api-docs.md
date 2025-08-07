# API Documentation - Logistics Automation Platform

## Base URL
```
Development: http://localhost:8000/api/v1
Production: https://logistics-platform.com/api/v1
```

## Authentication
All API endpoints require authentication using Bearer tokens.

```http
Authorization: Bearer <your_jwt_token>
```

## Core Endpoints

### Authentication

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "owner@example.com",
  "password": "password123"
}
```

#### Register
```http
POST /auth/register
Content-Type: application/json

{
  "username": "newowner@example.com",
  "password": "password123",
  "role": "owner",
  "phone": "+91XXXXXXXXXX"
}
```

### Driver Management

#### Get All Drivers
```http
GET /drivers/
```

#### Add New Driver
```http
POST /drivers/
Content-Type: application/json

{
  "name": "Driver Name",
  "phone": "+91XXXXXXXXXX",
  "license_number": "DL123456789",
  "vehicle_id": "vehicle_uuid"
}
```

#### Update Driver Availability
```http
PUT /drivers/{driver_id}/availability
Content-Type: application/json

{
  "is_available": true,
  "current_location": "City Name"
}
```

### Trip Management

#### Create New Trip
```http
POST /trips/
Content-Type: application/json

{
  "load_id": "load_uuid",
  "driver_id": "driver_uuid",
  "pickup_location": "Delhi",
  "delivery_location": "Mumbai",
  "freight_amount": 50000,
  "pickup_date": "2025-01-20"
}
```

#### Get Trip Details
```http
GET /trips/{trip_id}
```

#### Update Trip Status
```http
PUT /trips/{trip_id}/status
Content-Type: application/json

{
  "status": "in_transit",
  "location": "Current Location",
  "timestamp": "2025-01-20T10:30:00Z"
}
```

### Load Management

#### Get Available Loads
```http
GET /loads/?status=available&location=Delhi
```

#### Create Load Request
```http
POST /loads/
Content-Type: application/json

{
  "pickup_location": "Delhi",
  "delivery_location": "Mumbai",
  "cargo_type": "General",
  "weight": 10000,
  "freight_amount": 45000,
  "pickup_date": "2025-01-25"
}
```

### Expense Management

#### Log Expense
```http
POST /expenses/
Content-Type: application/json

{
  "trip_id": "trip_uuid",
  "expense_type": "fuel",
  "amount": 5000,
  "description": "Fuel at Highway Pump",
  "receipt_image": "base64_image_data"
}
```

#### Get Trip Expenses
```http
GET /expenses/?trip_id={trip_id}
```

### Financial Reports

#### Get Profit/Loss Report
```http
GET /reports/pnl?start_date=2025-01-01&end_date=2025-01-31
```

#### Generate Weekly Report
```http
POST /reports/weekly
Content-Type: application/json

{
  "week_start": "2025-01-20",
  "format": "excel"
}
```

### WhatsApp Bot Endpoints

#### Process WhatsApp Message
```http
POST /whatsapp/webhook
Content-Type: application/json

{
  "from": "+91XXXXXXXXXX",
  "message": "FREE",
  "timestamp": "2025-01-20T10:30:00Z"
}
```

#### Send WhatsApp Message
```http
POST /whatsapp/send
Content-Type: application/json

{
  "to": "+91XXXXXXXXXX",
  "message": "New trip assigned: Delhi to Mumbai",
  "trip_id": "trip_uuid"
}
```

## Agent System Endpoints

### Document Processing
```http
POST /agents/document-digitizer
Content-Type: multipart/form-data

{
  "image": "uploaded_file",
  "trip_id": "trip_uuid"
}
```

### Load Matching
```http
GET /agents/marketplace/matches?driver_location=Delhi&capacity=10000
```

### Automated Dispatch
```http
POST /agents/dispatch/broadcast
Content-Type: application/json

{
  "trip_id": "trip_uuid",
  "available_drivers": ["driver1_uuid", "driver2_uuid"]
}
```

## Response Formats

### Success Response
```json
{
  "status": "success",
  "data": {
    // Response data
  },
  "message": "Operation completed successfully"
}
```

### Error Response
```json
{
  "status": "error",
  "error_code": "VALIDATION_ERROR",
  "message": "Invalid input data",
  "details": {
    "field": "Error description"
  }
}
```

## Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Rate Limiting
- 100 requests per minute per user
- 1000 requests per hour per user
- Higher limits available for premium accounts
