from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
from .routes import auth, drivers, trips, expenses, whatsapp, ai_agents

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

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(drivers.router, prefix="/api/v1", tags=["drivers"])
app.include_router(trips.router, prefix="/api/v1", tags=["trips"])
app.include_router(expenses.router, prefix="/api/v1", tags=["expenses"])
app.include_router(whatsapp.router, prefix="/api/v1", tags=["whatsapp"])
app.include_router(ai_agents.router, prefix="/api/v1", tags=["ai-agents"])

@app.get("/")
async def root():
    return {"message": "Logistics Automation API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "logistics-api"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
