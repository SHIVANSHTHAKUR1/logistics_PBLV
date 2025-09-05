"""
Availability Agent - Manages driver availability and intelligent assignment
Uses AI to optimize driver-trip matching based on location, preferences, and history
"""
from typing import List, Dict, Optional, Any
from uuid import UUID
import asyncio
from datetime import datetime, timedelta
import math
import os
import sys

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from database import get_supabase_client
    from supabase import Client
except ImportError:
    # Fallback when imports fail
    get_supabase_client = None
    Client = None

class AvailabilityAgent:
    def __init__(self):
        self.name = "Availability Agent"
        self.version = "1.0.0"
    
    async def update_driver_availability(
        self, 
        phone_number: str, 
        status: str, 
        location: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Intelligently updates driver availability based on WhatsApp message
        """
        try:
            supabase = get_supabase_client()
            
            # Find driver by phone number
            driver_result = supabase.table("drivers").select("*").eq("phone", phone_number).execute()
            
            if not driver_result.data:
                return {
                    "success": False,
                    "message": "Driver not found",
                    "action": "register_driver"
                }
            
            driver = driver_result.data[0]
            driver_id = driver["id"]
            
            # Parse status from natural language
            is_available = self._parse_availability_status(status)
            
            # Update driver data
            update_data = {
                "is_available": is_available,
                "last_seen": datetime.utcnow().isoformat()
            }
            
            if location:
                update_data["current_location"] = location
            
            # Update in database
            result = supabase.table("drivers").update(update_data).eq("id", driver_id).execute()
            
            if result.data:
                # If driver became available, check for pending trips
                if is_available:
                    optimal_trip = await self._find_optimal_trip_for_driver(driver_id, supabase)
                    if optimal_trip:
                        return {
                            "success": True,
                            "message": f"Status updated to available. New trip opportunity found!",
                            "driver": result.data[0],
                            "suggested_trip": optimal_trip,
                            "action": "trip_suggestion"
                        }
                
                return {
                    "success": True,
                    "message": f"Status updated to {'available' if is_available else 'busy'}",
                    "driver": result.data[0],
                    "action": "status_updated"
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to update status",
                    "action": "retry"
                }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error updating availability: {str(e)}",
                "action": "error"
            }
    
    async def get_available_drivers(
        self, 
        location: Optional[str] = None,
        radius_km: float = 50.0,
        min_rating: float = 3.0
    ) -> List[Dict[str, Any]]:
        """
        Get available drivers with intelligent filtering and ranking
        """
        try:
            supabase = get_supabase_client()
            
            # Get all available drivers
            result = supabase.table("drivers").select("*").eq("is_available", True).execute()
            
            if not result.data:
                return []
            
            drivers = result.data
            
            # If location is specified, calculate distances and filter
            if location:
                drivers = await self._filter_drivers_by_location(drivers, location, radius_km)
            
            # Rank drivers by multiple factors
            ranked_drivers = await self._rank_drivers_by_suitability(drivers, supabase)
            
            return ranked_drivers
        
        except Exception as e:
            print(f"Error getting available drivers: {e}")
            return []
    
    async def find_best_driver_for_trip(
        self, 
        trip_id: UUID, 
        pickup_location: str,
        preferences: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        AI-powered driver selection for optimal trip assignment
        """
        try:
            supabase = get_supabase_client()
            
            # Get available drivers near pickup location
            available_drivers = await self.get_available_drivers(
                location=pickup_location,
                radius_km=preferences.get("max_distance_km", 25.0) if preferences else 25.0
            )
            
            if not available_drivers:
                return None
            
            # Score each driver based on multiple factors
            best_driver = None
            best_score = 0
            
            for driver in available_drivers:
                score = await self._calculate_driver_score(
                    driver, 
                    pickup_location, 
                    trip_id, 
                    preferences, 
                    supabase
                )
                
                if score > best_score:
                    best_score = score
                    best_driver = driver
            
            if best_driver:
                best_driver["selection_score"] = best_score
                best_driver["selection_reasons"] = await self._get_selection_reasons(
                    best_driver, pickup_location, supabase
                )
            
            return best_driver
        
        except Exception as e:
            print(f"Error finding best driver: {e}")
            return None
    
    async def predict_driver_acceptance(
        self, 
        driver_id: UUID, 
        trip_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Predict likelihood of driver accepting a trip based on historical data
        """
        try:
            supabase = get_supabase_client()
            
            # Get driver's trip history
            history_result = supabase.table("trips").select("*").eq("driver_id", str(driver_id)).execute()
            
            if not history_result.data:
                return {
                    "acceptance_probability": 0.5,  # Default for new drivers
                    "confidence": "low",
                    "factors": ["No historical data available"]
                }
            
            trip_history = history_result.data
            
            # Analyze patterns
            total_trips = len(trip_history)
            accepted_trips = len([t for t in trip_history if t["status"] != "cancelled"])
            
            # Calculate base acceptance rate
            base_rate = accepted_trips / total_trips if total_trips > 0 else 0.5
            
            # Adjust based on trip characteristics
            factors = []
            adjustment = 0
            
            # Distance factor
            if "distance_km" in trip_details:
                avg_distance = sum([t.get("distance_km", 0) for t in trip_history]) / total_trips
                if trip_details["distance_km"] > avg_distance * 1.5:
                    adjustment -= 0.1
                    factors.append("Trip longer than usual")
                elif trip_details["distance_km"] < avg_distance * 0.7:
                    adjustment += 0.1
                    factors.append("Trip shorter than usual")
            
            # Time of day factor
            current_hour = datetime.now().hour
            preferred_hours = self._get_driver_preferred_hours(trip_history)
            if current_hour in preferred_hours:
                adjustment += 0.1
                factors.append("Within preferred working hours")
            
            # Calculate final probability
            final_probability = max(0.1, min(0.9, base_rate + adjustment))
            
            confidence = "high" if total_trips > 10 else "medium" if total_trips > 3 else "low"
            
            return {
                "acceptance_probability": final_probability,
                "confidence": confidence,
                "factors": factors,
                "historical_acceptance_rate": base_rate,
                "total_trips_analyzed": total_trips
            }
        
        except Exception as e:
            print(f"Error predicting driver acceptance: {e}")
            return {
                "acceptance_probability": 0.5,
                "confidence": "low",
                "factors": [f"Error in prediction: {str(e)}"]
            }
    
    def _parse_availability_status(self, status: str) -> bool:
        """
        Parse natural language status into boolean availability
        """
        status = status.upper().strip()
        
        available_keywords = [
            "FREE", "AVAILABLE", "READY", "ONLINE", "ACTIVE", 
            "WORKING", "ON", "YES", "OPEN"
        ]
        
        busy_keywords = [
            "BUSY", "OCCUPIED", "UNAVAILABLE", "OFF", "OFFLINE", 
            "BREAK", "NO", "CLOSED", "NOT AVAILABLE"
        ]
        
        if any(keyword in status for keyword in available_keywords):
            return True
        elif any(keyword in status for keyword in busy_keywords):
            return False
        else:
            # Default interpretation based on context
            return "FREE" in status or "AVAILABLE" in status
    
    async def _find_optimal_trip_for_driver(
        self, 
        driver_id: str, 
        supabase: Client
    ) -> Optional[Dict[str, Any]]:
        """
        Find the most suitable pending trip for a newly available driver
        """
        try:
            # Get pending trips
            trips_result = supabase.table("trips").select("*").eq("status", "pending").execute()
            
            if not trips_result.data:
                return None
            
            # Get driver info
            driver_result = supabase.table("drivers").select("*").eq("id", driver_id).execute()
            if not driver_result.data:
                return None
            
            driver = driver_result.data[0]
            pending_trips = trips_result.data
            
            # Score each trip for this driver
            best_trip = None
            best_score = 0
            
            for trip in pending_trips:
                score = await self._calculate_trip_suitability_score(driver, trip)
                if score > best_score:
                    best_score = score
                    best_trip = trip
            
            if best_trip and best_score > 0.6:  # Only suggest if good match
                best_trip["suitability_score"] = best_score
                return best_trip
            
            return None
        
        except Exception as e:
            print(f"Error finding optimal trip: {e}")
            return None
    
    async def _filter_drivers_by_location(
        self, 
        drivers: List[Dict[str, Any]], 
        target_location: str, 
        radius_km: float
    ) -> List[Dict[str, Any]]:
        """
        Filter drivers by proximity to target location
        """
        # Simplified location matching (in production, use proper geocoding)
        filtered_drivers = []
        
        for driver in drivers:
            driver_location = driver.get("current_location", "")
            
            if driver_location:
                # Simple text matching for now
                # In production, use proper distance calculation with coordinates
                if self._locations_are_close(driver_location, target_location):
                    filtered_drivers.append(driver)
            else:
                # Include drivers without location (they can update it)
                filtered_drivers.append(driver)
        
        return filtered_drivers
    
    async def _rank_drivers_by_suitability(
        self, 
        drivers: List[Dict[str, Any]], 
        supabase: Client
    ) -> List[Dict[str, Any]]:
        """
        Rank drivers by suitability score
        """
        ranked_drivers = []
        
        for driver in drivers:
            score = await self._calculate_driver_base_score(driver, supabase)
            driver["suitability_score"] = score
            ranked_drivers.append(driver)
        
        # Sort by score (highest first)
        ranked_drivers.sort(key=lambda x: x["suitability_score"], reverse=True)
        
        return ranked_drivers
    
    async def _calculate_driver_score(
        self, 
        driver: Dict[str, Any], 
        pickup_location: str, 
        trip_id: UUID, 
        preferences: Optional[Dict[str, Any]], 
        supabase: Client
    ) -> float:
        """
        Calculate comprehensive driver score for trip assignment
        """
        score = 0.0
        
        # Base availability score
        score += 0.3
        
        # Location proximity (simplified)
        if driver.get("current_location"):
            if self._locations_are_close(driver["current_location"], pickup_location):
                score += 0.4
            else:
                score += 0.1
        
        # Historical performance
        performance_score = await self._get_driver_performance_score(driver["id"], supabase)
        score += performance_score * 0.3
        
        return min(1.0, score)
    
    async def _calculate_trip_suitability_score(
        self, 
        driver: Dict[str, Any], 
        trip: Dict[str, Any]
    ) -> float:
        """
        Calculate how suitable a trip is for a specific driver
        """
        score = 0.0
        
        # Location match
        if driver.get("current_location") and trip.get("pickup_location"):
            if self._locations_are_close(driver["current_location"], trip["pickup_location"]):
                score += 0.5
        
        # Trip urgency (if specified)
        if trip.get("priority") == "high":
            score += 0.2
        
        # Base suitability
        score += 0.3
        
        return min(1.0, score)
    
    async def _calculate_driver_base_score(
        self, 
        driver: Dict[str, Any], 
        supabase: Client
    ) -> float:
        """
        Calculate base suitability score for a driver
        """
        score = 0.5  # Base score
        
        # Recent activity bonus
        if driver.get("last_seen"):
            try:
                last_seen = datetime.fromisoformat(driver["last_seen"].replace('Z', '+00:00'))
                hours_since_last_seen = (datetime.utcnow() - last_seen.replace(tzinfo=None)).total_seconds() / 3600
                
                if hours_since_last_seen < 1:
                    score += 0.3
                elif hours_since_last_seen < 24:
                    score += 0.1
            except:
                pass
        
        # Performance score
        performance = await self._get_driver_performance_score(driver["id"], supabase)
        score += performance * 0.2
        
        return min(1.0, score)
    
    async def _get_driver_performance_score(
        self, 
        driver_id: str, 
        supabase: Client
    ) -> float:
        """
        Calculate driver performance score based on historical data
        """
        try:
            # Get recent trips
            result = supabase.table("trips").select("*").eq("driver_id", driver_id).limit(20).execute()
            
            if not result.data:
                return 0.5  # Default for new drivers
            
            trips = result.data
            total_trips = len(trips)
            completed_trips = len([t for t in trips if t["status"] == "completed"])
            
            completion_rate = completed_trips / total_trips if total_trips > 0 else 0.5
            
            return completion_rate
        
        except Exception as e:
            print(f"Error calculating performance score: {e}")
            return 0.5
    
    async def _get_selection_reasons(
        self, 
        driver: Dict[str, Any], 
        pickup_location: str, 
        supabase: Client
    ) -> List[str]:
        """
        Generate human-readable reasons for driver selection
        """
        reasons = []
        
        if driver.get("current_location"):
            if self._locations_are_close(driver["current_location"], pickup_location):
                reasons.append("Close to pickup location")
        
        if driver.get("suitability_score", 0) > 0.8:
            reasons.append("High suitability score")
        
        performance = await self._get_driver_performance_score(driver["id"], supabase)
        if performance > 0.8:
            reasons.append("Excellent track record")
        
        if not reasons:
            reasons.append("Available driver")
        
        return reasons
    
    def _locations_are_close(self, location1: str, location2: str) -> bool:
        """
        Simple location proximity check (replace with proper geocoding in production)
        """
        if not location1 or not location2:
            return False
        
        # Simple text matching for demonstration
        loc1_words = set(location1.lower().split())
        loc2_words = set(location2.lower().split())
        
        # Check for common words
        common_words = loc1_words.intersection(loc2_words)
        
        return len(common_words) > 0
    
    def _get_driver_preferred_hours(self, trip_history: List[Dict[str, Any]]) -> List[int]:
        """
        Analyze driver's preferred working hours from history
        """
        hour_counts = {}
        
        for trip in trip_history:
            if trip.get("created_at"):
                try:
                    created_time = datetime.fromisoformat(trip["created_at"].replace('Z', '+00:00'))
                    hour = created_time.hour
                    hour_counts[hour] = hour_counts.get(hour, 0) + 1
                except:
                    continue
        
        if not hour_counts:
            return list(range(9, 18))  # Default business hours
        
        # Return hours with above-average activity
        avg_activity = sum(hour_counts.values()) / len(hour_counts)
        preferred_hours = [hour for hour, count in hour_counts.items() if count > avg_activity]
        
        return preferred_hours if preferred_hours else list(range(9, 18))
