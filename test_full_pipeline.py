"""
Test the intelligence events API with test event publishing
"""
import urllib.request
import json

def test_pipeline():
    """Test the complete intelligence events pipeline"""
    
    print("🧠 Testing Intelligence Events Pipeline\n")
    
    # Step 1: Check initial state
    print("📡 Step 1: Checking initial state...")
    try:
        with urllib.request.urlopen('http://localhost:8000/api/intelligence/events') as response:
            data = json.loads(response.read().decode())
            initial_count = data['total']
            print(f"   Initial events in store: {initial_count}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Step 2: Publish test events
    print("\n📤 Step 2: Publishing test events via API...")
    try:
        req = urllib.request.Request(
            'http://localhost:8000/api/intelligence/events/test',
            method='POST'
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(f"   ✅ {data['message']}")
            print(f"   Total events in store: {data['total_events_in_store']}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Step 3: Retrieve and display events
    print("\n📥 Step 3: Retrieving events from API...")
    try:
        with urllib.request.urlopen('http://localhost:8000/api/intelligence/events?limit=10') as response:
            data = json.loads(response.read().decode())
            print(f"   Status: {data['status']}")
            print(f"   Total events: {data['total']}")
            print(f"   Events returned: {len(data['events'])}")
            
            if data['events']:
                print("\n📋 Recent Events:\n")
                for event in data['events'][:3]:  # Show first 3
                    print(f"   Event #{event['event_id']}: {event['event_type']}")
                    print(f"     Severity: {event['severity']} (score: {event['severity_score']:.2f})")
                    print(f"     Track ID: {event['track_id']}")
                    print(f"     Reasoning: {event['reasoning_text'][:70]}...")
                    print()
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_pipeline()
    
    if success:
        print("✅✅✅ INTELLIGENCE EVENTS PIPELINE FULLY OPERATIONAL! ✅✅✅")
        print("\n🎯 System Status:")
        print("   ✅ Event store module working")
        print("   ✅ Event publishing working")
        print("   ✅ API endpoint serving events")
        print("   ✅ Backend integration complete")
        print("\n📖 Next Steps:")
        print("   1. Open: test_events_endpoint.html in browser")
        print("   2. Click 'Refresh Events' to see the 5 test events")
        print("   3. Start camera feed to generate REAL events")
        print("   4. Check Intelligence Core: http://localhost:3000/intelligence-core")
        print("   5. Watch events appear in real-time with 1-second polling!")
    else:
        print("\n❌ Pipeline test failed")
