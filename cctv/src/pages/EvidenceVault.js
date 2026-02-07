import React, { useState, useRef, useEffect } from "react";
import "./EvidenceVault.css";

// EXACT REFERENCE MOCK DATA
const MOCK_DATA = [
    {
        id: "EV-2026-8892",
        title: "INTRUSION",
        type: "BIOMETRIC FAIL",
        severity: "CRITICAL",
        time: "14:02:45",
        confidence: 98,
        description: "Unauthorized biocoded entry attempt at Server Room B. Subject unidentified. Security protocols engaged.",
        thumbnailClass: "thumb-crit"
    },
    {
        id: "EV-2026-8891",
        title: "MOTION",
        type: "SECTOR 4",
        severity: "MEDIUM",
        time: "03:15:10",
        confidence: 85,
        description: "Anomalous movement pattern detected during scheduled downtime. Micro-movements suggest personnel.",
        thumbnailClass: "thumb-med"
    },
    {
        id: "EV-2026-8890",
        title: "LOITERING",
        type: "LOADING DOCK",
        severity: "HIGH",
        time: "11:45:22",
        confidence: 92,
        description: "Subject stationary for >300s in active transport zone. Facial recognition scan incomplete due to occlusion.",
        thumbnailClass: "thumb-high"
    },
    {
        id: "EV-2026-8889",
        title: "ROI BREACH",
        type: "PERIMETER N",
        severity: "HIGH",
        time: "09:30:05",
        confidence: 94,
        description: "Virtual fence line crossed by unrecognized vehicle. License plate extraction failed. Manual review required.",
        thumbnailClass: "thumb-high"
    },
    {
        id: "EV-2026-8888",
        title: "ANOMALY",
        type: "MAIN LOBBY",
        severity: "LOW",
        time: "08:12:00",
        confidence: 65,
        description: "Unattended object detected near reception desk. Thermal scan negative. Waiting for personnel check.",
        thumbnailClass: "thumb-low"
    }
];

const FILTERS = ["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"];

const EvidenceVault = () => {
    const [activeFilter, setActiveFilter] = useState("ALL");
    const scrollContainerRef = useRef(null);

    // MOUSE WHEEL HORIZONTAL SCROLL LOGIC
    useEffect(() => {
        const el = scrollContainerRef.current;
        if (el) {
            const onWheel = (e) => {
                // If pure vertical scroll, convert to horizontal
                if (e.deltaY !== 0) {
                    e.preventDefault();
                    el.scrollLeft += e.deltaY;
                }
            };
            el.addEventListener("wheel", onWheel, { passive: false });
            return () => el.removeEventListener("wheel", onWheel);
        }
    }, []);

    const filteredEvents = activeFilter === "ALL" 
        ? MOCK_DATA 
        : MOCK_DATA.filter(ev => ev.severity === activeFilter);

    return (
        <div className="vault-screen">
            {/* 1. HEADER & FILTERS */}
            <header className="vault-top-bar">
                <div className="vault-titles">
                    <h1 className="main-title">EVIDENCE VAULT</h1>
                    <div className="sub-title">AI-FLAGGED SECURITY EVENTS • FORENSIC TIMELINE</div>
                </div>

                <div className="filter-pills">
                    {FILTERS.map(f => (
                        <button 
                            key={f}
                            className={`filter-btn ${activeFilter === f ? 'active' : ''}`}
                            onClick={() => setActiveFilter(f)}
                        >
                            {f}
                        </button>
                    ))}
                </div>
            </header>

            {/* 3. HORIZONTAL SCROLL CONTAINER */}
            <div className="evidence-strip" ref={scrollContainerRef}>
                {filteredEvents.map(ev => (
                    <div key={ev.id} className={`ev-card ${ev.severity}`}>
                        
                        {/* CARD THUMBNAIL AREA */}
                        <div className={`media-area ${ev.thumbnailClass}`}>
                            <div className="rec-indicator">
                                <div className="rec-dot"></div>
                                <span>REC</span>
                            </div>
                            <div className={`severity-badge ${ev.severity}`}>
                                {ev.severity}
                            </div>
                            <div className="overlay-scanline"></div>
                        </div>

                        {/* CARD BODY */}
                        <div className="card-body">
                            <h2 className={`event-title ${ev.severity}`}>{ev.title}</h2>
                            
                            <div className="details-grid">
                                <div className="detail-row">
                                    <label>TYPE</label>
                                    <div className="val">{ev.type}</div>
                                </div>
                                <div className="detail-row">
                                    <label>TIME</label>
                                    <div className="val mono">{ev.time}</div>
                                </div>
                                <div className="detail-row full">
                                    <label>CONFIDENCE</label>
                                    <div className="conf-bar-container">
                                        <div className="conf-track">
                                            <div className="conf-fill" style={{width: `${ev.confidence}%`}}></div>
                                        </div>
                                        <span className="conf-text mono">{ev.confidence}%</span>
                                    </div>
                                </div>
                                <div className="detail-row full">
                                    <label>DESCRIPTION</label>
                                    <p className="desc-block">{ev.description}</p>
                                </div>
                                <div className="detail-row full">
                                    <label>EVENT ID</label>
                                    <div className="val mono id-dim">{ev.id}</div>
                                </div>
                            </div>

                            {/* BOTTOM ACTIONS */}
                            <div className="action-bar">
                                <button className="act-btn">EXPORT</button>
                                <button className="act-btn">ANALYZE</button>
                                <button className="act-btn delete">DELETE</button>
                            </div>
                        </div>
                    </div>
                ))}

                {/* VISUAL PADDING SPACER */}
                <div style={{minWidth: '20px'}}></div>
            </div>
        </div>
    );
};

export default EvidenceVault;