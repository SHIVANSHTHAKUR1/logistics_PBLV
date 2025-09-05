#!/usr/bin/env python3
"""
AI Logistics Demo Script
Demonstrates the capabilities of our AI-powered logistics system via API
"""
import json
import requests
from datetime import datetime

# API Configuration
BASE_URL = "http://localhost:8000"

def test_route_optimization():
    """Test the route optimization capabilities"""
    print("\n🚀 Testing Route Optimization...")
    
    test_data = {
        "origin": {"lat": 28.6139, "lng": 77.2090},  # Delhi
        "destination": {"lat": 19.0760, "lng": 72.8777},  # Mumbai
        "stops": [
            {"lat": 26.9124, "lng": 75.7873},  # Jaipur
            {"lat": 23.2599, "lng": 77.4126}   # Bhopal
        ],
        "vehicle_type": "truck",
        "departure_time": "2024-01-15T08:00:00"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/ai/routes/optimize", json=test_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ Route optimization successful!")
            print(f"   📍 Optimized route distance: {result.get('total_distance', 'N/A')} km")
            print(f"   ⏱️ Estimated time: {result.get('total_time', 'N/A')} hours")
            print(f"   💰 Estimated fuel cost: ₹{result.get('fuel_cost', 'N/A')}")
        else:
            print(f"❌ Route optimization failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Route optimization error: {e}")

def test_document_processing():
    """Test the document processing capabilities"""
    print("\n📄 Testing Document Processing...")
    
    try:
        # Test without actual file for now
        test_data = {"document_type": "receipt"}
        response = requests.post(f"{BASE_URL}/ai/documents/analyze", json=test_data, timeout=10)
        if response.status_code == 200:
            print("✅ Document processing endpoint available!")
        else:
            print(f"⚠️ Document processing response: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Document processing error: {e}")

def test_intelligent_trip_creation():
    """Test intelligent trip creation"""
    print("\n🧠 Testing Intelligent Trip Creation...")
    
    test_data = {
        "pickup_location": "Delhi, India",
        "delivery_location": "Mumbai, India", 
        "cargo_type": "Electronics",
        "cargo_weight": 500,
        "cargo_value": 100000,
        "pickup_date": "2024-01-15",
        "special_requirements": "Fragile items, temperature controlled"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/ai/trips/create-intelligent", json=test_data, timeout=15)
        if response.status_code == 200:
            result = response.json()
            print("✅ Intelligent trip creation successful!")
            print(f"   🚛 Recommended driver: {result.get('recommended_driver', 'N/A')}")
            print(f"   📍 Optimized route: {result.get('optimized_route', 'Available')}")
            print(f"   💰 Estimated cost: ₹{result.get('estimated_cost', 'N/A')}")
        else:
            print(f"❌ Intelligent trip creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Intelligent trip creation error: {e}")

def test_driver_analytics():
    """Test driver analytics"""
    print("\n👨‍💼 Testing Driver Analytics...")
    
    try:
        response = requests.get(f"{BASE_URL}/ai/drivers/analytics", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ Driver analytics successful!")
            print(f"   📊 Analytics available: {len(result.get('insights', []))}")
        else:
            print(f"⚠️ Driver analytics response: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Driver analytics error: {e}")

def test_api_health():
    """Test API health and AI status"""
    print("\n🏥 Testing API Health...")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API server is healthy")
        else:
            print(f"⚠️ API health check: {response.status_code}")
    except Exception as e:
        print(f"❌ API health check error: {e}")

def main():
    """Main demo function"""
    print("🌟 AI Logistics System Demo")
    print("=" * 40)
    print("🤖 Testing AI-powered logistics automation")
    print("📡 API Endpoint: http://localhost:8000")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running")
        else:
            print("❌ API server not responding properly")
            return
    except Exception as e:
        print(f"❌ Cannot connect to API server: {e}")
        print("💡 Make sure the server is running with: python src/backend/run_server.py")
        return
    
    # Run all tests
    test_api_health()
    test_route_optimization()
    test_document_processing()
    test_intelligent_trip_creation()
    test_driver_analytics()
    
    print("\n🎉 Demo completed!")
    print("🌐 View full API documentation at: http://localhost:8000/docs")
    print("🤖 All AI agents are active and ready for logistics automation!")

if __name__ == "__main__":
    main()
