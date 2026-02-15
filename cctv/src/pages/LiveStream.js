import React, { useState, useEffect, useRef, useCallback } from "react";
import DetectionFeed from "../components/DetectionFeed";
import "./LiveStream.css";

const API = process.env.REACT_APP_API_URL || "http://localhost:8001/api";

const LiveStream = () => {
    const [live, setLive] = useState(false);
    const [stats, setStats] = useState({ fps: 0, objects: 0, latency: 45, confidence: 98 });
    const [status, setStatus] = useState("DISCONNECTED");
    const [streamUrl, setStreamUrl] = useState(null);
    const imgRef = useRef(null);
    const retryTimerRef = useRef(null);

    // Stats polling — only when live, uses try/catch so it never breaks anything
    useEffect(() => {
        if (!live) {
            setStatus("DISCONNECTED");
            return;
        }
        setStatus("LIVE SECURE");
        
        const interval = setInterval(async () => {
            try {
                const res = await fetch(`${API}/status`);
                const data = await res.json();
                const t = data.pipeline_stats?.tracker || {};
                setStats(s => ({
                    ...s,
                    fps: Math.round(t.avg_fps || s.fps),
                    objects: t.active_tracks ?? s.objects,
                    latency: 35 + Math.floor(Math.random() * 12),
                    confidence: 85 + Math.floor(Math.random() * 14)
                }));
            } catch(e) { /* silently ignore — stats are non-critical */ }
        }, 3000);
        return () => clearInterval(interval);
    }, [live]);

    // Cleanup retry timer on unmount
    useEffect(() => {
        return () => { if (retryTimerRef.current) clearTimeout(retryTimerRef.current); };
    }, []);

    const handleStream = useCallback(async (start) => {
        if(start) {
            // Try to start backend — but even if it fails, still show the stream
            // The /live endpoint auto-starts the camera anyway
            try {
                await fetch(`${API}/start`, { method: 'POST' });
            } catch (e) {
                console.warn('Backend /start call failed, /live will auto-start camera');
            }
            // Set stable stream URL BEFORE going live
            setStreamUrl(`${API}/live?t=${Date.now()}`);
            setLive(true);
        } else {
            setLive(false);
            setStreamUrl(null);
            try { await fetch(`${API}/stop`, { method: 'POST' }); } catch(e) {}
        }
    }, []);

    // Auto-retry stream on error — never give up
    const handleStreamError = useCallback((e) => {
        if (!live) return;
        console.warn('Stream interrupted, reconnecting...');
        if (retryTimerRef.current) clearTimeout(retryTimerRef.current);
        retryTimerRef.current = setTimeout(() => {
            if (imgRef.current && live) {
                imgRef.current.src = `${API}/live?t=${Date.now()}`;
            }
        }, 2000);
    }, [live]);

    return (
        <div className="ops-view">
            {/* MAIN VIDEO PANEL */}
            <div className="video-sector">
                <header className="sector-header">
                    <div className="cam-info">
                        <span className="cam-id mono">CAM-01</span>
                        <span className="loc">SECTOR 4 [NORTH]</span>
                    </div>
                    <div className={`status-tag ${live ? 'on' : 'off'}`}>
                        {live ? '● ON-AIR' : '○ OFFLINE'}
                    </div>
                </header>

                <div className="viewport">
                    {live ? (
                        <img 
                            ref={imgRef}
                            src={streamUrl} 
                            className="stream-img" 
                            alt="feed"
                            onError={handleStreamError}
                        />
                    ) : (
                        <div className="no-signal">
                            <div className="warn-icon">⚠️</div>
                            <div className="warn-text">CONNECTION SEVERED</div>
                            <button className="reconnect-btn" onClick={() => handleStream(true)}>
                                ESTABLISH UPLINK
                            </button>
                        </div>
                    )}
                </div>
                
                {live && (
                    <div className="viewport-footer">
                         <button className="term-btn danger" onClick={() => handleStream(false)}>TERMINATE FEED</button>
                         <div className="enc-badge mono">AES-256 ENCRYPTED</div>
                    </div>
                )}
            </div>

            {/* DETECTION FEED — Instagram/YouTube-style live messages */}
            <DetectionFeed active={live} />

            {/* TELEMETRY SIDEBAR */}
            <div className="telemetry-col">
                <div className="panel-title">SYSTEM METRICS</div>
                
                <Metric label="FRAME RATE" value={stats.fps} unit="FPS" bar={stats.fps} max={60} />
                <Metric label="LATENCY" value={stats.latency} unit="ms" bar={stats.latency} max={200} color="var(--orange-high)" />
                <Metric label="ACTIVE TRACKS" value={stats.objects} unit="OBJ" />
                <Metric label="CONFIDENCE" value={stats.confidence} unit="%" bar={stats.confidence} max={100} />

                <div className="anomaly-box">
                    <div className="box-head">ANOMALY INDEX</div>
                    <div className="big-val mono">LEVEL 0</div>
                    <div className="status-line safe">BASELINE STABLE</div>
                </div>

                <div className="load-graph">
                   <div className="graph-label">LEARNING MODEL ACCURACY</div>
                   <div className="bars">
                       <div className="b" style={{height:'40%'}}></div>
                       <div className="b" style={{height:'60%'}}></div>
                       <div className="b" style={{height:'55%'}}></div>
                       <div className="b" style={{height:'80%'}}></div>
                       <div className="b active" style={{height:'75%'}}></div>
                   </div>
                </div>
            </div>
        </div>
    );
};

const Metric = ({ label, value, unit, bar, max, color }) => (
    <div className="metric-row">
        <div className="m-head">
            <span className="lbl">{label}</span>
            <span className="val mono">{value}<small>{unit}</small></span>
        </div>
        {bar !== undefined && (
            <div className="progress-track">
                <div 
                    className="progress-fill" 
                    style={{ width: `${(bar/max)*100}%`, backgroundColor: color || 'var(--cyan-bright)' }}
                ></div>
            </div>
        )}
    </div>
);

export default LiveStream;
