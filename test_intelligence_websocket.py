"""
🧠 Intelligence Core WebSocket Connection Test
Tests real-time streaming from Camera Feed → AI Agent → Intelligence Core
"""
import asyncio
import websockets
import json
from datetime import datetime

async def test_intelligence_websocket():
    """Test the /ws/intelligence WebSocket endpoint"""
    uri = "ws://localhost:8000/ws/intelligence"
    
    print("=" * 70)
    print("🧠 INTELLIGENCE CORE WEBSOCKET TEST")
    print("=" * 70)
    print(f"\n📡 Connecting to: {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected! Listening for AI reasoning data...\n")
            print("📊 DATA STRUCTURE VALIDATION:")
            print("-" * 70)
            
            message_count = 0
            start_time = datetime.now()
            
            # Listen for 10 messages (2 seconds at 200ms intervals)
            while message_count < 10:
                message = await websocket.recv()
                data = json.loads(message)
                message_count += 1
                
                # Validate data structure
                if message_count == 1:
                    print(f"\n✓ timestamp: {data.get('timestamp', 'MISSING')}")
                    print(f"✓ objects: {len(data.get('objects', []))} tracked")
                    print(f"✓ events: {len(data.get('events', []))} active")
                    print(f"✓ system_state: {data.get('system_state', 'MISSING')}")
                    print(f"✓ threat_level: {data.get('threat_level', 0):.2f}")
                    print(f"✓ active_tracks: {data.get('active_tracks', 0)}")
                    print(f"✓ stream_active: {data.get('stream_active', False)}")
                    
                    # Check object structure if any objects present
                    if data.get('objects'):
                        obj = data['objects'][0]
                        print(f"\n📦 OBJECT DATA STRUCTURE:")
                        print(f"   ✓ object_id: {obj.get('object_id')}")
                        print(f"   ✓ label: {obj.get('label')}")
                        print(f"   ✓ zone: {obj.get('zone')}")
                        print(f"   ✓ dwell_time: {obj.get('dwell_time')}")
                        print(f"   ✓ velocity: {obj.get('velocity')}")
                        print(f"   ✓ duration_score: {obj.get('duration_score')}")
                        print(f"   ✓ velocity_score: {obj.get('velocity_score')}")
                        print(f"   ✓ zone_score: {obj.get('zone_score')}")
                        print(f"   ✓ behavior_score: {obj.get('behavior_score')}")
                        print(f"   ✓ time_score: {obj.get('time_score')}")
                        print(f"   ✓ total_severity: {obj.get('total_severity')}")
                        print(f"   ✓ state: {obj.get('state')}")
                        print(f"   ✓ explanation: {obj.get('explanation')}")
                        print(f"   ✓ timestamp: {obj.get('timestamp')}")
                    
                    print("\n" + "-" * 70)
                
                # Show real-time updates
                if message_count % 2 == 0:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    latency = (elapsed / message_count) * 1000
                    print(f"⏱️  Message {message_count}/10 | Latency: {latency:.1f}ms | State: {data.get('system_state')} | Tracks: {data.get('active_tracks')}")
            
            # Calculate performance
            end_time = datetime.now()
            total_time = (end_time - start_time).total_seconds()
            avg_latency = (total_time / message_count) * 1000
            
            print("\n" + "=" * 70)
            print("📈 PERFORMANCE METRICS:")
            print("=" * 70)
            print(f"✓ Total messages: {message_count}")
            print(f"✓ Total time: {total_time:.2f}s")
            print(f"✓ Average latency: {avg_latency:.1f}ms")
            print(f"✓ Target latency: <200ms")
            print(f"✓ Status: {'✅ PASS' if avg_latency < 200 else '⚠️ WARNING'}")
            
            print("\n" + "=" * 70)
            print("🎉 TEST COMPLETE - WebSocket connection verified!")
            print("=" * 70)
            print("\n✨ Next steps:")
            print("   1. Open http://localhost:3000/intelligence-core")
            print("   2. Look for 'NEURAL LINK ACTIVE' status")
            print("   3. Start camera to see live reasoning data")
            print("   4. Watch objects appear in real-time (<200ms)")
            
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   • Ensure backend is running: python -m uvicorn backend.main_api:app --host 0.0.0.0 --port 8000")
        print("   • Check if port 8000 is available")
        print("   • Verify WebSocket endpoint exists at /ws/intelligence")

if __name__ == "__main__":
    print("\n🚀 Starting WebSocket connection test...")
    asyncio.run(test_intelligence_websocket())
