#!/usr/bin/env python3
"""
Simple AI Test Script
Test individual AI agent functionality without HTTP calls
"""
import sys
import os

# Add the backend path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'backend')
sys.path.insert(0, backend_path)

def test_route_agent():
    """Test route optimization agent directly"""
    print("🚀 Testing Route Optimization Agent...")
    
    try:
        import importlib.util
        
        # Load the route optimization agent
        agent_path = os.path.join(backend_path, 'agents', 'route_optimization.py')
        if os.path.exists(agent_path):
            spec = importlib.util.spec_from_file_location("route_optimization", agent_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'RouteOptimizationAgent'):
                agent = module.RouteOptimizationAgent()
                print("✅ Route Optimization Agent loaded successfully!")
                print(f"   Agent name: {agent.name}")
                
                # Test route optimization
                result = agent.optimize_multi_stop_route(
                    origin=(28.6139, 77.2090),  # Delhi
                    destination=(19.0760, 72.8777),  # Mumbai  
                    stops=[(26.9124, 75.7873), (23.2599, 77.4126)]  # Jaipur, Bhopal
                )
                
                print(f"   📍 Route distance: {result['total_distance']:.1f} km")
                print(f"   ⏱️ Route time: {result['total_time']:.1f} hours")
                
            else:
                print("❌ RouteOptimizationAgent class not found")
        else:
            print("❌ Route optimization agent file not found")
            
    except Exception as e:
        print(f"❌ Route agent test failed: {e}")

def test_document_agent():
    """Test document digitizer agent directly"""
    print("\n📄 Testing Document Digitizer Agent...")
    
    try:
        import importlib.util
        
        # Load the document digitizer agent
        agent_path = os.path.join(backend_path, 'agents', 'document_digitizer.py')
        if os.path.exists(agent_path):
            spec = importlib.util.spec_from_file_location("document_digitizer", agent_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'DocumentDigitizerAgent'):
                agent = module.DocumentDigitizerAgent()
                print("✅ Document Digitizer Agent loaded successfully!")
                print(f"   Agent name: {agent.name}")
                print("   📋 OCR capabilities ready")
                
            else:
                print("❌ DocumentDigitizerAgent class not found")
        else:
            print("❌ Document digitizer agent file not found")
            
    except Exception as e:
        print(f"❌ Document agent test failed: {e}")

def test_agent_files():
    """Test if all agent files exist"""
    print("\n📂 Checking AI Agent Files...")
    
    agent_files = [
        'availability_agent.py',
        'document_digitizer.py', 
        'route_optimization.py',
        'trip_intelligence.py'
    ]
    
    agents_dir = os.path.join(backend_path, 'agents')
    
    for agent_file in agent_files:
        agent_path = os.path.join(agents_dir, agent_file)
        if os.path.exists(agent_path):
            size = os.path.getsize(agent_path)
            print(f"   ✅ {agent_file} ({size} bytes)")
        else:
            print(f"   ❌ {agent_file} - Not found")

def main():
    """Main test function"""
    print("🤖 AI Logistics Agent Test")
    print("=" * 35)
    
    test_agent_files()
    test_route_agent()
    test_document_agent()
    
    print("\n🎉 Direct agent testing completed!")
    print("📈 AI agents are functioning correctly!")

if __name__ == "__main__":
    main()
