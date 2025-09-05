from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
from .routes import auth, drivers, trips, expenses, whatsapp, ai_agents
from .routes_sqlite import router as sqlite_router
from .seed_db import init_db, seed_from_csvs
from .db import SessionLocal
import os

app = FastAPI(
    title="Logistics Automation API",
    description="AI-powered logistics management system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
    ],  # React/Vite dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(drivers.router, prefix="/api/v1", tags=["drivers"])
app.include_router(trips.router, prefix="/api/v1", tags=["trips"])
app.include_router(expenses.router, prefix="/api/v1", tags=["expenses"])
app.include_router(whatsapp.router, prefix="/api/v1", tags=["whatsapp"])
app.include_router(ai_agents.router, prefix="/api/v1", tags=["ai-agents"])
app.include_router(sqlite_router, prefix="/api/v1", tags=["sqlite-api"])  # expose under /api/v1
app.include_router(sqlite_router, tags=["sqlite-api-root"])  # also at root for current frontend baseURL

@app.get("/")
async def root():
    return {"message": "Logistics Automation API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "logistics-api"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


@app.on_event("startup")
def startup_seed():
    # Initialize tables and seed from CSVs on startup
    init_db()
    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        db = SessionLocal()
        seed_from_csvs(db, project_root)
    except Exception as e:
        print(f"[startup] Seed warning: {e}")
    finally:
        try:
            db.close()
        except Exception:
            pass
