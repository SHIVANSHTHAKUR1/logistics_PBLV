# Getting Started Guide - Backend Development (Sanjit Palial)

## 🎯 Your Role: Backend Lead & AI/ML Specialist

You'll be responsible for building the FastAPI backend, implementing AI agents using LangChain, managing the database, and creating the WhatsApp bot integration.

---

## 🛠️ Development Environment Setup

### Step 1: Install Required Software
```bash
# Install Python 3.9+ from python.org
# Verify installation
python --version
# Should show Python 3.9 or higher

# Install Git
# Download from git-scm.com and install

# Install VS Code
# Download from code.visualstudio.com
```

### Step 2: Install VS Code Extensions
- Python (Microsoft)
- Python Docstring Generator
- Thunder Client (for API testing)
- GitLens (for Git integration)

### Step 3: Clone and Setup Project
```bash
# Navigate to your project folder
cd "c:\Users\shiva\OneDrive\Desktop\College\New folder"

# Create virtual environment
python -m venv logistics_env

# Activate virtual environment (Windows)
logistics_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file for environment variables
# Copy from .env.example and fill in your values
```

---

## 📁 Your Folder Structure

Create these folders in the `src/` directory:
```
src/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── database.py          # Database connection
│   │   ├── models/              # Database models
│   │   ├── routes/              # API endpoints
│   │   ├── services/            # Business logic
│   │   └── utils/               # Helper functions
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── availability_agent.py
│   │   ├── marketplace_agent.py
│   │   ├── dispatch_agent.py
│   │   ├── document_digitizer.py
│   │   └── reporting_agent.py
│   └── whatsapp/
│       ├── __init__.py
│       ├── bot_handler.py
│       └── message_processor.py
```

---

## 🗃️ Week 1 Tasks - Database & API Foundation

### Task 1: Database Schema Design
Create these tables in Supabase:

**Users Table:**
```sql
CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('owner', 'driver')),
    phone VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**Drivers Table:**
```sql
CREATE TABLE drivers (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    license_number VARCHAR(50),
    phone VARCHAR(20) NOT NULL,
    is_available BOOLEAN DEFAULT false,
    current_location VARCHAR(100),
    vehicle_id UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**Continue with Trips, Vehicles, Expenses, Loads tables...**

### Task 2: FastAPI Application Setup
Create `src/backend/app/main.py`:
```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn

app = FastAPI(
    title="Logistics Automation API",
    description="AI-powered logistics management system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

@app.get("/")
async def root():
    return {"message": "Logistics Automation API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "logistics-api"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

### Task 3: Database Connection
Create `src/backend/app/database.py`:
```python
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_db():
    return supabase
```

---

## 🤖 Week 2 Tasks - Authentication & CRUD Operations

### Task 1: User Authentication
Create `src/backend/app/routes/auth.py`:
```python
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
import bcrypt
import jwt
from datetime import datetime, timedelta

router = APIRouter()
security = HTTPBearer()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str
    phone: str = None

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register_user(user: UserCreate):
    # Implementation for user registration
    # Hash password, save to database
    pass

@router.post("/login")
async def login_user(credentials: UserLogin):
    # Implementation for user login
    # Verify credentials, return JWT token
    pass
```

### Task 2: CRUD Operations
Create routes for:
- `routes/drivers.py` - Driver management
- `routes/trips.py` - Trip operations
- `routes/expenses.py` - Expense tracking
- `routes/loads.py` - Load management

---

## 🔗 Week 3-4 Tasks - WhatsApp Integration

### Task 1: WhatsApp Webhook Handler
### Task 2: Message Processing Logic

---

## 🧠 Week 5-6 Tasks - AI Agents Development

### Task 1: Availability Agent
### Task 2: Document Digitizer Agent

---

## 🧪 Testing Your Work

### Unit Testing
Create `tests/test_backend.py`:
```python
import pytest
from fastapi.testclient import TestClient
from src.backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "logistics-api"}

def test_user_registration():
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "role": "owner"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/backend

# Run specific test file
pytest tests/test_backend.py
```

---

## 📚 Learning Resources

### FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

### LangChain
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Guide](https://langchain-ai.github.io/langgraph/)

### Supabase
- [Supabase Python Client](https://supabase.com/docs/reference/python)
- [Database Schema Design](https://supabase.com/docs/guides/database)

### WhatsApp Business API
- [WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [Twilio WhatsApp API](https://www.twilio.com/docs/whatsapp)

---

## 🤝 Collaboration Points

### With Shashank (Frontend):
- Define API contracts together
- Share authentication token format
- Coordinate real-time data updates
- Review API response formats

### With Shivansh (DevOps):
- Environment variables and configuration
- Database migration scripts
- API testing automation
- Deployment configuration

---

## 📊 Weekly Deliverables

**Week 1:**
- [ ] Database schema created in Supabase
- [ ] Basic FastAPI app running
- [ ] Authentication endpoints working
- [ ] API documentation started

**Week 2:**
- [ ] All CRUD operations implemented
- [ ] User management complete
- [ ] Basic tests written
- [ ] API endpoints documented

**Week 3:**
- [ ] WhatsApp webhook handler working
- [ ] Message processing logic implemented
- [ ] Driver availability system functional

**Week 4:**
- [ ] Trip assignment logic complete
- [ ] Expense logging through WhatsApp
- [ ] Integration with frontend APIs ready

Remember: Focus on getting basic functionality working first, then add complexity. Ask for help early if you get stuck!
