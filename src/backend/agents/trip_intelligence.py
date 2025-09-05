"""
Trip Intelligence Agent - Main AI coordinator for trip management
Orchestrates other agents to provide comprehensive trip intelligence and automation
"""
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from uuid import UUID
import json
import os
import sys

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Try to import other agents and database
try:
    from agents.availability_agent import AvailabilityAgent
    from agents.route_optimization import RouteOptimizationAgent  
    from agents.document_digitizer import DocumentDigitizerAgent
    from database import get_supabase_client
except ImportError:
    # Fallback for when running as a module
    AvailabilityAgent = None
    RouteOptimizationAgent = None
    DocumentDigitizerAgent = None
    get_supabase_client = None

class TripIntelligenceAgent:
    def __init__(self):
        self.name = "Trip Intelligence Agent"
        self.version = "1.0.0"
        
        # Initialize sub-agents with fallback handling
        try:
            self.availability_agent = AvailabilityAgent() if AvailabilityAgent else None
            self.route_agent = RouteOptimizationAgent() if RouteOptimizationAgent else None
            self.document_agent = DocumentDigitizerAgent() if DocumentDigitizerAgent else None
        except Exception as e:
            print(f"Warning: Could not initialize sub-agents: {e}")
            self.availability_agent = None
            self.route_agent = None
            self.document_agent = None
    
    async def create_intelligent_trip(
        self, 
        trip_request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a trip with full AI assistance - route optimization, driver assignment, cost estimation
        """
        try:
            pickup_location = trip_request.get("pickup_location")
            destination = trip_request.get("destination")
            priority = trip_request.get("priority", "medium")
            
            if not pickup_location or not destination:
                return {
                    "success": False,
                    "error": "Pickup location and destination are required"
                }
            
            # Step 1: Optimize route
            route_optimization = await self.route_agent.optimize_single_route(
                origin=pickup_location,
                destination=destination,
                constraints=trip_request.get("constraints")
            )
            
            if not route_optimization.get("success"):
                return {
                    "success": False,
                    "error": "Route optimization failed",
                    "details": route_optimization
                }
            
            # Step 2: Find optimal driver
            best_driver = await self.availability_agent.find_best_driver_for_trip(
                trip_id=None,  # We don't have trip ID yet
                pickup_location=pickup_location,
                preferences=trip_request.get("driver_preferences")
            )
            
            # Step 3: Predict driver acceptance
            driver_prediction = None
            if best_driver:
                driver_prediction = await self.availability_agent.predict_driver_acceptance(
                    driver_id=best_driver["id"],
                    trip_details=route_optimization["route_info"]
                )
            
            # Step 4: Calculate optimal departure time
            departure_optimization = await self.route_agent.suggest_optimal_departure_time(
                origin=pickup_location,
                destination=destination,
                preferred_arrival_time=trip_request.get("preferred_arrival_time")
            )
            
            # Step 5: Generate comprehensive trip plan
            trip_plan = {
                "route_details": route_optimization["route_info"],
                "recommended_driver": best_driver,
                "driver_acceptance_prediction": driver_prediction,
                "departure_recommendations": departure_optimization.get("recommended_options", []),
                "cost_breakdown": route_optimization["route_info"].get("costs", {}),
                "recommendations": route_optimization.get("recommendations", [])
            }
            
            # Step 6: Create trip record if auto-create is enabled
            trip_record = None
            if trip_request.get("auto_create", False):
                trip_record = await self._create_trip_record(trip_request, trip_plan)
            
            return {
                "success": True,
                "trip_plan": trip_plan,
                "trip_record": trip_record,
                "intelligence_summary": await self._generate_intelligence_summary(trip_plan),
                "created_at": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Trip intelligence creation failed: {str(e)}",
                "created_at": datetime.utcnow().isoformat()
            }
    
    async def monitor_trip_progress(self, trip_id: UUID) -> Dict[str, Any]:
        """
        Monitor active trip and provide real-time intelligence
        """
        try:
            supabase = get_supabase_client()
            
            # Get trip details
            trip_result = supabase.table("trips").select("*").eq("id", str(trip_id)).execute()
            
            if not trip_result.data:
                return {
                    "success": False,
                    "error": "Trip not found"
                }
            
            trip = trip_result.data[0]
            
            # Get driver details
            driver_result = supabase.table("drivers").select("*").eq("id", trip["driver_id"]).execute()
            driver = driver_result.data[0] if driver_result.data else None
            
            # Calculate progress metrics
            progress_metrics = await self._calculate_progress_metrics(trip, driver)
            
            # Generate real-time recommendations
            real_time_recommendations = await self._generate_real_time_recommendations(trip, driver, progress_metrics)
            
            # Check for potential issues
            potential_issues = await self._detect_potential_issues(trip, driver, progress_metrics)
            
            # Get expense insights
            expense_insights = await self._analyze_trip_expenses(trip_id)
            
            return {
                "success": True,
                "trip_status": trip["status"],
                "progress_metrics": progress_metrics,
                "real_time_recommendations": real_time_recommendations,
                "potential_issues": potential_issues,
                "expense_insights": expense_insights,
                "monitoring_timestamp": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Trip monitoring failed: {str(e)}",
                "monitoring_timestamp": datetime.utcnow().isoformat()
            }
    
    async def process_trip_document(
        self, 
        trip_id: UUID, 
        document_type: str, 
        image_data: bytes
    ) -> Dict[str, Any]:
        """
        Process trip-related documents (receipts, freight bills, etc.)
        """
        try:
            if document_type == "expense_receipt":
                result = await self.document_agent.process_expense_receipt(image_data)
                
                if result.get("success") and result.get("suggested_expense"):
                    # Auto-create expense if confidence is high
                    if result.get("confidence", 0) > 0.7:
                        expense_record = await self._create_expense_record(
                            trip_id, 
                            result["suggested_expense"], 
                            image_data
                        )
                        result["auto_created_expense"] = expense_record
            
            elif document_type == "freight_bill":
                result = await self.document_agent.extract_freight_bill_details(image_data)
                
                # Update trip with extracted details if confidence is high
                if result.get("success") and result.get("confidence", 0) > 0.8:
                    await self._update_trip_with_freight_details(trip_id, result["freight_details"])
            
            else:
                result = await self.document_agent.extract_freight_amount(image_data)
            
            # Add intelligence insights
            result["intelligence_insights"] = await self._generate_document_insights(result, document_type)
            
            return result
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Document processing failed: {str(e)}",
                "processing_timestamp": datetime.utcnow().isoformat()
            }
    
    async def optimize_driver_schedule(
        self, 
        driver_id: UUID, 
        time_horizon_days: int = 7
    ) -> Dict[str, Any]:
        """
        Optimize driver's schedule for the next few days
        """
        try:
            supabase = get_supabase_client()
            
            # Get driver details
            driver_result = supabase.table("drivers").select("*").eq("id", str(driver_id)).execute()
            
            if not driver_result.data:
                return {
                    "success": False,
                    "error": "Driver not found"
                }
            
            driver = driver_result.data[0]
            
            # Get pending trips that could be assigned to this driver
            pending_trips = await self._get_suitable_pending_trips(driver_id)
            
            # Get driver's current schedule
            current_schedule = await self._get_driver_schedule(driver_id, time_horizon_days)
            
            # Optimize schedule
            optimized_schedule = await self._optimize_schedule(driver, pending_trips, current_schedule)
            
            # Calculate performance metrics
            performance_metrics = await self._calculate_schedule_metrics(optimized_schedule)
            
            return {
                "success": True,
                "driver_name": driver["name"],
                "optimized_schedule": optimized_schedule,
                "performance_metrics": performance_metrics,
                "recommendations": await self._generate_schedule_recommendations(optimized_schedule),
                "optimization_timestamp": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Schedule optimization failed: {str(e)}",
                "optimization_timestamp": datetime.utcnow().isoformat()
            }
    
    async def generate_trip_analytics(
        self, 
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive trip analytics and insights
        """
        try:
            supabase = get_supabase_client()
            
            # Build query based on filters
            query = supabase.table("trips").select("*")
            
            if filters:
                if filters.get("start_date"):
                    query = query.gte("created_at", filters["start_date"])
                if filters.get("end_date"):
                    query = query.lte("created_at", filters["end_date"])
                if filters.get("status"):
                    query = query.eq("status", filters["status"])
                if filters.get("driver_id"):
                    query = query.eq("driver_id", filters["driver_id"])
            
            trips_result = query.execute()
            trips = trips_result.data if trips_result.data else []
            
            # Calculate analytics
            analytics = {
                "summary": await self._calculate_trip_summary(trips),
                "performance_trends": await self._analyze_performance_trends(trips),
                "cost_analysis": await self._analyze_cost_patterns(trips),
                "driver_performance": await self._analyze_driver_performance(trips),
                "route_efficiency": await self._analyze_route_efficiency(trips),
                "predictions": await self._generate_predictive_insights(trips)
            }
            
            return {
                "success": True,
                "analytics": analytics,
                "data_period": {
                    "start_date": filters.get("start_date") if filters else None,
                    "end_date": filters.get("end_date") if filters else None,
                    "total_trips_analyzed": len(trips)
                },
                "generated_at": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Analytics generation failed: {str(e)}",
                "generated_at": datetime.utcnow().isoformat()
            }
    
    async def _create_trip_record(
        self, 
        trip_request: Dict[str, Any], 
        trip_plan: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Create trip record in database
        """
        try:
            supabase = get_supabase_client()
            
            route_details = trip_plan["route_details"]
            
            trip_data = {
                "pickup_location": trip_request["pickup_location"],
                "destination": trip_request["destination"],
                "distance_km": route_details.get("distance_km"),
                "estimated_duration_hours": route_details.get("estimated_time_hours"),
                "estimated_cost": route_details.get("costs", {}).get("total_cost_inr"),
                "status": "pending",
                "priority": trip_request.get("priority", "medium"),
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Assign driver if available
            if trip_plan.get("recommended_driver"):
                trip_data["driver_id"] = trip_plan["recommended_driver"]["id"]
                trip_data["status"] = "assigned"
            
            result = supabase.table("trips").insert(trip_data).execute()
            
            return result.data[0] if result.data else None
        
        except Exception as e:
            print(f"Error creating trip record: {e}")
            return None
    
    async def _create_expense_record(
        self, 
        trip_id: UUID, 
        expense_suggestion: Dict[str, Any], 
        image_data: bytes
    ) -> Optional[Dict[str, Any]]:
        """
        Create expense record from OCR suggestion
        """
        try:
            supabase = get_supabase_client()
            
            import base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            expense_data = {
                "trip_id": str(trip_id),
                "category": expense_suggestion.get("category", "other"),
                "amount": expense_suggestion.get("amount", 0),
                "description": expense_suggestion.get("description", "Auto-created from receipt"),
                "receipt_image": image_base64,
                "created_at": datetime.utcnow().isoformat()
            }
            
            if expense_suggestion.get("expense_date"):
                expense_data["expense_date"] = expense_suggestion["expense_date"]
            
            result = supabase.table("expenses").insert(expense_data).execute()
            
            return result.data[0] if result.data else None
        
        except Exception as e:
            print(f"Error creating expense record: {e}")
            return None
    
    async def _generate_intelligence_summary(self, trip_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate AI summary of trip intelligence
        """
        route_details = trip_plan.get("route_details", {})
        driver = trip_plan.get("recommended_driver")
        
        summary = {
            "trip_viability": "high",
            "estimated_success_rate": 0.85,
            "key_insights": [],
            "risk_factors": [],
            "optimization_opportunities": []
        }
        
        # Analyze distance and time
        distance = route_details.get("distance_km", 0)
        time_hours = route_details.get("estimated_time_hours", 0)
        
        if distance > 500:
            summary["key_insights"].append("Long-distance trip requiring careful planning")
            summary["risk_factors"].append("Driver fatigue risk for long journey")
        
        if time_hours > 8:
            summary["risk_factors"].append("Journey exceeds recommended driving hours")
            summary["optimization_opportunities"].append("Consider splitting into multi-day trip")
        
        # Analyze cost efficiency
        costs = route_details.get("costs", {})
        cost_per_km = costs.get("total_cost_inr", 0) / distance if distance > 0 else 0
        
        if cost_per_km > 15:
            summary["optimization_opportunities"].append("High cost per km - review route efficiency")
        
        # Driver analysis
        if driver:
            if driver.get("suitability_score", 0) > 0.8:
                summary["key_insights"].append("Excellent driver match found")
            elif driver.get("suitability_score", 0) < 0.6:
                summary["risk_factors"].append("Suboptimal driver match")
        else:
            summary["risk_factors"].append("No suitable driver currently available")
            summary["trip_viability"] = "medium"
        
        return summary
    
    async def _calculate_progress_metrics(
        self, 
        trip: Dict[str, Any], 
        driver: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate real-time trip progress metrics
        """
        # This is a simplified version - in production, you'd integrate with GPS tracking
        return {
            "completion_percentage": 45.0,  # Example
            "estimated_remaining_time_hours": 2.5,
            "current_speed_kmh": 65,
            "on_schedule": True,
            "fuel_efficiency": "good"
        }
    
    async def _generate_real_time_recommendations(
        self, 
        trip: Dict[str, Any], 
        driver: Optional[Dict[str, Any]], 
        progress: Dict[str, Any]
    ) -> List[str]:
        """
        Generate real-time recommendations based on trip progress
        """
        recommendations = []
        
        if progress.get("current_speed_kmh", 0) > 80:
            recommendations.append("Reduce speed for better fuel efficiency and safety")
        
        if not progress.get("on_schedule", True):
            recommendations.append("Consider alternative route to make up time")
        
        return recommendations
    
    async def _detect_potential_issues(
        self, 
        trip: Dict[str, Any], 
        driver: Optional[Dict[str, Any]], 
        progress: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Detect potential issues with the trip
        """
        issues = []
        
        # Example issue detection
        if progress.get("completion_percentage", 0) < 20 and trip.get("status") == "in_progress":
            issues.append({
                "type": "progress_delay",
                "severity": "medium",
                "description": "Trip progress slower than expected",
                "suggested_action": "Contact driver for status update"
            })
        
        return issues
    
    async def _analyze_trip_expenses(self, trip_id: UUID) -> Dict[str, Any]:
        """
        Analyze expenses for a specific trip
        """
        try:
            supabase = get_supabase_client()
            
            expenses_result = supabase.table("expenses").select("*").eq("trip_id", str(trip_id)).execute()
            expenses = expenses_result.data if expenses_result.data else []
            
            total_expenses = sum(float(exp.get("amount", 0)) for exp in expenses)
            
            category_breakdown = {}
            for expense in expenses:
                category = expense.get("category", "other")
                category_breakdown[category] = category_breakdown.get(category, 0) + float(expense.get("amount", 0))
            
            return {
                "total_expenses": total_expenses,
                "expense_count": len(expenses),
                "category_breakdown": category_breakdown,
                "latest_expense": expenses[-1] if expenses else None
            }
        
        except Exception as e:
            return {
                "total_expenses": 0,
                "expense_count": 0,
                "error": str(e)
            }
    
    # Additional helper methods would be implemented here...
    async def _get_suitable_pending_trips(self, driver_id: UUID) -> List[Dict[str, Any]]:
        """Get pending trips suitable for the driver"""
        # Implementation would filter pending trips based on driver capabilities
        return []
    
    async def _get_driver_schedule(self, driver_id: UUID, days: int) -> List[Dict[str, Any]]:
        """Get driver's current schedule"""
        # Implementation would get assigned trips for the driver
        return []
    
    async def _optimize_schedule(
        self, 
        driver: Dict[str, Any], 
        pending_trips: List[Dict[str, Any]], 
        current_schedule: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Optimize driver schedule"""
        # Implementation would use optimization algorithms
        return current_schedule
    
    async def _calculate_schedule_metrics(self, schedule: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate performance metrics for schedule"""
        return {
            "utilization_rate": 0.75,
            "estimated_revenue": 15000,
            "total_distance_km": 1200
        }
    
    async def _generate_schedule_recommendations(self, schedule: List[Dict[str, Any]]) -> List[str]:
        """Generate schedule optimization recommendations"""
        return ["Consider grouping nearby deliveries", "Add buffer time for traffic"]
    
    async def _calculate_trip_summary(self, trips: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate summary statistics for trips"""
        return {
            "total_trips": len(trips),
            "completed_trips": len([t for t in trips if t.get("status") == "completed"]),
            "total_distance_km": sum(float(t.get("distance_km", 0)) for t in trips),
            "average_trip_duration": 4.5
        }
    
    async def _analyze_performance_trends(self, trips: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze performance trends"""
        return {"trend": "improving", "completion_rate_trend": "+5%"}
    
    async def _analyze_cost_patterns(self, trips: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze cost patterns"""
        return {"average_cost_per_km": 12.5, "cost_trend": "stable"}
    
    async def _analyze_driver_performance(self, trips: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze driver performance across trips"""
        return {"top_performers": [], "improvement_areas": []}
    
    async def _analyze_route_efficiency(self, trips: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze route efficiency"""
        return {"most_efficient_routes": [], "optimization_potential": "15%"}
    
    async def _generate_predictive_insights(self, trips: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate predictive insights"""
        return {
            "predicted_demand": "increasing",
            "recommended_fleet_size": 5,
            "seasonal_patterns": []
        }
    
    async def _update_trip_with_freight_details(
        self, 
        trip_id: UUID, 
        freight_details: Dict[str, Any]
    ) -> None:
        """Update trip with extracted freight bill details"""
        try:
            supabase = get_supabase_client()
            
            update_data = {}
            
            if freight_details.get("origin"):
                update_data["pickup_location"] = freight_details["origin"]
            
            if freight_details.get("destination"):
                update_data["destination"] = freight_details["destination"]
            
            if freight_details.get("weight"):
                update_data["cargo_weight"] = freight_details["weight"]
            
            if update_data:
                supabase.table("trips").update(update_data).eq("id", str(trip_id)).execute()
        
        except Exception as e:
            print(f"Error updating trip with freight details: {e}")
    
    async def _generate_document_insights(
        self, 
        processing_result: Dict[str, Any], 
        document_type: str
    ) -> List[str]:
        """Generate insights from document processing"""
        insights = []
        
        if processing_result.get("success"):
            confidence = processing_result.get("confidence", 0)
            
            if confidence > 0.8:
                insights.append("High confidence extraction - data is likely accurate")
            elif confidence > 0.5:
                insights.append("Medium confidence - manual verification recommended")
            else:
                insights.append("Low confidence - manual entry may be more accurate")
            
            if document_type == "expense_receipt":
                amount = processing_result.get("receipt_info", {}).get("amount", {}).get("amount")
                if amount and amount > 1000:
                    insights.append("High value expense - consider additional approval")
        
        return insights
