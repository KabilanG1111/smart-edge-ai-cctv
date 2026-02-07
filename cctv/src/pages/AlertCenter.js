import React, { useState, useEffect } from "react";
import "./AlertCenter.css";

/* 
   ELITE MOCK DATA GENERATOR 
   Ensures the UI is populated with high-fidelity intelligence data 
   even when the backend is quiet.
*/
const THREAT_TYPES = [
    { title: "UNAUTHORIZED ACCESS", severity: "CRITICAL", agent: "AccessControl.AI" },
    { title: "LOITERING DETECTED", severity: "MEDIUM", agent: "Behavior.Net" },
    { title: "WEAPON SIGNATURE", severity: "CRITICAL", agent: "ObjectRec.V8" },
    { title: "ABANDONED OBJECT", severity: "HIGH", agent: "Anomaly.Detector" },
    { title: "CROWD DENSITY SPIKE", severity: "LOW", agent: "Crowd.Metric" },
    { title: "FORCED ENTRY ATTEMPT", severity: "CRITICAL", agent: "Breach.Analyzer" },
    { title: "PERIMETER BREACH", severity: "HIGH", agent: "Zone.Guardian" },
    { title: "ANOMALOUS MOVEMENT", severity: "MEDIUM", agent: "Motion.Intel" },
];

const ZONES = ["SECTOR 7-A", "LOADING DOCK B", "SERVER ROOM MAIN", "PERIMETER EAST", "MAIN LOBBY", "ELEVATOR BANK C"];

const generateMockThreats = (count = 12) => {
    return Array.from({ length: count }, (_, i) => {
        const type = THREAT_TYPES[Math.floor(Math.random() * THREAT_TYPES.length)];
        const zone = ZONES[Math.floor(Math.random() * ZONES.length)];
        return {
            id: `TH-${207500 + i}`,
            title: type.title,
            severity: type.severity,
            zone: zone,
            timestamp: new Date(Date.now() - Math.floor(Math.random() * 10000000)).toISOString(),
            description: `AI confidence threshold exceeded in ${zone}. Correlation with behavioral baseline indicates deviation. Immediate review recommended.`,
            confidence: 0.85 + Math.random() * 0.14,
            agent: type.agent,
            isLive: i === 0,
            status: i === 0 ? "ACTIVE" : "MONITORING"
        };
    });
};

const MOCK_DATA = generateMockThreats();

const AlertCenter = () => {
    const [threats, setThreats] = useState(MOCK_DATA);
    const [filter, setFilter] = useState("ALL");
    const [selectedThreat, setSelectedThreat] = useState(null);
    const [currentTime, setCurrentTime] = useState(new Date());

    // Live Clock Update
    useEffect(() => {
        const timer = setInterval(() => setCurrentTime(new Date()), 1000);
        return () => clearInterval(timer);
    }, []);

    // Select first threat on load
    useEffect(() => {
        if (threats.length > 0 && !selectedThreat) {
            setSelectedThreat(threats[0]);
        }
    }, [threats, selectedThreat]);

    // Filter Logic
    const filteredThreats = threats.filter(t => 
        filter === "ALL" ? true : t.severity === filter
    );

    // Severity Order for Sorting (Critical first)
    const severityWeight = { CRITICAL: 3, HIGH: 2, MEDIUM: 1, LOW: 0 };
    filteredThreats.sort((a, b) => severityWeight[b.severity] - severityWeight[a.severity]);

    return (
        <div className="alert-master-layout">
            {/* LEFT PANEL: LIST */}
            <div className="alert-list-panel">
                <div className="list-header">
                    <div className="lh-title">
                        <h2>THREAT STREAM</h2>
                        <span className="live-dot"></span>
                    </div>
                </div>
                
                <div className="list-controls">
                     {['ALL', 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].map(f => (
                        <button 
                            key={f}
                            className={`filter-pill ${filter === f ? 'active' : ''} ${f}`}
                            onClick={() => setFilter(f)}
                        >
                            {f}
                        </button>
                    ))}
                </div>

                <div className="list-scroll-area">
                    {filteredThreats.map(threat => (
                        <div 
                            key={threat.id} 
                            className={`alert-item-card ${threat.severity} ${selectedThreat?.id === threat.id ? 'selected' : ''}`}
                            onClick={() => setSelectedThreat(threat)}
                        >
                            <div className="aic-top">
                                <span className={`aic-badge ${threat.severity}`}>{threat.severity}</span>
                                <span className="aic-time">{threat.timestamp.split('T')[1].substr(0,5)}</span>
                            </div>
                            <div className="aic-title">{threat.title}</div>
                            <div className="aic-zone">{threat.zone}</div>
                            <div className="aic-status-row">
                                <span className="aic-status">{threat.status}</span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* RIGHT PANEL: DETAILS */}
            <div className="alert-details-panel">
                {selectedThreat ? (
                    <div className="details-container">
                        {/* HEADER */}
                        <div className="details-header">
                            <div className="dh-left">
                                <div className="dh-id">{selectedThreat.id}</div>
                                <div className="dh-zone">LOCATION: {selectedThreat.zone}</div>
                            </div>
                            <div className="dh-right">
                                <span className="dh-live">LIVE FEED ACTIVE</span>
                            </div>
                        </div>

                        {/* SEVERITY CIRCLE */}
                        <div className="severity-hero">
                            <div className={`sev-circle ${selectedThreat.severity}`}>
                                <div className="sev-ring-1"></div>
                                <div className="sev-ring-2"></div>
                                <div className="sev-text">{selectedThreat.severity}</div>
                            </div>
                        </div>

                        {/* INFO GRID */}
                        <div className="details-grid">
                            <div className="d-card glass">
                                <div className="dc-label">THREAT TYPE</div>
                                <div className="dc-val">{selectedThreat.title}</div>
                            </div>
                             <div className="d-card glass">
                                <div className="dc-label">DETECTED BY</div>
                                <div className="dc-val">{selectedThreat.agent}</div>
                            </div>
                             <div className="d-card glass">
                                <div className="dc-label">CONFIDENCE</div>
                                <div className="dc-val">{(selectedThreat.confidence * 100).toFixed(1)}%</div>
                            </div>
                             <div className="d-card glass">
                                <div className="dc-label">TIMESTAMP</div>
                                <div className="dc-val mono">{selectedThreat.timestamp}</div>
                            </div>
                        </div>

                        <div className="description-box glass">
                            <div className="dc-label">INTELLIGENCE SUMMARY</div>
                            <p>{selectedThreat.description}</p>
                        </div>

                        {/* ACTIONS */}
                        <div className="details-actions">
                            <button className="action-btn dispatch">DISPATCH SECURITY</button>
                            <button className="action-btn review">MARK REVIEWED</button>
                            <button className="action-btn dismiss">DISMISS</button>
                        </div>
                    </div>
                ) : (
                    <div className="empty-details">
                        SELECT AN ALERT TO VIEW INTELLIGENCE
                    </div>
                )}
            </div>
        </div>
    );
};

export default AlertCenter;
