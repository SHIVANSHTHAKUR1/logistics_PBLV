from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import Dict, List, Optional, Any
from uuid import UUID
import sys
import os

# Dynamic agent loading function
def load_agents():
    """Dynamically load AI agents with proper path handling"""
    import importlib.util
    import sys
    import os
    
    # Get the backend directory
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    agents_base = os.path.join(backend_dir, 'agents')
    
    agents = {}
    agent_files = {
        'TripIntelligenceAgent': 'trip_intelligence.py',
        'AvailabilityAgent': 'availability_agent.py', 
        'RouteOptimizationAgent': 'route_optimization.py',
        'DocumentDigitizerAgent': 'document_digitizer.py'
    }
    
    for agent_class, filename in agent_files.items():
        try:
            agent_path = os.path.join(agents_base, filename)
            if os.path.exists(agent_path):
                spec = importlib.util.spec_from_file_location(filename[:-3], agent_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, agent_class):
                    agents[agent_class] = getattr(module, agent_class)
                    print(f"✅ Loaded {agent_class}")
                else:
                    print(f"⚠️ {agent_class} not found in {filename}")
            else:
                print(f"⚠️ Agent file not found: {agent_path}")
        except Exception as e:
            print(f"❌ Failed to load {agent_class}: {e}")
    
    return agents

# Load agents
try:
    loaded_agents = load_agents()
    AGENTS_AVAILABLE = len(loaded_agents) > 0
    
    if AGENTS_AVAILABLE:
        print(f"🎉 Successfully loaded {len(loaded_agents)} AI agents")
        TripIntelligenceAgent = loaded_agents.get('TripIntelligenceAgent')
        AvailabilityAgent = loaded_agents.get('AvailabilityAgent')
        RouteOptimizationAgent = loaded_agents.get('RouteOptimizationAgent')
        DocumentDigitizerAgent = loaded_agents.get('DocumentDigitizerAgent')
    else:
        print("⚠️ No AI agents could be loaded")
        
except Exception as e:
    print(f"❌ Agent loading failed: {e}")
    AGENTS_AVAILABLE = False

router = APIRouter(prefix="/ai", tags=["ai-agents"])

# Initialize agents if available
if AGENTS_AVAILABLE:
    # Only initialize agents that were successfully loaded
    trip_intelligence = TripIntelligenceAgent() if TripIntelligenceAgent else None
    availability_agent = AvailabilityAgent() if AvailabilityAgent else None
    route_agent = RouteOptimizationAgent() if RouteOptimizationAgent else None
    document_agent = DocumentDigitizerAgent() if DocumentDigitizerAgent else None
    
    print(f"🚀 Initialized available agents:")
    if trip_intelligence: print("  - Trip Intelligence Agent")
    if availability_agent: print("  - Availability Agent") 
    if route_agent: print("  - Route Optimization Agent")
    if document_agent: print("  - Document Digitizer Agent")
else:
    trip_intelligence = None
    availability_agent = None
    route_agent = None
    document_agent = None

@router.post("/trips/create-intelligent")
async def create_intelligent_trip(trip_request: Dict[str, Any]):
    """
    Create a trip with full AI assistance - route optimization, driver assignment, cost estimation
    """
    if not AGENTS_AVAILABLE or not trip_intelligence:
        raise HTTPException(status_code=503, detail="AI agents not available")
    
    try:
        result = await trip_intelligence.create_intelligent_trip(trip_request)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Trip creation failed"))
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI trip creation failed: {str(e)}")

@router.get("/trips/{trip_id}/monitor")
async def monitor_trip_progress(trip_id: UUID):
    """
    Monitor active trip and provide real-time intelligence
    """
    if not AGENTS_AVAILABLE or not trip_intelligence:
        raise HTTPException(status_code=503, detail="AI agents not available")
    
    try:
        result = await trip_intelligence.monitor_trip_progress(trip_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail=result.get("error", "Trip monitoring failed"))
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trip monitoring failed: {str(e)}")

@router.post("/trips/{trip_id}/process-document")
async def process_trip_document(
    trip_id: UUID,
    document_type: str = Form(...),
    document: UploadFile = File(...)
):
    """
    Process trip-related documents (receipts, freight bills, etc.) using OCR
    """
    try:
        # Read the uploaded file
        image_data = await document.read()
        
        result = await trip_intelligence.process_trip_document(
            trip_id=trip_id,
            document_type=document_type,
            image_data=image_data
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Document processing failed"))
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document processing failed: {str(e)}")

@router.get("/drivers/{driver_id}/optimize-schedule")
async def optimize_driver_schedule(
    driver_id: UUID,
    time_horizon_days: int = 7
):
    """
    Optimize driver's schedule for the next few days using AI
    """
    try:
        result = await trip_intelligence.optimize_driver_schedule(
            driver_id=driver_id,
            time_horizon_days=time_horizon_days
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail=result.get("error", "Schedule optimization failed"))
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Schedule optimization failed: {str(e)}")

@router.post("/analytics/trips")
async def generate_trip_analytics(filters: Optional[Dict[str, Any]] = None):
    """
    Generate comprehensive trip analytics and insights using AI
    """
    try:
        result = await trip_intelligence.generate_trip_analytics(filters)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Analytics generation failed"))
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics generation failed: {str(e)}")

@router.post("/drivers/find-optimal")
async def find_optimal_driver(
    pickup_location: str,
    trip_details: Dict[str, Any],
    preferences: Optional[Dict[str, Any]] = None
):
    """
    Find the optimal driver for a trip using AI matching
    """
    try:
        result = await availability_agent.find_best_driver_for_trip(
            trip_id=None,
            pickup_location=pickup_location,
            preferences=preferences
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="No suitable driver found")
        
        return {
            "success": True,
            "optimal_driver": result,
            "selection_timestamp": trip_intelligence.datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Driver optimization failed: {str(e)}")

@router.post("/routes/optimize")
async def optimize_route(
    origin: str,
    destination: str,
    constraints: Optional[Dict[str, Any]] = None
):
    """
    Optimize a single route using AI route planning
    """
    try:
        result = await route_agent.optimize_single_route(
            origin=origin,
            destination=destination,
            constraints=constraints
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Route optimization failed"))
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Route optimization failed: {str(e)}")

@router.post("/routes/optimize-multi-stop")
async def optimize_multi_stop_route(
    stops: List[str],
    constraints: Optional[Dict[str, Any]] = None
):
    """
    Optimize a route with multiple stops using AI (TSP optimization)
    """
    try:
        result = await route_agent.optimize_multi_stop_route(
            stops=stops,
            constraints=constraints
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Multi-stop optimization failed"))
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Multi-stop optimization failed: {str(e)}")

@router.post("/routes/departure-time")
async def suggest_departure_time(
    origin: str,
    destination: str,
    preferred_arrival_time: Optional[str] = None
):
    """
    Suggest optimal departure time considering traffic patterns
    """
    try:
        result = await route_agent.suggest_optimal_departure_time(
            origin=origin,
            destination=destination,
            preferred_arrival_time=preferred_arrival_time
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Departure time optimization failed"))
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Departure time optimization failed: {str(e)}")

@router.post("/routes/fuel-optimization")
async def calculate_fuel_optimization(
    route_info: Dict[str, Any],
    vehicle_specs: Optional[Dict[str, Any]] = None
):
    """
    Calculate fuel optimization strategies for a route
    """
    try:
        result = await route_agent.calculate_fuel_optimization(
            route_info=route_info,
            vehicle_specs=vehicle_specs
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Fuel optimization failed"))
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fuel optimization failed: {str(e)}")

@router.post("/documents/extract-receipt")
async def extract_receipt_details(document: UploadFile = File(...)):
    """
    Extract details from expense receipts using OCR
    """
    try:
        image_data = await document.read()
        
        result = await document_agent.process_expense_receipt(image_data)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Receipt extraction failed"))
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Receipt extraction failed: {str(e)}")

@router.post("/documents/extract-freight-bill")
async def extract_freight_bill(document: UploadFile = File(...)):
    """
    Extract details from freight bills using OCR
    """
    try:
        image_data = await document.read()
        
        result = await document_agent.extract_freight_bill_details(image_data)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Freight bill extraction failed"))
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Freight bill extraction failed: {str(e)}")

@router.post("/drivers/availability/update")
async def update_driver_availability_ai(
    phone_number: str,
    status_message: str,
    location: Optional[str] = None
):
    """
    Update driver availability using AI to parse natural language status
    """
    try:
        result = await availability_agent.update_driver_availability(
            phone_number=phone_number,
            status=status_message,
            location=location
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message", "Availability update failed"))
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Availability update failed: {str(e)}")

@router.get("/drivers/available")
async def get_available_drivers_ai(
    location: Optional[str] = None,
    radius_km: float = 50.0,
    min_rating: float = 3.0
):
    """
    Get available drivers with AI-powered filtering and ranking
    """
    try:
        result = await availability_agent.get_available_drivers(
            location=location,
            radius_km=radius_km,
            min_rating=min_rating
        )
        
        return {
            "success": True,
            "available_drivers": result,
            "count": len(result),
            "search_criteria": {
                "location": location,
                "radius_km": radius_km,
                "min_rating": min_rating
            },
            "timestamp": trip_intelligence.datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Driver search failed: {str(e)}")

@router.post("/drivers/{driver_id}/predict-acceptance")
async def predict_driver_acceptance(
    driver_id: UUID,
    trip_details: Dict[str, Any]
):
    """
    Predict likelihood of driver accepting a trip using AI analysis
    """
    try:
        result = await availability_agent.predict_driver_acceptance(
            driver_id=driver_id,
            trip_details=trip_details
        )
        
        return {
            "success": True,
            "prediction": result,
            "trip_details": trip_details,
            "analysis_timestamp": trip_intelligence.datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Acceptance prediction failed: {str(e)}")

@router.get("/health")
async def ai_agents_health():
    """
    Health check for AI agents
    """
    return {
        "status": "healthy",
        "agents": {
            "trip_intelligence": trip_intelligence.name,
            "availability_agent": availability_agent.name,
            "route_optimization": route_agent.name,
            "document_digitizer": document_agent.name
        },
        "capabilities": [
            "Intelligent trip creation",
            "Real-time trip monitoring",
            "OCR document processing",
            "Route optimization",
            "Driver matching",
            "Schedule optimization",
            "Predictive analytics"
        ],
        "timestamp": trip_intelligence.datetime.utcnow().isoformat()
    }

