import React, { useState, useEffect, useRef, useCallback } from "react";
import "./DetectionFeed.css";

const API = process.env.REACT_APP_API_URL || "http://localhost:8001/api";

// Emoji map for detected object classes (YOLO COCO 80 classes)
const CLASS_ICONS = {
  person: "🚶", bicycle: "🚲", car: "🚗", motorcycle: "🏍️", airplane: "✈️",
  bus: "🚌", train: "🚆", truck: "🚛", boat: "🚤", bird: "🐦",
  cat: "🐱", dog: "🐕", horse: "🐴", sheep: "🐑", cow: "🐄",
  elephant: "🐘", bear: "🐻", zebra: "🦓", giraffe: "🦒",
  backpack: "🎒", umbrella: "☂️", handbag: "👜", suitcase: "🧳",
  frisbee: "🥏", skis: "🎿", snowboard: "🏂", sports_ball: "⚽",
  "sports ball": "⚽", kite: "🪁", baseball_bat: "🏏", "baseball bat": "🏏",
  "baseball glove": "🧤", skateboard: "🛹", surfboard: "🏄",
  "tennis racket": "🎾", bottle: "🍾", "wine glass": "🍷",
  cup: "☕", fork: "🍴", knife: "🔪", spoon: "🥄", bowl: "🥣",
  banana: "🍌", apple: "🍎", sandwich: "🥪", orange: "🍊",
  broccoli: "🥦", carrot: "🥕", "hot dog": "🌭", pizza: "🍕",
  donut: "🍩", cake: "🎂", chair: "🪑", couch: "🛋️", "potted plant": "🪴",
  bed: "🛏️", "dining table": "🍽️", toilet: "🚽", tv: "📺",
  laptop: "💻", mouse: "🖱️", remote: "📱", keyboard: "⌨️",
  "cell phone": "📲", microwave: "🔲", oven: "🔥", toaster: "🍞",
  sink: "🚰", refrigerator: "🧊", book: "📖", clock: "🕐",
  vase: "🏺", scissors: "✂️", "teddy bear": "🧸", "hair drier": "💨",
  toothbrush: "🪥", "stop sign": "🛑", "parking meter": "🅿️",
  bench: "💺", "fire hydrant": "🧯", "traffic light": "🚦",
};

const getIcon = (cls) => CLASS_ICONS[cls] || "🔍";

// Severity color based on class
const getClassColor = (cls) => {
  if (["person"].includes(cls)) return "var(--cyan-bright)";
  if (["car", "truck", "bus", "motorcycle"].includes(cls)) return "var(--orange-high, #ff9100)";
  if (["dog", "cat", "bird", "cow", "horse", "sheep", "bear", "elephant", "zebra", "giraffe"].includes(cls))
    return "var(--neon-green, #00e676)";
  if (["knife", "scissors"].includes(cls)) return "var(--red-crit, #ff1744)";
  return "#aaa";
};

const DetectionFeed = ({ active }) => {
  const [messages, setMessages] = useState([]);
  const lastTimestamp = useRef(0);
  const feedRef = useRef(null);
  const pollRef = useRef(null);

  // Poll backend for new detections
  const pollDetections = useCallback(async () => {
    if (!active) return;
    try {
      const res = await fetch(`${API}/detections?since=${lastTimestamp.current}`);
      const data = await res.json();
      if (data.detections && data.detections.length > 0) {
        // Update timestamp watermark
        const maxTs = Math.max(...data.detections.map((d) => d.timestamp));
        lastTimestamp.current = maxTs;

        // Convert to messages with unique keys
        const newMsgs = data.detections.map((d) => ({
          id: d.id,
          icon: getIcon(d.class),
          label: d.class.toUpperCase(),
          confidence: d.confidence,
          trackId: d.track_id,
          isNew: d.is_new,
          duration: d.duration,
          color: getClassColor(d.class),
          createdAt: Date.now(), // local time for fade-out timer
        }));

        setMessages((prev) => {
          const merged = [...prev, ...newMsgs];
          // Keep latest 40 messages max
          return merged.slice(-40);
        });
      }
    } catch (e) {
      /* silent */
    }
  }, [active]);

  // Start/stop polling
  useEffect(() => {
    if (active) {
      lastTimestamp.current = Date.now() / 1000 - 5; // start from 5s ago
      pollRef.current = setInterval(pollDetections, 1500);
      return () => clearInterval(pollRef.current);
    } else {
      setMessages([]);
      if (pollRef.current) clearInterval(pollRef.current);
    }
  }, [active, pollDetections]);

  // Auto-remove messages after 60 seconds (fade out)
  useEffect(() => {
    const cleanup = setInterval(() => {
      const now = Date.now();
      setMessages((prev) => prev.filter((m) => now - m.createdAt < 60000));
    }, 5000);
    return () => clearInterval(cleanup);
  }, []);

  // Auto scroll to bottom on new messages
  useEffect(() => {
    if (feedRef.current) {
      feedRef.current.scrollTop = feedRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="detection-feed">
      <div className="feed-header">
        <span className="feed-title">LIVE DETECTIONS</span>
        <span className="feed-dot" />
        <span className="feed-count">{messages.length}</span>
      </div>

      <div className="feed-scroll" ref={feedRef}>
        {messages.length === 0 ? (
          <div className="feed-empty">
            <div className="empty-icon">📡</div>
            <div className="empty-text">Waiting for detections...</div>
          </div>
        ) : (
          messages.map((msg) => {
            const age = Date.now() - msg.createdAt;
            const fading = age > 45000; // start fading at 45s
            return (
              <div
                key={msg.id}
                className={`feed-msg ${msg.isNew ? "is-new" : ""} ${fading ? "fading" : ""}`}
                style={{ "--accent": msg.color }}
              >
                <span className="msg-icon">{msg.icon}</span>
                <div className="msg-body">
                  <span className="msg-label" style={{ color: msg.color }}>
                    {msg.label}
                  </span>
                  <span className="msg-conf">{msg.confidence}%</span>
                </div>
                <span className="msg-track">#{msg.trackId}</span>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default DetectionFeed;
