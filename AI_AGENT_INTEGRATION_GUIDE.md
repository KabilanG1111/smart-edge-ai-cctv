# 🔌 AI AGENT INTEGRATION GUIDE

## Integrating the AI Reasoning Layer into Your CCTV Pipeline

**Target:** Production deployment with ByteTrack, YOLOv8, and FastAPI  
**Difficulty:** Intermediate  
**Time:** 30-60 minutes

---

## 📋 PREREQUISITES

✅ Existing CCTV pipeline with:
- Video ingestion (GStreamer)
- Object detection (YOLOv8)
- Multi-object tracking (ByteTrack)
- Backend API (FastAPI)

✅ Python 3.8+  
✅ NumPy installed  
✅ Threading support

---

## 🚀 QUICK START (5 Minutes)

### Step 1: Import the Agent

```python
from ai_agent import AIReasoningAgent
from datetime import datetime

# Initialize agent
agent = AIReasoningAgent(
    frame_width=1920,
    frame_height=1080,
    fps=30,
    log_dir="./ai_agent_logs",  # Optional: event logging
    verbose=True
)
```

### Step 2: Add Zones (Optional but Recommended)

```python
# Example: Define restricted server room
agent.add_zone(
    zone_id="server_room",
    name="Server Room - Restricted",
    polygon=[(600, 200), (800, 200), (800, 500), (600, 500)],
    zone_type="restricted",
    severity_weight=2.0
)

# Example: Parking lot with crowd limit
agent.add_zone(
    zone_id="parking",
    name="Parking Lot",
    polygon=[(100, 100), (500, 100), (500, 400), (100, 400)],
    zone_type="crowd_limit",
    max_occupancy=50
)

# Example: Entry-only turnstile
agent.add_zone(
    zone_id="entrance",
    name="Building Entrance",
    polygon=[(200, 50), (300, 50), (300, 150), (200, 150)],
    zone_type="entry_only"
)
```

### Step 3: Process Frames

```python
# In your video processing loop
def process_video_frame(frame, yolo_model, bytetrack_tracker):
    # 1. YOLOv8 detection
    detections = yolo_model(frame)
    
    # 2. ByteTrack tracking
    tracked_objects = bytetrack_tracker.update(detections)
    
    # 3. AI Agent reasoning (THIS IS NEW!)
    agent_output = agent.process_frame(
        detections=tracked_objects,  # From ByteTrack
        frame_shape=frame.shape[:2],  # (height, width)
        timestamp=datetime.now()
    )
    
    # 4. Check for critical alerts
    if agent_output['critical_alerts']:
        for alert in agent_output['critical_alerts']:
            print(f"🚨 CRITICAL ALERT: {alert.reason}")
            # Send to alert system, dashboard, etc.
    
    # 5. Use smoothed detections for visualization
    return agent_output['smoothed_detections']
```

**That's it!** The AI Agent is now running in your pipeline.

---

## 📊 FULL INTEGRATION EXAMPLE

### Complete Backend Integration with FastAPI

```python
# backend/main_api.py
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import StreamingResponse
import cv2
import numpy as np
from datetime import datetime
from typing import List, Dict
import logging

# Existing imports
from core.inference_engine import StableInferenceEngine  # Your existing detector
from ai_agent import AIReasoningAgent

logger = logging.getLogger(__name__)

app = FastAPI(title="Enterprise CCTV with AI Agent")

# Initialize your existing detection engine
detection_engine = StableInferenceEngine(
    model_path="yolov8m.pt",
    conf_threshold=0.20
)

# Initialize AI Reasoning Agent (NEW!)
ai_agent = AIReasoningAgent(
    frame_width=1920,
    frame_height=1080,
    fps=30,
    log_dir="./logs/ai_agent",
    verbose=True
)

# Configure zones for your environment
def setup_zones():
    """Define spatial zones for monitoring"""
    
    # Restricted areas
    ai_agent.add_zone(
        zone_id="vault",
        name="Bank Vault",
        polygon=[(500, 300), (700, 300), (700, 600), (500, 600)],
        zone_type="restricted",
        severity_weight=3.0,
        denied_classes={'person'}  # No one allowed
    )
    
    # Time-restricted areas (e.g., office after hours)
    from datetime import time
    ai_agent.add_zone(
        zone_id="office",
        name="Office Area",
        polygon=[(100, 100), (400, 100), (400, 400), (100, 400)],
        zone_type="time_restricted",
        allowed_time_start=time(9, 0),   # 9 AM
        allowed_time_end=time(17, 0),    # 5 PM
        severity_weight=1.5
    )
    
    # Crowd-limited areas
    ai_agent.add_zone(
        zone_id="lobby",
        name="Building Lobby",
        polygon=[(800, 200), (1200, 200), (1200, 800), (800, 800)],
        zone_type="crowd_limit",
        max_occupancy=30
    )
    
    # Entry-only zones
    ai_agent.add_zone(
        zone_id="entry_gate",
        name="Entry Gate",
        polygon=[(50, 500), (150, 500), (150, 600), (50, 600)],
        zone_type="entry_only"
    )
    
    # Exit-only zones
    ai_agent.add_zone(
        zone_id="exit_gate",
        name="Exit Gate",
        polygon=[(1800, 500), (1900, 500), (1900, 600), (1800, 600)],
        zone_type="exit_only"
    )
    
    logger.info("✅ AI Agent zones configured")

# Setup zones on startup
setup_zones()

# Global state for alerts
latest_alerts: List[Dict] = []
alert_lock = threading.Lock()


def gen_frames():
    """Video streaming generator with AI Agent"""
    camera = cv2.VideoCapture(0)  # Or your GStreamer pipeline
    
    frame_count = 0
    
    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            
            frame_count += 1
            timestamp = datetime.now()
            
            # ==========================================
            # EXISTING DETECTION PIPELINE
            # ==========================================
            
            # Run detection + tracking
            detections = detection_engine.process_frame(frame)
            
            # Convert to ByteTrack format
            tracked_objects = []
            for det in detections:
                tracked_objects.append({
                    'track_id': det.get('track_id', 0),
                    'bbox': det['bbox'],  # [x1, y1, x2, y2]
                    'confidence': det['confidence'],
                    'class_name': det['class_name']
                })
            
            # ==========================================
            # AI AGENT REASONING (NEW!)
            # ==========================================
            
            agent_output = ai_agent.process_frame(
                detections=tracked_objects,
                frame_shape=frame.shape[:2],
                timestamp=timestamp
            )
            
            # Extract AI Agent outputs
            smoothed_detections = agent_output['smoothed_detections']
            critical_alerts = agent_output['critical_alerts']
            active_events = agent_output['active_events']
            processing_time = agent_output['processing_time_ms']
            
            # ==========================================
            # ALERT HANDLING
            # ==========================================
            
            if critical_alerts:
                with alert_lock:
                    for alert in critical_alerts:
                        alert_data = {
                            'timestamp': timestamp.isoformat(),
                            'event_type': alert.event_type.value,
                            'severity': alert.severity_score,
                            'reason': alert.reason,
                            'location': alert.location,
                            'zone': alert.zone_id,
                            'evidence': alert.evidence
                        }
                        latest_alerts.append(alert_data)
                        
                        # Log critical alert
                        logger.critical(f"🚨 {alert.reason}")
                        
                        # TODO: Send to alert system (email, SMS, webhook, etc.)
                        # send_alert_notification(alert_data)
            
            # ==========================================
            # VISUALIZATION
            # ==========================================
            
            # Draw smoothed detections (anti-flicker!)
            for det in smoothed_detections:
                bbox = det['bbox']
                x1, y1, x2, y2 = map(int, bbox)
                class_name = det['class_name']
                confidence = det['confidence']
                locked = det.get('class_locked', False)
                
                # Color: Green if locked, Yellow if unlocking
                color = (0, 255, 0) if locked else (0, 255, 255)
                
                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
                # Draw label
                label = f"{class_name} {confidence:.2f}"
                if locked:
                    label += " [LOCK]"
                
                cv2.putText(frame, label, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # Draw zones
            if ai_agent.spatial_engine:
                for zone_id, zone in ai_agent.spatial_engine.zones.items():
                    if zone.active:
                        # Draw zone polygon
                        pts = zone.polygon.astype(np.int32)
                        
                        # Color based on zone type
                        zone_colors = {
                            'restricted': (0, 0, 255),      # Red
                            'time_restricted': (0, 165, 255),  # Orange
                            'entry_only': (255, 255, 0),    # Cyan
                            'exit_only': (255, 0, 255),     # Magenta
                            'crowd_limit': (255, 255, 0),   # Yellow
                            'normal': (0, 255, 0)           # Green
                        }
                        color = zone_colors.get(zone.zone_type.value, (128, 128, 128))
                        
                        cv2.polylines(frame, [pts], True, color, 2)
                        cv2.putText(frame, zone.name, tuple(pts[0]),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Draw event alerts on frame
            if active_events:
                y_offset = 30
                for event in active_events[:5]:  # Show top 5
                    severity_color = (
                        (0, 255, 255) if event.state.value == "MONITORING" else
                        (0, 165, 255) if event.state.value == "WARNING" else
                        (0, 0, 255)   # CRITICAL/SUSPICIOUS
                    )
                    
                    text = f"{event.event_type.value}: {event.state.value}"
                    cv2.putText(frame, text, (10, y_offset),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, severity_color, 2)
                    y_offset += 25
            
            # Draw performance stats
            stats_text = f"AI Agent: {processing_time:.1f}ms | Events: {len(active_events)}"
            cv2.putText(frame, stats_text, (10, frame.shape[0] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Encode frame
            ret, buffer = cv2.imencode('.jpg', frame,
                                      [cv2.IMWRITE_JPEG_QUALITY, 85])
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            # Periodic cleanup (every 5 minutes)
            if frame_count % (fps * 300) == 0:
                ai_agent.cleanup(max_age_seconds=300)
    
    finally:
        camera.release()


@app.get("/video_feed")
async def video_feed():
    """Stream video with AI Agent overlays"""
    return StreamingResponse(
        gen_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.get("/api/alerts")
async def get_alerts():
    """Get latest critical alerts"""
    with alert_lock:
        return {
            "alerts": latest_alerts[-50:],  # Last 50 alerts
            "count": len(latest_alerts)
        }


@app.get("/api/ai-agent/stats")
async def get_ai_agent_stats():
    """Get comprehensive AI Agent statistics"""
    stats = ai_agent.get_comprehensive_stats()
    
    return {
        "status": "operational",
        "statistics": stats,
        "performance": {
            "avg_processing_ms": stats['agent']['avg_processing_time_ms'],
            "frames_processed": stats['agent']['frames_processed'],
            "target_fps": stats['agent']['fps']
        }
    }


@app.get("/api/ai-agent/events")
async def get_active_events():
    """Get all active events"""
    critical = ai_agent.get_critical_alerts()
    
    events = []
    if ai_agent.event_layer:
        for event in ai_agent.event_layer.active_events.values():
            events.append({
                'event_id': event.event_id,
                'type': event.event_type.value,
                'state': event.state.value,
                'severity': event.severity_score,
                'reason': event.reason,
                'duration': event.duration,
                'location': event.location,
                'zone': event.zone_id,
                'evidence': event.evidence
            })
    
    return {
        "active_events": events,
        "critical_count": len(critical)
    }


@app.post("/api/ai-agent/export-report")
async def export_event_report():
    """Export comprehensive event report"""
    filepath = f"./reports/event_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    ai_agent.export_event_report(filepath)
    
    return {
        "message": "Report exported",
        "filepath": filepath
    }


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Shutting down AI Agent...")
    ai_agent.cleanup()
```

---

## 🎨 FRONTEND INTEGRATION

### React Dashboard Component

```typescript
// components/AIAgentDashboard.tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Alert {
  timestamp: string;
  event_type: string;
  severity: number;
  reason: string;
  location: [number, number];
  zone: string;
  evidence: string[];
}

interface Stats {
  agent: {
    frames_processed: number;
    avg_processing_time_ms: number;
  };
  context: {
    active_objects: number;
    loitering_count: number;
  };
  events: {
    total_events_detected: number;
    active_events: number;
    critical_events: number;
  };
}

export const AIAgentDashboard: React.FC = () => {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch alerts
        const alertsRes = await axios.get('/api/alerts');
        setAlerts(alertsRes.data.alerts);

        // Fetch stats
        const statsRes = await axios.get('/api/ai-agent/stats');
        setStats(statsRes.data.statistics);
      } catch (error) {
        console.error('Failed to fetch AI Agent data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 2000); // Update every 2s

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="ai-agent-dashboard">
      <h2>🤖 AI Agent Intelligence</h2>

      {/* Performance Stats */}
      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <h3>Processing Time</h3>
            <p className="stat-value">
              {stats.agent.avg_processing_time_ms.toFixed(1)} ms
            </p>
            <p className="stat-label">
              {stats.agent.avg_processing_time_ms < 25 ? '✅ Optimal' : '⚠️ Slow'}
            </p>
          </div>

          <div className="stat-card">
            <h3>Active Objects</h3>
            <p className="stat-value">{stats.context.active_objects}</p>
            <p className="stat-label">Currently tracking</p>
          </div>

          <div className="stat-card">
            <h3>Active Events</h3>
            <p className="stat-value">{stats.events.active_events}</p>
            <p className="stat-label">
              {stats.events.critical_events} critical
            </p>
          </div>

          <div className="stat-card">
            <h3>Loitering</h3>
            <p className="stat-value">{stats.context.loitering_count}</p>
            <p className="stat-label">Suspicious behavior</p>
          </div>
        </div>
      )}

      {/* Critical Alerts */}
      <div className="alerts-section">
        <h3>🚨 Critical Alerts</h3>
        {alerts.length === 0 ? (
          <p className="no-alerts">No alerts</p>
        ) : (
          <div className="alerts-list">
            {alerts.slice(-10).reverse().map((alert, idx) => (
              <div
                key={idx}
                className={`alert-card severity-${
                  alert.severity >= 0.7 ? 'critical' :
                  alert.severity >= 0.5 ? 'high' : 'medium'
                }`}
              >
                <div className="alert-header">
                  <span className="alert-type">{alert.event_type}</span>
                  <span className="alert-time">
                    {new Date(alert.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <div className="alert-reason">{alert.reason}</div>
                <div className="alert-meta">
                  Zone: {alert.zone || 'Unknown'} | 
                  Severity: {(alert.severity * 100).toFixed(0)}%
                </div>
                {alert.evidence.length > 0 && (
                  <details className="alert-evidence">
                    <summary>Evidence ({alert.evidence.length})</summary>
                    <ul>
                      {alert.evidence.map((ev, i) => (
                        <li key={i}>{ev}</li>
                      ))}
                    </ul>
                  </details>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
```

### CSS Styling

```css
/* styles/AIAgentDashboard.css */
.ai-agent-dashboard {
  padding: 20px;
  background: #1a1a2e;
  color: #eee;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: #16213e;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  color: #0f4c75;
  margin: 10px 0;
}

.stat-label {
  font-size: 0.9rem;
  color: #aaa;
}

.alerts-section {
  margin-top: 30px;
}

.alerts-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.alert-card {
  background: #16213e;
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid;
}

.alert-card.severity-critical {
  border-left-color: #e74c3c;
}

.alert-card.severity-high {
  border-left-color: #f39c12;
}

.alert-card.severity-medium {
  border-left-color: #3498db;
}

.alert-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.alert-type {
  font-weight: bold;
  text-transform: uppercase;
  color: #0f4c75;
}

.alert-reason {
  font-size: 1.1rem;
  margin-bottom: 10px;
}

.alert-meta {
  font-size: 0.85rem;
  color: #aaa;
}

.alert-evidence summary {
  cursor: pointer;
  color: #3498db;
  margin-top: 10px;
}

.alert-evidence ul {
  margin-top: 10px;
  padding-left: 20px;
  font-size: 0.9rem;
}
```

---

## 🔧 CONFIGURATION OPTIONS

### Agent Initialization Options

```python
agent = AIReasoningAgent(
    frame_width=1920,              # Video resolution
    frame_height=1080,
    fps=30,                         # Video frame rate
    
    # Enable/disable specific layers
    enable_context=True,            # Behavioral tracking
    enable_spatial=True,            # Zone monitoring
    enable_temporal=True,           # Anti-flicker
    enable_severity=True,           # Risk scoring
    enable_events=True,             # Pattern detection
    
    # Logging
    log_dir="./logs",               # None = no logging
    verbose=True                    # Debug output
)
```

### Layer-Specific Tuning

```python
# If you need custom thresholds
from ai_agent.context_engine import BehavioralContextEngine
from ai_agent.event_patterns import EventIntelligenceLayer

context_engine = BehavioralContextEngine(
    loitering_threshold=15.0,       # Seconds (default: 10)
    velocity_smoothing=7,            # Frames (default: 5)
    acceleration_threshold=60.0      # px/s² (default: 50)
)

event_layer = EventIntelligenceLayer(
    theft_concealment_time=3.0,     # Seconds (default: 2)
    theft_exit_velocity=100.0,      # px/s (default: 80)
    fight_proximity_threshold=80.0   # Pixels (default: 100)
)

# Then pass to agent (requires modifying agent_core.py)
```

---

## 📊 MONITORING & DEBUGGING

### Enable Debug Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Now all AI Agent layers will output detailed logs
```

### Performance Profiling

```python
import time

def profile_agent_performance():
    """Profile each reasoning layer"""
    
    # Sample frame
    detections = [...]  # Your test detections
    
    times = {}
    
    # Profile temporal layer
    start = time.time()
    smoothed = agent.temporal_layer.update(detections)
    times['temporal'] = (time.time() - start) * 1000
    
    # Profile context engine
    start = time.time()
    obj_states = agent.context_engine.update(smoothed, timestamp, frame_shape)
    times['context'] = (time.time() - start) * 1000
    
    # ... profile other layers ...
    
    print("Layer Performance:")
    for layer, ms in times.items():
        print(f"  {layer}: {ms:.2f} ms")
```

---

## ✅ TESTING CHECKLIST

Before deploying to production:

- [ ] Agent processes frames without errors
- [ ] Processing time < 25ms per frame
- [ ] Zones are correctly defined
- [ ] Alerts are triggered for test scenarios
- [ ] Memory usage stable over 24 hours
- [ ] Event logs are being written correctly
- [ ] Dashboard displays real-time data
- [ ] Alert notifications reach destinations
- [ ] Graceful shutdown without data loss
- [ ] Load testing with multiple cameras

---

## 🐛 TROUBLESHOOTING

### Issue: High CPU Usage

**Solution:** Reduce processing frequency or disable heavy layers

```python
# Process every Nth frame
if frame_count % 2 == 0:  # Process every 2nd frame
    agent_output = agent.process_frame(...)
```

### Issue: Memory Leak

**Solution:** Enable periodic cleanup

```python
# Cleanup old objects every 5 minutes
if frame_count % (fps * 300) == 0:
    agent.cleanup(max_age_seconds=300)
```

### Issue: Too Many Alerts

**Solution:** Adjust severity thresholds

```python
agent.critical_threshold = 0.8  # Only alert on 80%+ severity
agent.severity_engine.weights['duration'] = 0.30  # Increase duration weight
```

---

## 📞 SUPPORT

- **Documentation:** [AI_AGENT_ARCHITECTURE.md](AI_AGENT_ARCHITECTURE.md)
- **Testing:** [AI_AGENT_TESTING_STRATEGY.md](AI_AGENT_TESTING_STRATEGY.md)
- **GitHub Issues:** [Report bugs](https://github.com/your-repo/issues)
- **Email:** ai-agent-support@your-company.com

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-14
