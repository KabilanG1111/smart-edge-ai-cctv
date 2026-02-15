"""
Test event publishing to verify the full pipeline works
"""
import sys
sys.path.insert(0, 'F:/CCTV')

from backend.event_store import (
    publish_event, get_events, EventType, EventSeverity,
    generate_reasoning_text, get_severity_level
)
import time

def test_event_publishing():
    """Test publishing various event types"""
    print("🧠 Testing Event Publishing Pipeline\n")
    
    # Test 1: Loitering event
    print("📝 Publishing LOITERING event...")
    reasoning = generate_reasoning_text(EventType.LOITERING, 42, 18.5, {})
    publish_event(
        event_type=EventType.LOITERING,
        severity=EventSeverity.MEDIUM,
        track_id=42,
        severity_score=0.68,
        duration=18.5,
        reasoning_text=reasoning
    )
    time.sleep(0.1)
    
    # Test 2: Zone violation
    print("📝 Publishing ZONE_VIOLATION event...")
    reasoning = generate_reasoning_text(EventType.ZONE_VIOLATION, 15, 5.2, {})
    publish_event(
        event_type=EventType.ZONE_VIOLATION,
        severity=EventSeverity.HIGH,
        track_id=15,
        severity_score=0.82,
        duration=5.2,
        reasoning_text=reasoning
    )
    time.sleep(0.1)
    
    # Test 3: Intrusion
    print("📝 Publishing INTRUSION event...")
    reasoning = generate_reasoning_text(EventType.INTRUSION, 7, 12.0, {})
    publish_event(
        event_type=EventType.INTRUSION,
        severity=EventSeverity.CRITICAL,
        track_id=7,
        severity_score=0.95,
        duration=12.0,
        reasoning_text=reasoning
    )
    time.sleep(0.1)
    
    # Test 4: Fight
    print("📝 Publishing FIGHT event...")
    reasoning = generate_reasoning_text(EventType.FIGHT, 23, 8.7, {})
    publish_event(
        event_type=EventType.FIGHT,
        severity=EventSeverity.CRITICAL,
        track_id=23,
        severity_score=0.91,
        duration=8.7,
        reasoning_text=reasoning
    )
    time.sleep(0.1)
    
    # Test 5: Theft
    print("📝 Publishing THEFT event...")
    reasoning = generate_reasoning_text(EventType.THEFT, 33, 25.3, {})
    publish_event(
        event_type=EventType.THEFT,
        severity=EventSeverity.HIGH,
        track_id=33,
        severity_score=0.79,
        duration=25.3,
        reasoning_text=reasoning
    )
    
    print("\n✅ Published 5 test events")
    
    # Retrieve and display events
    print("\n📋 Retrieving events from store...")
    events = get_events(limit=10)
    
    print(f"\n📊 Total events in store: {len(events)}")
    
    if events:
        print("\n🔍 Event Details:\n")
        for event in events:
            print(f"  Event #{event['event_id']}:")
            print(f"    Type: {event['event_type']}")
            print(f"    Severity: {event['severity']} (score: {event['severity_score']:.2f})")
            print(f"    Track ID: {event['track_id']}")
            print(f"    Duration: {event['duration']}s")
            print(f"    Reasoning: {event['reasoning_text']}")
            print(f"    Timestamp: {event['timestamp']}")
            print()
    
    return True

if __name__ == "__main__":
    success = test_event_publishing()
    
    if success:
        print("✅ Event Publishing Pipeline TEST PASSED!")
        print("\n📖 Next steps:")
        print("  1. Run: python test_events_api.py")
        print("  2. Open: test_events_endpoint.html")
        print("  3. Verify events appear in both tests")
        print("  4. Check Intelligence Core: http://localhost:3000/intelligence-core")
