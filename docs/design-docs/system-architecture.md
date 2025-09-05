# System Architecture - AI-Powered Logistics Management System

## Overview
This document outlines the system architecture for the AI-powered logistics management platform designed to automate and optimize logistics operations for small to medium-sized trucking businesses.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  Web Dashboard    │  WhatsApp Bot  │  Mobile App  │  API Clients │
│  (React.js)       │  (Chat Interface) │  (Future)   │  (External)  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY                                │
├─────────────────────────────────────────────────────────────────┤
│           FastAPI Application Server                            │
│  • Authentication & Authorization                              │
│  • Request Routing & Validation                               │
│  • Rate Limiting & Security                                   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SERVICE LAYER                                │
├─────────────────────────────────────────────────────────────────┤
│  AI Agents      │  WhatsApp     │  Trip         │  Analytics    │
│  • Route Opt    │  Integration  │  Management   │  Service      │
│  • Doc Digitizer│  • Message    │  • Assignment │  • Reporting  │
│  • Availability │    Processing │  • Tracking   │  • Insights   │
│  • Marketplace  │  • Bot Logic  │  • Optimization│  • KPIs      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DATA LAYER                                  │
├─────────────────────────────────────────────────────────────────┤
│  Supabase       │  File Storage │  Cache Layer  │  External APIs│
│  • PostgreSQL   │  • Images     │  • Redis      │  • Maps API   │
│  • Real-time    │  • Documents  │  • Sessions   │  • Weather    │
│  • Auth         │  • Receipts   │  • Temp Data  │  • Traffic    │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Component Architecture

### 1. Frontend Layer

#### Web Dashboard (React.js)
```
src/frontend/
├── components/
│   ├── layout/          # Navigation, sidebars, headers
│   ├── dashboard/       # Metrics cards, charts
│   ├── trips/          # Trip management UI
│   ├── drivers/        # Driver management UI
│   ├── vehicles/       # Vehicle tracking UI
│   └── analytics/      # Reports and analytics UI
├── pages/              # Page-level components
├── services/           # API integration layer
├── store/              # Redux state management
└── utils/              # Utility functions
```

**Key Features:**
- Responsive design for desktop and mobile
- Real-time updates via WebSocket
- Progressive Web App (PWA) capabilities
- Offline functionality for critical features

#### WhatsApp Integration
```
WhatsApp Bot Flow:
User Message → Meta Webhook → FastAPI → AI Processing → Response → WhatsApp API
```

**Supported Message Types:**
- Text commands
- Image uploads (receipts, documents)
- Location sharing
- Voice messages (future)

### 2. Backend API Layer

#### FastAPI Application Structure
```
src/backend/
├── app/
│   ├── main.py                 # Application entry point
│   ├── config.py              # Configuration management
│   ├── dependencies.py        # Dependency injection
│   └── middleware.py          # Custom middleware
├── routes/
│   ├── auth.py               # Authentication endpoints
│   ├── drivers.py            # Driver management
│   ├── trips.py              # Trip operations
│   ├── vehicles.py           # Vehicle management
│   ├── expenses.py           # Expense tracking
│   ├── analytics.py          # Analytics endpoints
│   └── whatsapp.py           # WhatsApp webhook
├── models/
│   ├── database.py           # Database models
│   ├── schemas.py            # Pydantic schemas
│   └── validators.py         # Data validation
├── services/
│   ├── auth_service.py       # Authentication logic
│   ├── trip_service.py       # Trip business logic
│   ├── notification_service.py # Notification handling
│   └── analytics_service.py  # Analytics processing
└── utils/
    ├── security.py           # Security utilities
    ├── email.py              # Email services
    └── helpers.py            # General utilities
```

### 3. AI Agents Architecture

#### Agent Framework (LangChain + LangGraph)
```
src/backend/agents/
├── base_agent.py              # Abstract base agent
├── availability_agent.py      # Driver availability management
├── route_optimizer_agent.py   # Route optimization
├── document_digitizer_agent.py # OCR and document processing
├── marketplace_agent.py       # Load matching
└── analytics_agent.py         # Business intelligence
```

#### AI Agent Workflow
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  Agent Router   │───▶│  Specific Agent │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Context DB    │◀───│  Memory Store   │◀───│  Action Engine  │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 4. Database Schema

#### Core Entities
```sql
-- Users (Owners and Drivers)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Drivers
CREATE TABLE drivers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    license_number VARCHAR(50),
    phone VARCHAR(20) NOT NULL,
    is_available BOOLEAN DEFAULT false,
    current_location POINT,
    vehicle_id UUID,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Vehicles
CREATE TABLE vehicles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID REFERENCES users(id),
    registration_number VARCHAR(20) UNIQUE NOT NULL,
    type VARCHAR(50) NOT NULL,
    capacity_weight DECIMAL(10,2),
    capacity_volume DECIMAL(10,2),
    fuel_type VARCHAR(20),
    is_available BOOLEAN DEFAULT true,
    current_location POINT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Trips
CREATE TABLE trips (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID REFERENCES users(id),
    driver_id UUID REFERENCES drivers(id),
    vehicle_id UUID REFERENCES vehicles(id),
    pickup_location VARCHAR(255) NOT NULL,
    delivery_location VARCHAR(255) NOT NULL,
    pickup_datetime TIMESTAMP,
    delivery_datetime TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    load_details JSONB,
    route_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Expenses
CREATE TABLE expenses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trip_id UUID REFERENCES trips(id),
    driver_id UUID REFERENCES drivers(id),
    category VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    receipt_url VARCHAR(255),
    approved BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 5. Integration Architecture

#### External Service Integrations
```
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                            │
├─────────────────────────────────────────────────────────────────┤
│  WhatsApp API  │  Google Maps  │  Weather API │  Payment Gateway│
│  • Messaging   │  • Geocoding  │  • Conditions│  • Transactions │
│  • Media       │  • Routing    │  • Forecasts │  • Invoicing   │
│  • Webhooks    │  • Traffic    │  • Alerts    │  • Settlements │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   INTEGRATION LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│           API Adapters & Service Clients                       │
│  • Rate limiting and retry logic                              │
│  • Error handling and circuit breakers                        │
│  • Data transformation and validation                         │
│  • Authentication and security                                │
└─────────────────────────────────────────────────────────────────┘
```

### 6. Automation Layer (n8n)

#### Workflow Architecture
```
src/automation/
├── workflows/
│   ├── trip_assignment.json      # Automated trip assignment
│   ├── expense_processing.json   # Expense approval workflow
│   ├── driver_notifications.json # Driver status notifications
│   ├── daily_reports.json        # Automated reporting
│   └── maintenance_alerts.json   # Vehicle maintenance reminders
├── custom-nodes/
│   ├── logistics-api-node/       # Custom API integration
│   ├── whatsapp-node/           # WhatsApp integration
│   └── ai-agent-node/           # AI agent integration
└── credentials/
    ├── api-credentials.json      # Encrypted API keys
    └── webhook-configs.json      # Webhook configurations
```

#### Workflow Triggers
- **Time-based**: Scheduled reports, maintenance alerts
- **Event-based**: Trip status changes, driver availability
- **Webhook-based**: External system integrations
- **Manual**: User-initiated processes

### 7. Security Architecture

#### Authentication & Authorization
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Login    │───▶│  JWT Token      │───▶│  Role-Based     │
│                 │    │  Generation     │    │  Access Control │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Token Storage  │◀───│  Token          │───▶│  API Endpoint   │
│  (HTTP-only     │    │  Validation     │    │  Protection     │
│   cookies)      │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

#### Security Layers
1. **Network Security**: HTTPS, firewall rules, VPN access
2. **Application Security**: Input validation, SQL injection prevention
3. **Data Security**: Encryption at rest and in transit
4. **Access Control**: Role-based permissions, API rate limiting
5. **Monitoring**: Security event logging, anomaly detection

### 8. Deployment Architecture

#### Production Environment
```
┌─────────────────────────────────────────────────────────────────┐
│                    PRODUCTION DEPLOYMENT                        │
├─────────────────────────────────────────────────────────────────┤
│                    Load Balancer (Nginx)                       │
├─────────────────────────────────────────────────────────────────┤
│  Frontend         │  Backend API      │  n8n Automation        │
│  (React Build)    │  (FastAPI)        │  (Workflow Engine)     │
│  • Static Assets  │  • API Endpoints  │  • Scheduled Tasks     │
│  • PWA Shell     │  • WebSocket      │  • Event Processing    │
└─────────────────────────────────────────────────────────────────┘
│                    Database Cluster                            │
│  Primary DB       │  Read Replicas    │  Backup Storage        │
│  (Supabase)       │  (Performance)    │  (Disaster Recovery)   │
└─────────────────────────────────────────────────────────────────┘
```

#### Container Architecture (Docker)
```yaml
services:
  frontend:
    image: logistics-frontend:latest
    ports: ["3000:3000"]
    
  backend:
    image: logistics-backend:latest
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - WHATSAPP_TOKEN=${WHATSAPP_TOKEN}
    
  n8n:
    image: n8nio/n8n:latest
    ports: ["5678:5678"]
    volumes:
      - ./n8n_data:/home/node/.n8n
    
  nginx:
    image: nginx:alpine
    ports: ["80:80", "443:443"]
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

### 9. Scalability Considerations

#### Horizontal Scaling Points
1. **API Layer**: Multiple FastAPI instances behind load balancer
2. **Database**: Read replicas for query distribution
3. **File Storage**: CDN for static assets and media files
4. **Background Tasks**: Queue-based processing with workers
5. **Caching**: Redis cluster for session and data caching

#### Performance Optimization
- **Database Indexing**: Optimized queries for frequent operations
- **API Caching**: Response caching for expensive operations
- **Image Optimization**: Compressed images and lazy loading
- **Code Splitting**: Lazy-loaded React components
- **CDN Integration**: Global content distribution

### 10. Monitoring & Observability

#### System Monitoring
```
┌─────────────────────────────────────────────────────────────────┐
│                    MONITORING STACK                             │
├─────────────────────────────────────────────────────────────────┤
│  Application     │  Infrastructure  │  Business       │  User   │
│  Monitoring      │  Monitoring      │  Metrics        │  Analytics│
│  • API Response  │  • Server Health │  • Trip Volume  │  • Usage  │
│  • Error Rates   │  • Database      │  • Revenue      │  • Behavior│
│  • Performance   │  • Memory/CPU    │  • Efficiency   │  • Feedback│
└─────────────────────────────────────────────────────────────────┘
```

#### Alerting System
- **Critical Alerts**: System downtime, database failures
- **Warning Alerts**: High error rates, performance degradation
- **Business Alerts**: Unusual trip patterns, revenue anomalies
- **Maintenance Alerts**: Scheduled maintenance reminders

This architecture provides a scalable, maintainable, and secure foundation for the AI-powered logistics management system, with clear separation of concerns and well-defined integration points between components.
