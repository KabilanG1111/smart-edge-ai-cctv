import React, { useState, useRef, useEffect } from "react";
import { motion, useMotionValue, useTransform, animate } from "framer-motion";
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

// TRI-CARD SPATIAL LAYOUT CONFIGURATION
const LAYOUT_CONFIG = {
    centerScale: 1.0,
    sideScale: 0.88,
    centerOpacity: 1.0,
    sideOpacity: 0.4,
    cardSpacing: 480, // Generous horizontal spacing
    animationDuration: 0.5,
    easing: [0.25, 0.1, 0.25, 1], // Smooth, confident motion
    swipeThreshold: 60,
};

// Calculate transform for tri-card layout
const getCardPosition = (index, activeIndex, totalCards) => {
    const relativePosition = index - activeIndex;
    
    // Only show -1, 0, +1 (left, center, right)
    if (Math.abs(relativePosition) > 1) {
        return { display: false };
    }

    const isCenter = relativePosition === 0;
    const x = relativePosition * LAYOUT_CONFIG.cardSpacing;
    const scale = isCenter ? LAYOUT_CONFIG.centerScale : LAYOUT_CONFIG.sideScale;
    const opacity = isCenter ? LAYOUT_CONFIG.centerOpacity : LAYOUT_CONFIG.sideOpacity;
    const zIndex = isCenter ? 50 : 10 + Math.abs(relativePosition);

    return {
        display: true,
        x,
        scale,
        opacity,
        zIndex,
        isCenter,
    };
};

const EvidenceVault = () => {
    const [activeFilter, setActiveFilter] = useState("ALL");
    const [activeIndex, setActiveIndex] = useState(0);
    const containerRef = useRef(null);

    const filteredEvents = activeFilter === "ALL" 
        ? MOCK_DATA 
        : MOCK_DATA.filter(ev => ev.severity === activeFilter);

    // Navigate cards
    const navigateCard = (direction) => {
        setActiveIndex((prev) => {
            const newIndex = prev + direction;
            if (newIndex < 0) return filteredEvents.length - 1;
            if (newIndex >= filteredEvents.length) return 0;
            return newIndex;
        });
    };

    // Drag interaction
    const handleDragEnd = (event, info) => {
        const dragDistance = info.offset.x;
        
        if (Math.abs(dragDistance) > LAYOUT_CONFIG.swipeThreshold) {
            if (dragDistance > 0) {
                navigateCard(-1); // Swipe right -> previous
            } else {
                navigateCard(1); // Swipe left -> next
            }
        }
    };

    // Keyboard navigation
    useEffect(() => {
        const handleKeyDown = (e) => {
            if (e.key === "ArrowLeft") navigateCard(-1);
            if (e.key === "ArrowRight") navigateCard(1);
        };
        window.addEventListener("keydown", handleKeyDown);
        return () => window.removeEventListener("keydown", handleKeyDown);
    }, [filteredEvents.length]);

    // Mouse wheel navigation
    useEffect(() => {
        const el = containerRef.current;
        if (el) {
            let wheelTimeout;
            const onWheel = (e) => {
                e.preventDefault();
                clearTimeout(wheelTimeout);
                wheelTimeout = setTimeout(() => {
                    if (e.deltaY > 0) {
                        navigateCard(1);
                    } else if (e.deltaY < 0) {
                        navigateCard(-1);
                    }
                }, 50);
            };
            el.addEventListener("wheel", onWheel, { passive: false });
            return () => el.removeEventListener("wheel", onWheel);
        }
    }, [filteredEvents.length]);

    const hasMultipleCards = filteredEvents.length > 1;

    return (
        <div className="vault-screen">
            {/* HEADER & FILTERS */}
            <header className="vault-top-bar">
                <div className="vault-titles">
                    <h1 className="main-title">EVIDENCE VAULT</h1>
                    <div className="sub-title">CLASSIFIED SECURITY EVENTS · FORENSIC INTELLIGENCE</div>
                </div>

                <div className="filter-pills">
                    {FILTERS.map(f => (
                        <button 
                            key={f}
                            className={`filter-btn ${activeFilter === f ? 'active' : ''}`}
                            onClick={() => {
                                setActiveFilter(f);
                                setActiveIndex(0);
                            }}
                        >
                            {f}
                        </button>
                    ))}
                </div>
            </header>

            {/* TRI-CARD SPATIAL LAYOUT */}
            <div className="spatial-vault-container" ref={containerRef}>
                <div className="card-stage">
                    {filteredEvents.map((ev, index) => {
                        const position = getCardPosition(index, activeIndex, filteredEvents.length);
                        
                        if (!position.display) return null;

                        return (
                            <motion.div
                                key={ev.id}
                                className={`ev-card spatial ${ev.severity} ${position.isCenter ? 'center' : 'side'}`}
                                drag={position.isCenter ? "x" : false}
                                dragConstraints={{ left: 0, right: 0 }}
                                dragElastic={0.15}
                                onDragEnd={position.isCenter ? handleDragEnd : undefined}
                                animate={{
                                    x: position.x,
                                    scale: position.scale,
                                    opacity: position.opacity,
                                }}
                                transition={{
                                    duration: LAYOUT_CONFIG.animationDuration,
                                    ease: LAYOUT_CONFIG.easing,
                                }}
                                style={{
                                    zIndex: position.zIndex,
                                }}
                            >
                                {/* CARD THUMBNAIL */}
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

                                    {/* ACTIONS */}
                                    {position.isCenter && (
                                        <div className="action-bar">
                                            <button className="act-btn">EXPORT</button>
                                            <button className="act-btn">ANALYZE</button>
                                            <button className="act-btn delete">DELETE</button>
                                        </div>
                                    )}
                                </div>
                            </motion.div>
                        );
                    })}
                </div>

                {/* MINIMAL NAVIGATION */}
                {hasMultipleCards && (
                    <div className="vault-nav">
                        <button 
                            className="nav-arrow left" 
                            onClick={() => navigateCard(-1)}
                            aria-label="Previous event"
                        >
                            ‹
                        </button>
                        
                        <div className="position-indicator">
                            <span className="current">{String(activeIndex + 1).padStart(2, '0')}</span>
                            <span className="divider">—</span>
                            <span className="total">{String(filteredEvents.length).padStart(2, '0')}</span>
                        </div>

                        <button 
                            className="nav-arrow right" 
                            onClick={() => navigateCard(1)}
                            aria-label="Next event"
                        >
                            ›
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default EvidenceVault;

