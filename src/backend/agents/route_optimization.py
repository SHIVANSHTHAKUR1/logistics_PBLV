"""
Route Optimization Agent - Optimizes routes and provides intelligent trip planning
Uses algorithms to find optimal routes, considering traffic, fuel costs, and time constraints
"""
import math
import asyncio
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timedelta
import json
from dataclasses import dataclass

@dataclass
class Location:
    name: str
    latitude: float = 0.0
    longitude: float = 0.0
    address: str = ""

@dataclass
class RouteSegment:
    from_location: Location
    to_location: Location
    distance_km: float
    estimated_time_minutes: int
    fuel_cost: float
    toll_cost: float = 0.0

class RouteOptimizationAgent:
    def __init__(self):
        self.name = "Route Optimization Agent"
        self.version = "1.0.0"
        
        # Default parameters (can be configured)
        self.fuel_price_per_liter = 100.0  # INR
        self.vehicle_mileage_kmpl = 12.0   # km per liter
        self.driver_hourly_rate = 150.0    # INR per hour
        
        # Simplified city coordinates for demonstration
        self.city_coordinates = {
            "mumbai": {"lat": 19.0760, "lng": 72.8777},
            "delhi": {"lat": 28.7041, "lng": 77.1025},
            "bangalore": {"lat": 12.9716, "lng": 77.5946},
            "chennai": {"lat": 13.0827, "lng": 80.2707},
            "kolkata": {"lat": 22.5726, "lng": 88.3639},
            "pune": {"lat": 18.5204, "lng": 73.8567},
            "hyderabad": {"lat": 17.3850, "lng": 78.4867},
            "ahmedabad": {"lat": 23.0225, "lng": 72.5714},
            "jaipur": {"lat": 26.9124, "lng": 75.7873},
            "surat": {"lat": 21.1702, "lng": 72.8311}
        }
    
    async def optimize_single_route(
        self, 
        origin: str, 
        destination: str, 
        constraints: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Optimize a single route from origin to destination
        """
        try:
            # Parse locations
            origin_loc = self._parse_location(origin)
            destination_loc = self._parse_location(destination)
            
            if not origin_loc or not destination_loc:
                return {
                    "success": False,
                    "error": "Unable to parse origin or destination locations"
                }
            
            # Calculate route details
            route_info = await self._calculate_route_details(origin_loc, destination_loc, constraints)
            
            # Generate route recommendations
            recommendations = await self._generate_route_recommendations(route_info, constraints)
            
            return {
                "success": True,
                "route_info": route_info,
                "recommendations": recommendations,
                "optimization_timestamp": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "optimization_timestamp": datetime.utcnow().isoformat()
            }
    
    async def optimize_multi_stop_route(
        self, 
        stops: List[str], 
        constraints: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Optimize a route with multiple stops (Traveling Salesman Problem variant)
        """
        try:
            if len(stops) < 2:
                return {
                    "success": False,
                    "error": "At least 2 stops are required"
                }
            
            # Parse all locations
            locations = []
            for stop in stops:
                loc = self._parse_location(stop)
                if loc:
                    locations.append(loc)
            
            if len(locations) != len(stops):
                return {
                    "success": False,
                    "error": "Unable to parse some locations"
                }
            
            # Find optimal route order
            optimal_order = await self._find_optimal_route_order(locations, constraints)
            
            # Calculate detailed route information
            route_segments = []
            total_distance = 0.0
            total_time = 0
            total_cost = 0.0
            
            for i in range(len(optimal_order) - 1):
                from_loc = locations[optimal_order[i]]
                to_loc = locations[optimal_order[i + 1]]
                
                segment = await self._calculate_route_segment(from_loc, to_loc, constraints)
                route_segments.append(segment)
                
                total_distance += segment.distance_km
                total_time += segment.estimated_time_minutes
                total_cost += segment.fuel_cost + segment.toll_cost
            
            return {
                "success": True,
                "optimal_order": [stops[i] for i in optimal_order],
                "route_segments": [self._segment_to_dict(seg) for seg in route_segments],
                "summary": {
                    "total_distance_km": round(total_distance, 2),
                    "total_time_hours": round(total_time / 60, 2),
                    "total_cost_inr": round(total_cost, 2),
                    "fuel_cost_inr": round(sum(seg.fuel_cost for seg in route_segments), 2),
                    "toll_cost_inr": round(sum(seg.toll_cost for seg in route_segments), 2)
                },
                "optimization_timestamp": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "optimization_timestamp": datetime.utcnow().isoformat()
            }
    
    async def suggest_optimal_departure_time(
        self, 
        origin: str, 
        destination: str, 
        preferred_arrival_time: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Suggest optimal departure time considering traffic patterns
        """
        try:
            origin_loc = self._parse_location(origin)
            destination_loc = self._parse_location(destination)
            
            if not origin_loc or not destination_loc:
                return {
                    "success": False,
                    "error": "Unable to parse locations"
                }
            
            # Calculate base travel time
            base_route = await self._calculate_route_details(origin_loc, destination_loc)
            base_time_hours = base_route["estimated_time_hours"]
            
            # Analyze different departure time options
            departure_options = []
            
            # Check different hours of the day
            for hour in range(6, 23):  # 6 AM to 10 PM
                departure_time = datetime.now().replace(hour=hour, minute=0, second=0)
                
                # Apply traffic multiplier based on time
                traffic_multiplier = self._get_traffic_multiplier(hour)
                adjusted_time = base_time_hours * traffic_multiplier
                
                arrival_time = departure_time + timedelta(hours=adjusted_time)
                
                departure_options.append({
                    "departure_time": departure_time.strftime("%H:%M"),
                    "estimated_arrival_time": arrival_time.strftime("%H:%M"),
                    "travel_time_hours": round(adjusted_time, 2),
                    "traffic_condition": self._get_traffic_condition(hour),
                    "score": self._calculate_departure_score(hour, adjusted_time)
                })
            
            # Sort by score (best options first)
            departure_options.sort(key=lambda x: x["score"], reverse=True)
            
            # If preferred arrival time is given, find closest options
            if preferred_arrival_time:
                preferred_options = self._filter_by_arrival_preference(
                    departure_options, preferred_arrival_time
                )
                
                return {
                    "success": True,
                    "preferred_options": preferred_options[:3],
                    "all_options": departure_options[:10],
                    "base_travel_time_hours": base_time_hours,
                    "optimization_timestamp": datetime.utcnow().isoformat()
                }
            
            return {
                "success": True,
                "recommended_options": departure_options[:5],
                "all_options": departure_options,
                "base_travel_time_hours": base_time_hours,
                "optimization_timestamp": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "optimization_timestamp": datetime.utcnow().isoformat()
            }
    
    async def calculate_fuel_optimization(
        self, 
        route_info: Dict[str, Any],
        vehicle_specs: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Calculate fuel optimization strategies for a route
        """
        try:
            # Use provided vehicle specs or defaults
            mileage = vehicle_specs.get("mileage_kmpl", self.vehicle_mileage_kmpl) if vehicle_specs else self.vehicle_mileage_kmpl
            fuel_price = vehicle_specs.get("fuel_price_per_liter", self.fuel_price_per_liter) if vehicle_specs else self.fuel_price_per_liter
            tank_capacity = vehicle_specs.get("tank_capacity_liters", 50) if vehicle_specs else 50
            
            distance_km = route_info.get("total_distance_km", 0)
            
            # Calculate fuel requirements
            fuel_needed_liters = distance_km / mileage
            fuel_cost = fuel_needed_liters * fuel_price
            
            # Calculate number of fuel stops needed
            fuel_stops_needed = math.ceil(fuel_needed_liters / tank_capacity) - 1
            
            # Suggest fuel stops along the route
            fuel_stop_suggestions = []
            if fuel_stops_needed > 0:
                stop_interval_km = distance_km / (fuel_stops_needed + 1)
                
                for i in range(1, fuel_stops_needed + 1):
                    stop_distance = stop_interval_km * i
                    fuel_stop_suggestions.append({
                        "stop_number": i,
                        "approximate_distance_km": round(stop_distance, 0),
                        "suggested_location": f"Fuel stop {i} (around {stop_distance:.0f}km mark)"
                    })
            
            # Fuel efficiency tips
            efficiency_tips = [
                "Maintain steady speed (60-80 km/h for optimal mileage)",
                "Avoid aggressive acceleration and braking",
                "Keep tires properly inflated",
                "Remove unnecessary weight from vehicle",
                "Plan route to avoid heavy traffic areas"
            ]
            
            if distance_km > 500:
                efficiency_tips.append("Consider overnight rest to avoid driver fatigue")
            
            return {
                "success": True,
                "fuel_analysis": {
                    "total_fuel_needed_liters": round(fuel_needed_liters, 2),
                    "estimated_fuel_cost_inr": round(fuel_cost, 2),
                    "fuel_stops_recommended": fuel_stops_needed,
                    "cost_per_km": round(fuel_cost / distance_km, 2) if distance_km > 0 else 0
                },
                "fuel_stop_suggestions": fuel_stop_suggestions,
                "efficiency_tips": efficiency_tips,
                "vehicle_specs_used": {
                    "mileage_kmpl": mileage,
                    "fuel_price_per_liter": fuel_price,
                    "tank_capacity_liters": tank_capacity
                }
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _parse_location(self, location_str: str) -> Optional[Location]:
        """
        Parse location string and get coordinates
        """
        location_lower = location_str.lower().strip()
        
        # Check if it's a known city
        for city, coords in self.city_coordinates.items():
            if city in location_lower or location_lower in city:
                return Location(
                    name=location_str,
                    latitude=coords["lat"],
                    longitude=coords["lng"],
                    address=location_str
                )
        
        # For unknown locations, return with default coordinates
        return Location(
            name=location_str,
            latitude=0.0,
            longitude=0.0,
            address=location_str
        )
    
    async def _calculate_route_details(
        self, 
        origin: Location, 
        destination: Location, 
        constraints: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Calculate detailed route information
        """
        # Calculate distance using Haversine formula
        distance_km = self._calculate_distance(
            origin.latitude, origin.longitude,
            destination.latitude, destination.longitude
        )
        
        # Estimate travel time (average speed based on route type)
        avg_speed_kmh = 60  # Default highway speed
        if constraints and "preferred_speed" in constraints:
            avg_speed_kmh = constraints["preferred_speed"]
        
        estimated_time_hours = distance_km / avg_speed_kmh
        estimated_time_minutes = estimated_time_hours * 60
        
        # Calculate costs
        fuel_needed = distance_km / self.vehicle_mileage_kmpl
        fuel_cost = fuel_needed * self.fuel_price_per_liter
        
        # Estimate toll costs (simplified)
        toll_cost = self._estimate_toll_cost(distance_km)
        
        # Driver cost
        driver_cost = estimated_time_hours * self.driver_hourly_rate
        
        total_cost = fuel_cost + toll_cost + driver_cost
        
        return {
            "origin": origin.name,
            "destination": destination.name,
            "distance_km": round(distance_km, 2),
            "estimated_time_hours": round(estimated_time_hours, 2),
            "estimated_time_minutes": round(estimated_time_minutes, 0),
            "costs": {
                "fuel_cost_inr": round(fuel_cost, 2),
                "toll_cost_inr": round(toll_cost, 2),
                "driver_cost_inr": round(driver_cost, 2),
                "total_cost_inr": round(total_cost, 2)
            },
            "fuel_needed_liters": round(fuel_needed, 2)
        }
    
    async def _calculate_route_segment(
        self, 
        from_loc: Location, 
        to_loc: Location, 
        constraints: Optional[Dict[str, Any]] = None
    ) -> RouteSegment:
        """
        Calculate details for a single route segment
        """
        distance_km = self._calculate_distance(
            from_loc.latitude, from_loc.longitude,
            to_loc.latitude, to_loc.longitude
        )
        
        avg_speed = 60  # km/h
        estimated_time_minutes = (distance_km / avg_speed) * 60
        
        fuel_cost = (distance_km / self.vehicle_mileage_kmpl) * self.fuel_price_per_liter
        toll_cost = self._estimate_toll_cost(distance_km)
        
        return RouteSegment(
            from_location=from_loc,
            to_location=to_loc,
            distance_km=distance_km,
            estimated_time_minutes=int(estimated_time_minutes),
            fuel_cost=fuel_cost,
            toll_cost=toll_cost
        )
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using Haversine formula
        """
        if lat1 == 0 and lon1 == 0 and lat2 == 0 and lon2 == 0:
            # Fallback for unknown coordinates - estimate based on names
            return 100.0  # Default distance
        
        R = 6371  # Earth's radius in kilometers
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat/2) * math.sin(dlat/2) + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dlon/2) * math.sin(dlon/2))
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def _estimate_toll_cost(self, distance_km: float) -> float:
        """
        Estimate toll costs based on distance
        """
        # Simplified toll calculation
        if distance_km < 50:
            return 0.0
        elif distance_km < 200:
            return distance_km * 0.5  # 50 paise per km
        else:
            return distance_km * 0.8  # 80 paise per km for long distances
    
    async def _find_optimal_route_order(
        self, 
        locations: List[Location], 
        constraints: Optional[Dict[str, Any]] = None
    ) -> List[int]:
        """
        Find optimal order to visit locations (simplified TSP)
        """
        if len(locations) <= 3:
            # For small sets, try all permutations
            return await self._brute_force_tsp(locations)
        else:
            # For larger sets, use nearest neighbor heuristic
            return await self._nearest_neighbor_tsp(locations)
    
    async def _brute_force_tsp(self, locations: List[Location]) -> List[int]:
        """
        Brute force solution for small TSP instances
        """
        from itertools import permutations
        
        n = len(locations)
        min_distance = float('inf')
        best_route = list(range(n))
        
        # Try all possible routes starting from location 0
        for perm in permutations(range(1, n)):
            route = [0] + list(perm)
            total_distance = 0
            
            for i in range(n - 1):
                loc1 = locations[route[i]]
                loc2 = locations[route[i + 1]]
                total_distance += self._calculate_distance(
                    loc1.latitude, loc1.longitude,
                    loc2.latitude, loc2.longitude
                )
            
            if total_distance < min_distance:
                min_distance = total_distance
                best_route = route
        
        return best_route
    
    async def _nearest_neighbor_tsp(self, locations: List[Location]) -> List[int]:
        """
        Nearest neighbor heuristic for TSP
        """
        n = len(locations)
        unvisited = set(range(1, n))
        route = [0]  # Start from first location
        current = 0
        
        while unvisited:
            nearest = min(unvisited, key=lambda x: self._calculate_distance(
                locations[current].latitude, locations[current].longitude,
                locations[x].latitude, locations[x].longitude
            ))
            route.append(nearest)
            unvisited.remove(nearest)
            current = nearest
        
        return route
    
    def _get_traffic_multiplier(self, hour: int) -> float:
        """
        Get traffic multiplier based on hour of day
        """
        # Peak hours: 7-10 AM and 5-8 PM
        if 7 <= hour <= 10 or 17 <= hour <= 20:
            return 1.5  # 50% more time due to traffic
        elif 11 <= hour <= 16 or 21 <= hour <= 23:
            return 1.0  # Normal traffic
        else:
            return 0.8  # Light traffic (early morning/night)
    
    def _get_traffic_condition(self, hour: int) -> str:
        """
        Get traffic condition description
        """
        if 7 <= hour <= 10 or 17 <= hour <= 20:
            return "Heavy traffic"
        elif 11 <= hour <= 16 or 21 <= hour <= 23:
            return "Moderate traffic"
        else:
            return "Light traffic"
    
    def _calculate_departure_score(self, hour: int, travel_time: float) -> float:
        """
        Calculate score for departure time (higher = better)
        """
        score = 100.0
        
        # Prefer avoiding peak hours
        if 7 <= hour <= 10 or 17 <= hour <= 20:
            score -= 30
        
        # Prefer reasonable hours (not too early/late)
        if hour < 6 or hour > 22:
            score -= 20
        
        # Prefer shorter travel times
        score -= travel_time * 5
        
        return max(0, score)
    
    def _filter_by_arrival_preference(
        self, 
        options: List[Dict[str, Any]], 
        preferred_arrival: str
    ) -> List[Dict[str, Any]]:
        """
        Filter options by preferred arrival time
        """
        try:
            preferred_time = datetime.strptime(preferred_arrival, "%H:%M").time()
            
            # Sort by closeness to preferred arrival time
            def time_difference(option):
                arrival_time = datetime.strptime(option["estimated_arrival_time"], "%H:%M").time()
                preferred_minutes = preferred_time.hour * 60 + preferred_time.minute
                arrival_minutes = arrival_time.hour * 60 + arrival_time.minute
                return abs(preferred_minutes - arrival_minutes)
            
            return sorted(options, key=time_difference)[:5]
        
        except ValueError:
            # If preferred time format is invalid, return top scored options
            return options[:5]
    
    def _segment_to_dict(self, segment: RouteSegment) -> Dict[str, Any]:
        """
        Convert RouteSegment to dictionary
        """
        return {
            "from": segment.from_location.name,
            "to": segment.to_location.name,
            "distance_km": round(segment.distance_km, 2),
            "estimated_time_minutes": segment.estimated_time_minutes,
            "fuel_cost_inr": round(segment.fuel_cost, 2),
            "toll_cost_inr": round(segment.toll_cost, 2),
            "total_cost_inr": round(segment.fuel_cost + segment.toll_cost, 2)
        }
    
    async def _generate_route_recommendations(
        self, 
        route_info: Dict[str, Any], 
        constraints: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Generate recommendations for the route
        """
        recommendations = []
        
        distance = route_info.get("distance_km", 0)
        time_hours = route_info.get("estimated_time_hours", 0)
        
        # Distance-based recommendations
        if distance > 500:
            recommendations.append("Long distance trip - consider overnight rest stops")
            recommendations.append("Plan for multiple fuel stops")
        elif distance > 200:
            recommendations.append("Medium distance trip - one fuel stop may be needed")
        
        # Time-based recommendations
        if time_hours > 8:
            recommendations.append("Consider splitting journey over multiple days")
        elif time_hours > 4:
            recommendations.append("Plan for rest breaks every 2 hours")
        
        # Cost optimization
        fuel_cost = route_info.get("costs", {}).get("fuel_cost_inr", 0)
        if fuel_cost > 2000:
            recommendations.append("High fuel cost - consider fuel-efficient driving techniques")
        
        # Default recommendations
        if not recommendations:
            recommendations.extend([
                "Maintain steady speed for better fuel efficiency",
                "Check weather conditions before departure",
                "Keep emergency contact numbers handy"
            ])
        
        return recommendations
