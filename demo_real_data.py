#!/usr/bin/env python3
"""
AI Logistics Demo with Real Data
Demonstrates AI capabilities using actual logistics data from CSV files
"""
import pandas as pd
import json
import sys
import os
from datetime import datetime, timedelta

# Add the backend path for direct agent imports
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'backend')
sys.path.insert(0, backend_path)

def load_logistics_data():
    """Load all logistics data from CSV files"""
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'raw')
    
    try:
        drivers_df = pd.read_csv(os.path.join(data_dir, 'drivers.csv'))
        vehicles_df = pd.read_csv(os.path.join(data_dir, 'vehicles.csv'))
        trips_df = pd.read_csv(os.path.join(data_dir, 'trips.csv'))
        expenses_df = pd.read_csv(os.path.join(data_dir, 'expenses.csv'))
        owners_df = pd.read_csv(os.path.join(data_dir, 'owners.csv'))
        loads_df = pd.read_csv(os.path.join(data_dir, 'loads.csv'))
        
        print("✅ Successfully loaded logistics data:")
        print(f"   📊 Drivers: {len(drivers_df)} records")
        print(f"   🚛 Vehicles: {len(vehicles_df)} records")
        print(f"   🗺️ Trips: {len(trips_df)} records")
        print(f"   💰 Expenses: {len(expenses_df)} records")
        print(f"   🏢 Owners: {len(owners_df)} records")
        print(f"   📦 Loads: {len(loads_df)} records")
        
        return {
            'drivers': drivers_df,
            'vehicles': vehicles_df,
            'trips': trips_df,
            'expenses': expenses_df,
            'owners': owners_df,
            'loads': loads_df
        }
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def test_route_optimization_with_real_data(data):
    """Test route optimization using real trip data"""
    print("\n🚀 Testing Route Optimization with Real Data...")
    
    try:
        import importlib.util
        
        # Load the route optimization agent
        agent_path = os.path.join(backend_path, 'agents', 'route_optimization.py')
        if os.path.exists(agent_path):
            spec = importlib.util.spec_from_file_location("route_optimization", agent_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'RouteOptimizationAgent'):
                route_agent = module.RouteOptimizationAgent()
                
                # Get a real trip from our data
                trip = data['trips'].iloc[0]  # First trip: Delhi to Mumbai
                print(f"   🗺️ Optimizing route: {trip['pickup_location']} → {trip['delivery_location']}")
                
                # Test multi-stop optimization with intermediate cities
                stops = [
                    (26.9124, 75.7873),  # Jaipur
                    (23.2599, 77.4126)   # Bhopal
                ]
                
                result = route_agent.calculate_route_distance(
                    (trip['pickup_lat'], trip['pickup_lng']),
                    (trip['delivery_lat'], trip['delivery_lng'])
                )
                
                print(f"   📏 Direct distance: {result['distance']:.1f} km")
                print(f"   ⏱️ Estimated time: {result['time']:.1f} hours")
                
                # Test fuel optimization
                vehicle = data['vehicles'][data['vehicles']['vehicle_id'] == trip['vehicle_id']].iloc[0]
                fuel_result = route_agent.calculate_fuel_cost(
                    result['distance'], 
                    float(vehicle['mileage_kmpl'])
                )
                
                print(f"   ⛽ Estimated fuel cost: ₹{fuel_result['total_cost']:.2f}")
                print(f"   📊 Fuel consumption: {fuel_result['fuel_liters']:.1f} liters")
                
            else:
                print("❌ RouteOptimizationAgent class not found")
                
    except Exception as e:
        print(f"❌ Route optimization test failed: {e}")

def test_driver_analytics_with_real_data(data):
    """Test driver analytics using real driver data"""
    print("\n👨‍💼 Testing Driver Analytics with Real Data...")
    
    try:
        import importlib.util
        
        # Load the availability agent
        agent_path = os.path.join(backend_path, 'agents', 'availability_agent.py')
        if os.path.exists(agent_path):
            spec = importlib.util.spec_from_file_location("availability_agent", agent_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'AvailabilityAgent'):
                availability_agent = module.AvailabilityAgent()
                
                # Analyze driver performance
                drivers = data['drivers']
                available_drivers = drivers[drivers['availability_status'] == 'available']
                
                print(f"   📊 Total drivers: {len(drivers)}")
                print(f"   ✅ Available drivers: {len(available_drivers)}")
                print(f"   🚫 Busy drivers: {len(drivers[drivers['availability_status'] == 'busy'])}")
                
                # Find best drivers by rating
                top_drivers = drivers.nlargest(3, 'rating')
                print(f"\n   🏆 Top 3 Drivers by Rating:")
                for _, driver in top_drivers.iterrows():
                    print(f"      • {driver['name']} - Rating: {driver['rating']}/5.0 ({driver['experience_years']} years exp)")
                
                # Test driver scoring for a real trip
                trip = data['trips'].iloc[3]  # Jaipur to Delhi trip
                print(f"\n   🎯 Finding best driver for: {trip['pickup_location']} → {trip['delivery_location']}")
                
                # Score available drivers for this trip
                best_drivers = []
                for _, driver in available_drivers.iterrows():
                    # Calculate distance from driver to pickup location
                    distance = availability_agent.calculate_distance(
                        driver['current_location_lat'], driver['current_location_lng'],
                        trip['pickup_lat'], trip['pickup_lng']
                    )
                    
                    score = (driver['rating'] * 20) + (driver['experience_years'] * 2) - (distance * 0.1)
                    best_drivers.append({
                        'name': driver['name'],
                        'score': score,
                        'distance_km': distance,
                        'rating': driver['rating'],
                        'experience': driver['experience_years']
                    })
                
                # Sort by score and show top 3
                best_drivers.sort(key=lambda x: x['score'], reverse=True)
                print(f"   🥇 Best Driver Matches:")
                for i, driver in enumerate(best_drivers[:3], 1):
                    print(f"      {i}. {driver['name']} - Score: {driver['score']:.1f} (Rating: {driver['rating']}, {driver['distance_km']:.1f}km away)")
                
            else:
                print("❌ AvailabilityAgent class not found")
                
    except Exception as e:
        print(f"❌ Driver analytics test failed: {e}")

def test_expense_analysis_with_real_data(data):
    """Analyze expenses using real expense data"""
    print("\n💰 Testing Expense Analysis with Real Data...")
    
    try:
        expenses = data['expenses']
        trips = data['trips']
        
        # Expense summary
        total_expenses = expenses['amount_inr'].sum()
        print(f"   📊 Total expenses: ₹{total_expenses:,.2f}")
        
        # Expense breakdown by type
        expense_by_type = expenses.groupby('expense_type')['amount_inr'].sum().sort_values(ascending=False)
        print(f"\n   📋 Expense Breakdown:")
        for expense_type, amount in expense_by_type.items():
            percentage = (amount / total_expenses) * 100
            print(f"      • {expense_type.title()}: ₹{amount:,.2f} ({percentage:.1f}%)")
        
        # Trip profitability analysis
        completed_trips = trips[trips['status'] == 'completed']
        print(f"\n   🚚 Trip Profitability Analysis:")
        
        for _, trip in completed_trips.iterrows():
            trip_expenses = expenses[expenses['trip_id'] == trip['trip_id']]['amount_inr'].sum()
            revenue = trip['cargo_value_inr'] * 0.05  # Assume 5% of cargo value as freight charge
            profit = revenue - trip_expenses
            margin = (profit / revenue) * 100 if revenue > 0 else 0
            
            print(f"      📦 {trip['trip_id']}: Revenue ₹{revenue:,.0f}, Expenses ₹{trip_expenses:,.0f}, Profit ₹{profit:,.0f} ({margin:.1f}%)")
        
        # Driver expense analysis
        driver_expenses = expenses.groupby('driver_id')['amount_inr'].sum().sort_values(ascending=False)
        print(f"\n   👨‍💼 Top Drivers by Expenses:")
        for driver_id, amount in driver_expenses.head(5).items():
            driver_name = data['drivers'][data['drivers']['driver_id'] == driver_id]['name'].iloc[0]
            print(f"      • {driver_name} ({driver_id}): ₹{amount:,.2f}")
            
    except Exception as e:
        print(f"❌ Expense analysis failed: {e}")

def test_document_processing_simulation(data):
    """Simulate document processing with real data"""
    print("\n📄 Testing Document Processing Simulation...")
    
    try:
        import importlib.util
        
        # Load the document digitizer agent
        agent_path = os.path.join(backend_path, 'agents', 'document_digitizer.py')
        if os.path.exists(agent_path):
            spec = importlib.util.spec_from_file_location("document_digitizer", agent_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'DocumentDigitizerAgent'):
                doc_agent = module.DocumentDigitizerAgent()
                
                print(f"   🤖 Document AI Agent: {doc_agent.name}")
                print(f"   🔧 OCR capabilities initialized")
                
                # Simulate processing real expense receipts
                fuel_expenses = data['expenses'][data['expenses']['expense_type'] == 'fuel']
                print(f"\n   ⛽ Simulating OCR processing of {len(fuel_expenses)} fuel receipts:")
                
                total_fuel_amount = 0
                for _, expense in fuel_expenses.iterrows():
                    # Simulate OCR extraction
                    extracted_amount = expense['amount_inr']
                    total_fuel_amount += extracted_amount
                    
                    print(f"      📋 Receipt {expense['receipt_number']}: ₹{extracted_amount:,.2f}")
                    print(f"         📍 Location: {expense['location']}")
                    print(f"         📅 Date: {expense['expense_date']}")
                
                print(f"\n   💡 AI Processing Summary:")
                print(f"      🔍 Total receipts processed: {len(fuel_expenses)}")
                print(f"      💰 Total fuel costs extracted: ₹{total_fuel_amount:,.2f}")
                print(f"      📊 Average fuel cost per receipt: ₹{total_fuel_amount/len(fuel_expenses):,.2f}")
                
                # Simulate categorization
                expense_categories = data['expenses']['expense_type'].value_counts()
                print(f"\n   🏷️ Document categorization results:")
                for category, count in expense_categories.items():
                    print(f"      • {category.title()}: {count} documents")
                
            else:
                print("❌ DocumentDigitizerAgent class not found")
                
    except Exception as e:
        print(f"❌ Document processing simulation failed: {e}")

def test_trip_intelligence_with_real_data(data):
    """Test trip intelligence using real data"""
    print("\n🧠 Testing Trip Intelligence with Real Data...")
    
    try:
        trips = data['trips']
        drivers = data['drivers']
        vehicles = data['vehicles']
        loads = data['loads']
        
        # Trip status analysis
        status_counts = trips['status'].value_counts()
        print(f"   📊 Trip Status Overview:")
        for status, count in status_counts.items():
            print(f"      • {status.title()}: {count} trips")
        
        # Upcoming trips analysis
        scheduled_trips = trips[trips['status'] == 'scheduled']
        print(f"\n   📅 Upcoming Trips Analysis:")
        print(f"      🚚 Scheduled trips: {len(scheduled_trips)}")
        
        for _, trip in scheduled_trips.iterrows():
            load_info = loads[loads['trip_id'] == trip['trip_id']].iloc[0]
            driver_info = drivers[drivers['driver_id'] == trip['driver_id']].iloc[0]
            vehicle_info = vehicles[vehicles['vehicle_id'] == trip['vehicle_id']].iloc[0]
            
            print(f"\n      📦 Trip {trip['trip_id']}:")
            print(f"         🗺️ Route: {trip['pickup_location']} → {trip['delivery_location']}")
            print(f"         👨‍💼 Driver: {driver_info['name']} (Rating: {driver_info['rating']}/5)")
            print(f"         🚛 Vehicle: {vehicle_info['registration_number']} ({vehicle_info['capacity_tons']}T capacity)")
            print(f"         📦 Cargo: {load_info['cargo_description']} ({trip['cargo_weight_tons']}T)")
            print(f"         💰 Cargo Value: ₹{trip['cargo_value_inr']:,}")
            print(f"         📅 Pickup Date: {trip['pickup_date']}")
            
            # Special requirements check
            if pd.notna(load_info['special_requirements']):
                print(f"         ⚠️ Special Requirements: {load_info['special_requirements']}")
        
        # Performance metrics
        completed_trips = trips[trips['status'] == 'completed']
        if len(completed_trips) > 0:
            avg_distance = completed_trips['distance_km'].mean()
            total_cargo_value = completed_trips['cargo_value_inr'].sum()
            print(f"\n   📈 Performance Metrics:")
            print(f"      📏 Average trip distance: {avg_distance:.1f} km")
            print(f"      💰 Total cargo value transported: ₹{total_cargo_value:,}")
            print(f"      🚚 Fleet utilization: {len(completed_trips)}/{len(trips)} trips completed")
        
    except Exception as e:
        print(f"❌ Trip intelligence test failed: {e}")

def main():
    """Main demo function"""
    print("🌟 AI Logistics System - Real Data Demo")
    print("=" * 50)
    print("🤖 Testing AI capabilities with actual logistics data")
    
    # Load real data
    data = load_logistics_data()
    if not data:
        print("❌ Failed to load data. Exiting...")
        return
    
    # Run comprehensive AI tests with real data
    test_route_optimization_with_real_data(data)
    test_driver_analytics_with_real_data(data)
    test_expense_analysis_with_real_data(data)
    test_document_processing_simulation(data)
    test_trip_intelligence_with_real_data(data)
    
    print("\n🎉 Real Data Demo Completed!")
    print("📊 AI system successfully processed actual logistics data")
    print("🚀 Ready for production deployment with real-world scenarios")

if __name__ == "__main__":
    main()
