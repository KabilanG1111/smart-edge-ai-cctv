"""
Test /api/intelligence/live endpoint
"""
import urllib.request
import json

print("=" * 70)
print("TESTING /api/intelligence/live ENDPOINT")
print("=" * 70)

# Test 1: Endpoint connectivity
print("\n[TEST 1] Endpoint Connectivity...")
try:
    with urllib.request.urlopen('http://localhost:8000/api/intelligence/live', timeout=5) as response:
        if response.status == 200:
            print("  ✅ Endpoint reachable")
            data = json.loads(response.read().decode())
            print(f"  Status: {data.get('status')}")
            print(f"  Total Events: {data.get('total')}")
        else:
            print(f"  ❌ Status code: {response.status}")
            exit(1)
except Exception as e:
    print(f"  ❌ Connection error: {e}")
    exit(1)

# Test 2: Response structure
print("\n[TEST 2] Response Structure...")
try:
    with urllib.request.urlopen('http://localhost:8000/api/intelligence/live?limit=10') as response:
        data = json.loads(response.read().decode())
        
        required_keys = ['status', 'total', 'events']
        if all(key in data for key in required_keys):
            print("  ✅ All required keys present")
            print(f"     Keys: {list(data.keys())}")
        else:
            print("  ❌ Missing required keys")
            exit(1)
            
        if data['events']:
            event_keys = list(data['events'][0].keys())
            required_event_keys = ['track_id', 'event_type', 'severity', 'reasoning', 'timestamp']
            if all(key in event_keys for key in required_event_keys):
                print("  ✅ Event structure correct")
                print(f"     Event Keys: {event_keys}")
            else:
                print("  ❌ Missing event keys")
                exit(1)
        else:
            print("  ℹ️  No events yet (normal for fresh start)")
except Exception as e:
    print(f"  ❌ Error: {e}")
    exit(1)

# Test 3: Display sample events
print("\n[TEST 3] Sample Events...")
if data['events']:
    for i, event in enumerate(data['events'][:3], 1):
        print(f"\n  Event {i}:")
        print(f"    Type: {event['event_type']}")
        print(f"    Severity: {event['severity']}")
        print(f"    Track ID: {event['track_id']}")
        print(f"    Reasoning: {event['reasoning'][:60]}...")
        print(f"    Timestamp: {event['timestamp']}")
else:
    print("  ℹ️  No events in buffer (camera not started)")
    print("  💡 Start camera feed to generate real-time reasoning!")

print("\n" + "=" * 70)
print("✅ ENDPOINT TEST PASSED")
print("=" * 70)
print("\nAPI Endpoint Ready:")
print("  URL: http://localhost:8000/api/intelligence/live")
print("  Method: GET")
print("  Params: limit (default: 50)")
print("\nFrontend Integration:")
print("  Polling interval: 500ms")
print("  Event format: track_id, event_type, severity, reasoning, timestamp")
print("  Severity colors: CRITICAL (red), WARNING (yellow), NORMAL (green)")
print("\nNext Steps:")
print("  1. Open Intelligence Core: http://localhost:3000/intelligence-core")
print("  2. Start camera feed")
print("  3. Watch real-time reasoning appear within 1 second!")
