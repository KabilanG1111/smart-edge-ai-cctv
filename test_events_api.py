"""
Quick test of the Intelligence Events API endpoint
"""
import urllib.request
import json
import time

def test_endpoint():
    """Test the /api/intelligence/events endpoint"""
    url = 'http://localhost:8000/api/intelligence/events?limit=10'
    
    print("🧠 Testing Intelligence Events API")
    print(f"📡 URL: {url}\n")
    
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            if response.status == 200:
                print("✅ Endpoint is reachable!")
                data = json.loads(response.read().decode())
                
                print(f"\n📊 Response:")
                print(f"  Status: {data.get('status')}")
                print(f"  Total Events: {data.get('total')}")
                print(f"  Events Returned: {len(data.get('events', []))}")
                
                if data.get('events'):
                    print(f"\n📋 Recent Events:")
                    for event in data['events'][:5]:  # Show first 5
                        print(f"\n  Event #{event['event_id']}:")
                        print(f"    Type: {event['event_type']}")
                        print(f"    Severity: {event['severity']} (score: {event['severity_score']:.2f})")
                        print(f"    Track ID: {event['track_id']}")
                        print(f"    Duration: {event['duration']}s")
                        print(f"    Timestamp: {event['timestamp']}")
                        print(f"    Reasoning: {event['reasoning_text'][:80]}...")
                else:
                    print("\n  ℹ️  No events in store yet")
                    print("  👉 Start the camera to generate events")
                
                return True
            else:
                print(f"❌ Unexpected status code: {response.status}")
                return False
                
    except urllib.error.URLError as e:
        print(f"❌ Connection error: {e}")
        print("  Make sure the backend is running on port 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_endpoint()
    
    if success:
        print("\n✅ Intelligence Events API is OPERATIONAL!")
        print("\n📖 Next steps:")
        print("  1. Open test_events_endpoint.html in a browser for live view")
        print("  2. Start the camera feed to generate real events")
        print("  3. Check Intelligence Core page: http://localhost:3000/intelligence-core")
    else:
        print("\n❌ Test failed")
