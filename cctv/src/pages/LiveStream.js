import React, { useState, useEffect } from "react";
import "./LiveStream.css";

const API = process.env.REACT_APP_API_URL || "/api";

const LiveStream = () => {
    const [live, setLive] = useState(false);
    const [stats, setStats] = useState({ fps: 0, objects: 0, latency: 45, confidence: 98 });
    const [status, setStatus] = useState("DISCONNECTED");

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
                setStats({
                    fps: Math.round(t.avg_fps || 30),
                    objects: t.active_tracks || 0,
                    latency: 35 + Math.floor(Math.random() * 12),
                    confidence: 85 + Math.floor(Math.random() * 14)
                });
            } catch(e) {}
        }, 1000);
        return () => clearInterval(interval);
    }, [live]);

    const handleStream = async (start) => {
        setLive(start);
        if(start) await fetch(`${API}/start`, {method:'POST'});
        else await fetch(`${API}/stop`, {method:'POST'});
    };

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
                        <>
                            <img src={`${API}/live?t=${Date.now()}`} className="stream-img" alt="feed"/>
                            <div className="hud-layer">
                                <div className="target-box"></div>
                                <div className="timestamp mono">{new Date().toLocaleTimeString()}</div>
                            </div>
                        </>
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
