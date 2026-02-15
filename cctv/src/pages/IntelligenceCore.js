import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './IntelligenceCore.css';

const IntelligenceCore = () => {
    const [reasoningData, setReasoningData] = useState(null);
    const [lastActiveData, setLastActiveData] = useState(null); // Persist last active state
    const [isLiveData, setIsLiveData] = useState(false); // Track if data is live or historical
    const [lastActiveTime, setLastActiveTime] = useState(null); // When was last activity
    const [eventLog, setEventLog] = useState([]);
    const [reasoningEvents, setReasoningEvents] = useState([]); // 🎯 NEW: Structured reasoning events
    const [isConnected, setIsConnected] = useState(false);
    const [isReasoningConnected, setIsReasoningConnected] = useState(false); // 🧠 NEW: Reasoning engine connection
    const [lastUpdateTime, setLastUpdateTime] = useState(new Date());
    const wsRef = useRef(null);
    const reasoningWsRef = useRef(null); // 🧠 NEW: Reasoning WebSocket ref
    const logRef = useRef(null);

    // WebSocket connection for real-time reasoning stream
    useEffect(() => {
        const connectWebSocket = () => {
            // PRIMARY endpoint: /ws/intelligence (production-grade streaming)
            const ws = new WebSocket('ws://localhost:8001/ws/intelligence');
            
            ws.onopen = () => {
                console.log('🧠 Intelligence Core connected - real-time reasoning active');
                setIsConnected(true);
            };
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                
                // Update last update timestamp
                setLastUpdateTime(new Date());
                
                // 🔥 PERSISTENCE LOGIC: Detect if this is live or idle data
                const hasActiveData = data.active_tracks > 0 || data.system_state !== 'IDLE';
                
                if (hasActiveData) {
                    // Live data detected - update both current and last active
                    setIsLiveData(true);
                    setLastActiveTime(new Date());
                    setLastActiveData(data); // Save for persistence
                    setReasoningData(data);
                    
                    // Log critical threats
                    if (data.threat_level > 0.75) {
                        console.log(`⚠️ CRITICAL: ${data.active_tracks} tracks | ${(data.threat_level * 100).toFixed(0)}% threat`);
                    } else if (data.active_tracks > 0) {
                        console.log(`🎯 LIVE DATA: ${data.active_tracks} tracks | ${(data.threat_level * 100).toFixed(0)}% threat`);
                    }
                } else {
                    // IDLE state - check if we have historical data to display
                    const storedData = lastActiveData || JSON.parse(localStorage.getItem('intelligence_core_last_active') || 'null');
                    
                    if (storedData && storedData.active_tracks > 0) {
                        setIsLiveData(false);
                        setLastActiveData(storedData);
                        setReasoningData(storedData); // Show historical data
                        console.log('📊 Showing historical data (camera idle)');
                    } else {
                        // No historical data available, show idle
                        setReasoningData(data);
                    }
                }
                
                // Add to event log if there are new events or threats
                if (hasActiveData && (data.events?.length > 0 || data.critical_count > 0)) {
                    const newLog = {
                        id: Date.now() + Math.random(), // Ensure unique IDs
                        timestamp: new Date().toLocaleTimeString(),
                        type: data.system_state,
                        message: generateLogMessage(data),
                        severity: data.threat_level
                    };
                    
                    setEventLog(prev => [newLog, ...prev].slice(0, 100)); // Max 100 entries
                }
            };
            
            ws.onerror = (error) => {
                console.error('❌ Intelligence WebSocket error:', error);
                setIsConnected(false);
            };
            
            ws.onclose = () => {
                console.log('🔄 WebSocket closed, reconnecting in 2s...');
                setIsConnected(false);
                setTimeout(connectWebSocket, 2000);
            };
            
            wsRef.current = ws;
        };
        
        connectWebSocket();
        
        return () => {
            if (wsRef.current) {
                wsRef.current.close();
            }
        };
    }, []);

    // 🧠 REAL-TIME REASONING ENGINE: WebSocket connection to reasoning engine
    useEffect(() => {
        const connectReasoningWebSocket = () => {
            // NEW: Real-time reasoning engine endpoint
            const ws = new WebSocket('ws://localhost:8001/ws/reasoning');
            
            ws.onopen = () => {
                console.log('🧠 Reasoning Engine connected - real-time analysis active');
                setIsReasoningConnected(true);
            };
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                
                // Handle initial connection message
                if (data.status === 'connected') {
                    console.log('✅ Reasoning engine ready:', data.message);
                    return;
                }
                
                // Process reasoning events
                if (data.events && Array.isArray(data.events)) {
                    const transformedEvents = data.events.map((event, index) => ({
                        id: `reasoning_${event.track_id}_${event.timestamp}_${index}`,
                        timestamp: new Date(event.timestamp * 1000).toLocaleTimeString(),
                        type: event.class_name ? event.class_name.toUpperCase() : 'DETECTION',
                        message: event.message,
                        severity: event.severity === 'CRITICAL' ? 0.9 : event.severity === 'WARNING' ? 0.6 : 0.3,
                        severityLevel: event.severity, // CRITICAL, WARNING, NORMAL
                        color: event.color, // red, yellow, cyan
                        trackId: event.track_id,
                        metadata: event.metadata || {}
                    }));
                    
                    // Update reasoning events state
                    setReasoningEvents(prev => [...transformedEvents, ...prev].slice(0, 50));
                    
                    // Merge into event log (avoid duplicates)
                    setEventLog(prev => {
                        const existingIds = new Set(prev.map(e => e.id));
                        const newEvents = transformedEvents.filter(e => !existingIds.has(e.id));
                        
                        if (newEvents.length > 0) {
                            console.log(`🧠 ${newEvents.length} new reasoning event(s):`, 
                                        newEvents.map(e => e.message).join('; '));
                        }
                        
                        return [...newEvents, ...prev].slice(0, 100);
                    });
                    
                    // Update last active time when new events arrive
                    if (transformedEvents.length > 0) {
                        setLastActiveTime(new Date());
                        setIsLiveData(true);
                    }
                }
            };
            
            ws.onerror = (error) => {
                console.error('❌ Reasoning WebSocket error:', error);
                setIsReasoningConnected(false);
            };
            
            ws.onclose = () => {
                console.log('🔄 Reasoning WebSocket closed, reconnecting in 3s...');
                setIsReasoningConnected(false);
                setTimeout(connectReasoningWebSocket, 3000);
            };
            
            reasoningWsRef.current = ws;
        };
        
        connectReasoningWebSocket();
        
        return () => {
            if (reasoningWsRef.current) {
                reasoningWsRef.current.close();
            }
        };
    }, []);

    // Load persisted data from localStorage on mount
    useEffect(() => {
        try {
            const savedData = localStorage.getItem('intelligence_core_last_active');
            const savedTime = localStorage.getItem('intelligence_core_last_active_time');
            const savedEventLog = localStorage.getItem('intelligence_core_event_log');
            
            if (savedData) {
                const parsed = JSON.parse(savedData);
                setLastActiveData(parsed);
                setReasoningData(parsed);
                setIsLiveData(false);
                console.log('📦 Restored historical data from localStorage');
            }
            
            if (savedTime) {
                setLastActiveTime(new Date(savedTime));
            }
            
            if (savedEventLog) {
                setEventLog(JSON.parse(savedEventLog));
            }
        } catch (error) {
            console.error('Failed to load persisted data:', error);
        }
    }, []);

    // Save active data to localStorage whenever it updates
    useEffect(() => {
        if (lastActiveData && lastActiveData.active_tracks > 0) {
            try {
                localStorage.setItem('intelligence_core_last_active', JSON.stringify(lastActiveData));
                if (lastActiveTime) {
                    localStorage.setItem('intelligence_core_last_active_time', lastActiveTime.toISOString());
                }
                localStorage.setItem('intelligence_core_event_log', JSON.stringify(eventLog.slice(0, 20))); // Save last 20 events
            } catch (error) {
                console.error('Failed to save data to localStorage:', error);
            }
        }
    }, [lastActiveData, lastActiveTime, eventLog]);

    // 🎯 REAL-TIME BEHAVIOR REASONING: Poll /api/intelligence/live every 500ms
    useEffect(() => {
        const fetchReasoningEvents = async () => {
            try {
                const response = await fetch('http://localhost:8001/api/intelligence/live?limit=50');
                const data = await response.json();
                
                if (data.status === 'active' && data.events && data.events.length > 0) {
                    // Transform backend events to eventLog format
                    const transformedEvents = data.events.map((event, index) => ({
                        id: `${event.track_id}_${event.event_type}_${event.timestamp}_${index}`,
                        timestamp: new Date(event.timestamp).toLocaleTimeString(),
                        type: event.event_type, // LOITERING, RUNNING, FIGHTING, INTRUSION
                        message: event.reasoning,
                        severity: Math.min(event.velocity / 200.0, 1.0), // Normalize velocity for progress bar
                        severityLevel: event.severity, // NORMAL, WARNING, CRITICAL
                        trackId: event.track_id,
                        duration: event.duration,
                        velocity: event.velocity
                    }));
                    
                    setReasoningEvents(transformedEvents);
                    
                    // Merge with existing event log (avoid duplicates by ID)
                    setEventLog(prev => {
                        const existingIds = new Set(prev.map(e => e.id));
                        const newEvents = transformedEvents.filter(e => !existingIds.has(e.id));
                        
                        if (newEvents.length > 0) {
                            console.log(`🔔 ${newEvents.length} new live reasoning event(s)`);
                        }
                        
                        return [...newEvents, ...prev].slice(0, 100); // Keep max 100
                    });
                }
            } catch (error) {
                console.error('Failed to fetch live reasoning:', error);
            }
        };
        
        // Initial fetch
        fetchReasoningEvents();
        
        // Poll every 500ms for real-time updates
        const pollInterval = setInterval(fetchReasoningEvents, 500);
        
        return () => clearInterval(pollInterval);
    }, []);

    // Auto-scroll event log
    useEffect(() => {
        if (logRef.current) {
            logRef.current.scrollTop = 0;
        }
    }, [eventLog]);

    const generateLogMessage = (data) => {
        if (data.critical_count > 0) {
            return `🚨 ${data.critical_count} CRITICAL THREAT${data.critical_count > 1 ? 'S' : ''} DETECTED`;
        }
        if (data.events?.length > 0) {
            const event = data.events[0];
            return `⚡ ${event.type.replace('_', ' ')} - ${event.reason}`;
        }
        if (data.system_state === 'MONITORING' && data.objects?.length > 0) {
            return `👁️ Tracking ${data.objects.length} object${data.objects.length > 1 ? 's' : ''}`;
        }
        return '✓ All systems nominal';
    };

    const getStateColor = (state) => {
        switch (state) {
            case 'CRITICAL': return '#ff0055';
            case 'WARNING': return '#ff9100';
            case 'MONITORING': return '#00d9ff';
            default: return '#00ff88';
        }
    };

    const getSeverityColor = (severity) => {
        if (typeof severity === 'string') {
            // Handle severity level strings (LOW, MEDIUM, HIGH, CRITICAL)
            switch (severity.toUpperCase()) {
                case 'CRITICAL': return '#ff0055';
                case 'HIGH': return '#ff4400';
                case 'MEDIUM': return '#ff9100';
                case 'LOW': return '#00ff88';
                default: return '#00d9ff';
            }
        } else {
            // Handle severity scores (0.0-1.0)
            if (severity >= 0.75) return '#ff0055'; // CRITICAL
            if (severity >= 0.50) return '#ff4400'; // HIGH
            if (severity >= 0.25) return '#ff9100'; // MEDIUM
            return '#00ff88'; // LOW
        }
    };

    const getSeverityClass = (severity) => {
        if (severity >= 0.7) return 'critical';
        if (severity >= 0.5) return 'high';
        if (severity >= 0.3) return 'medium';
        return 'low';
    };

    // Generate AI reasoning summary sentence
    const generateAIReasoningSummary = () => {
        if (!reasoningData) return 'Initializing neural network...';
        
        const { system_state, active_tracks, threat_level, events, critical_count } = reasoningData;
        
        if (system_state === 'CRITICAL' && critical_count > 0) {
            return `Critical threat detected! ${critical_count} object${critical_count > 1 ? 's' : ''} exhibiting high-risk behavior patterns requiring immediate attention.`;
        }
        
        if (system_state === 'WARNING' && threat_level >= 0.5) {
            return `Elevated threat posture detected. AI monitoring ${active_tracks} track${active_tracks > 1 ? 's' : ''} with ${(threat_level * 100).toFixed(0)}% severity assessment.`;
        }
        
        if (system_state === 'MONITORING' && active_tracks > 0) {
            const highestSeverity = reasoningData.objects?.length > 0 
                ? Math.max(...reasoningData.objects.map(obj => obj.total_severity || obj.severity_breakdown?.total_severity || 0))
                : 0;
            
            if (highestSeverity > 0.3) {
                return `Active surveillance of ${active_tracks} object${active_tracks > 1 ? 's' : ''}. Behavioral analysis indicates ${(highestSeverity * 100).toFixed(0)}% anomaly score.`;
            }
            return `Tracking ${active_tracks} object${active_tracks > 1 ? 's' : ''} with nominal behavioral patterns. All zones secure.`;
        }
        
        if (events?.length > 0) {
            const event = events[0];
            return `Event detected: ${event.type.replace('_', ' ')} - ${event.reason}`;
        }
        
        return 'All systems nominal. Neural network standing by for detection events.';
    };

    // Get highest severity and last event
    const getHighestSeverity = () => {
        if (!reasoningData || !reasoningData.objects || reasoningData.objects.length === 0) {
            return 0;
        }
        return Math.max(...reasoningData.objects.map(obj => obj.total_severity || obj.severity_breakdown?.total_severity || 0));
    };

    const getLastEventType = () => {
        if (eventLog.length > 0) {
            return eventLog[0].message;
        }
        if (reasoningData?.events?.length > 0) {
            return reasoningData.events[0].type.replace('_', ' ').toUpperCase();
        }
        return 'None';
    };

    return (
        <div className="intelligence-core">
            {/* Header */}
            <div className="core-header">
                <div className="header-left">
                    <div className="core-logo">
                        <div className="pulse-ring"></div>
                        <div className="logo-center">🧠</div>
                    </div>
                    <div className="header-text">
                        <h1>AI INTELLIGENCE CORE</h1>
                        <p>Multi-Layer Reasoning Engine</p>
                    </div>
                </div>
                
                <div className="header-right">
                    <div className={`status-indicator ${isConnected && isReasoningConnected ? 'connected' : 'disconnected'}`}>
                        <div className="status-dot"></div>
                        <span>{isConnected && isReasoningConnected ? 'NEURAL LINK + REASONING ACTIVE' : 'RECONNECTING...'}</span>
                    </div>
                    {reasoningData && (
                        <div className="processing-stats">
                            <div className="stat">
                                <span className="stat-label">LATENCY</span>
                                <span className="stat-value">{reasoningData.processing_time_ms?.toFixed(1) || 0}ms</span>
                            </div>
                            <div className="stat">
                                <span className="stat-label">FRAME</span>
                                <span className="stat-value">{reasoningData.frame_count || 0}</span>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Live AI Summary Panel */}
            <motion.div 
                className="ai-summary-panel"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, ease: "easeOut" }}
            >
                <div className="summary-header">
                    <div className="summary-title">
                        <span className="summary-icon">⚡</span>
                        <h3>{isLiveData ? 'LIVE AI REASONING SUMMARY' : 'AI REASONING SUMMARY (HISTORICAL)'}</h3>
                    </div>
                    <div className="summary-timestamp">
                        <span className="timestamp-label">{isLiveData ? 'LAST UPDATE' : 'LAST ACTIVE'}</span>
                        <motion.span 
                            className="timestamp-value"
                            key={lastUpdateTime.getTime()}
                            initial={{ scale: 1.2, color: '#00d9ff' }}
                            animate={{ scale: 1, color: isLiveData ? '#00ff88' : '#ff9100' }}
                            transition={{ duration: 0.3 }}
                        >
                            {(isLiveData ? lastUpdateTime : (lastActiveTime || lastUpdateTime)).toLocaleTimeString()}
                        </motion.span>
                    </div>
                </div>

                {/* Historical Data Indicator */}
                {!isLiveData && lastActiveData && (
                    <motion.div 
                        className="historical-indicator"
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        transition={{ duration: 0.4 }}
                    >
                        <div className="historical-content">
                            <span className="historical-icon">📊</span>
                            <span className="historical-text">
                                Displaying last recorded data - Camera not currently active
                            </span>
                            <span className="historical-badge">HISTORICAL</span>
                        </div>
                    </motion.div>
                )}

                <div className="summary-metrics">
                    {/* Active Tracks */}
                    <motion.div 
                        className="metric-card"
                        whileHover={{ scale: 1.05, borderColor: '#00d9ff' }}
                        transition={{ duration: 0.2 }}
                    >
                        <div className="metric-icon">👁️</div>
                        <div className="metric-content">
                            <div className="metric-label">ACTIVE TRACKS</div>
                            <motion.div 
                                className="metric-value"
                                key={reasoningData?.active_tracks || 0}
                                initial={{ scale: 1.3, color: '#00d9ff' }}
                                animate={{ scale: 1, color: '#ffffff' }}
                                transition={{ duration: 0.4, type: "spring" }}
                            >
                                {reasoningData?.active_tracks || 0}
                            </motion.div>
                        </div>
                        <div className="metric-pulse"></div>
                    </motion.div>

                    {/* Highest Severity */}
                    <motion.div 
                        className={`metric-card severity-${getSeverityClass(getHighestSeverity())}`}
                        whileHover={{ scale: 1.05, borderColor: getStateColor(reasoningData?.system_state || 'IDLE') }}
                        transition={{ duration: 0.2 }}
                    >
                        <div className="metric-icon">🎯</div>
                        <div className="metric-content">
                            <div className="metric-label">HIGHEST SEVERITY</div>
                            <motion.div 
                                className="metric-value"
                                key={getHighestSeverity()}
                                initial={{ scale: 1.3, opacity: 0.5 }}
                                animate={{ scale: 1, opacity: 1 }}
                                transition={{ duration: 0.4, type: "spring" }}
                            >
                                {(getHighestSeverity() * 100).toFixed(0)}%
                            </motion.div>
                        </div>
                        <motion.div 
                            className="metric-severity-bar"
                            initial={{ width: 0 }}
                            animate={{ width: `${getHighestSeverity() * 100}%` }}
                            transition={{ duration: 0.8, ease: "easeOut" }}
                            style={{ background: getStateColor(reasoningData?.system_state || 'IDLE') }}
                        ></motion.div>
                    </motion.div>

                    {/* Last Event */}
                    <motion.div 
                        className="metric-card event-card"
                        whileHover={{ scale: 1.05, borderColor: '#7b2ff7' }}
                        transition={{ duration: 0.2 }}
                    >
                        <div className="metric-icon">📡</div>
                        <div className="metric-content">
                            <div className="metric-label">LAST EVENT</div>
                            <AnimatePresence mode="wait">
                                <motion.div 
                                    className="metric-value event-text"
                                    key={getLastEventType()}
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: 10 }}
                                    transition={{ duration: 0.3 }}
                                >
                                    {getLastEventType()}
                                </motion.div>
                            </AnimatePresence>
                        </div>
                        <div className="metric-pulse"></div>
                    </motion.div>

                    {/* System State */}
                    <motion.div 
                        className={`metric-card state-card state-${reasoningData?.system_state?.toLowerCase() || 'idle'}`}
                        whileHover={{ scale: 1.05 }}
                        transition={{ duration: 0.2 }}
                    >
                        <div className="metric-icon">🛡️</div>
                        <div className="metric-content">
                            <div className="metric-label">SYSTEM STATE</div>
                            <AnimatePresence mode="wait">
                                <motion.div 
                                    className="metric-value"
                                    key={reasoningData?.system_state || 'IDLE'}
                                    initial={{ scale: 1.2, opacity: 0 }}
                                    animate={{ scale: 1, opacity: 1 }}
                                    exit={{ scale: 0.8, opacity: 0 }}
                                    transition={{ duration: 0.3 }}
                                    style={{ color: getStateColor(reasoningData?.system_state || 'IDLE') }}
                                >
                                    {reasoningData?.system_state || 'IDLE'}
                                </motion.div>
                            </AnimatePresence>
                        </div>
                        <motion.div 
                            className="metric-state-indicator"
                            animate={{ 
                                boxShadow: `0 0 20px ${getStateColor(reasoningData?.system_state || 'IDLE')}`,
                                backgroundColor: getStateColor(reasoningData?.system_state || 'IDLE')
                            }}
                            transition={{ duration: 0.5 }}
                        ></motion.div>
                    </motion.div>
                </div>

                {/* AI Reasoning Summary Text */}
                <motion.div 
                    className="summary-reasoning"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.3, duration: 0.5 }}
                >
                    <div className="reasoning-header">
                        <span className="reasoning-icon">🧠</span>
                        <span className="reasoning-title">AI ASSESSMENT</span>
                    </div>
                    <AnimatePresence mode="wait">
                        <motion.p 
                            className="reasoning-text"
                            key={generateAIReasoningSummary()}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            transition={{ duration: 0.5 }}
                        >
                            {generateAIReasoningSummary()}
                        </motion.p>
                    </AnimatePresence>
                </motion.div>
            </motion.div>

            {/* Main Content Grid */}
            <div className="core-grid">
                {/* Left Column - Object Tracking */}
                <div className="grid-section tracking-section">
                    <div className="section-header">
                        <h2>ACTIVE TRACKING</h2>
                        <div className="badge">{reasoningData?.active_tracks || 0}</div>
                    </div>
                    
                    <div className="tracking-list">
                        {reasoningData?.objects?.length > 0 ? (
                            reasoningData.objects.map((obj) => (
                                <div key={obj.object_id} className={`tracking-card ${getSeverityClass(obj.severity_breakdown.total_severity)}`}>
                                    <div className="card-header">
                                        <div className="object-id">#{obj.object_id}</div>
                                        <div className="object-class">{obj.class.toUpperCase()}</div>
                                        <div className={`threat-badge ${obj.is_threat ? 'threat' : 'safe'}`}>
                                            {obj.is_threat ? '⚠️ THREAT' : '✓ SAFE'}
                                        </div>
                                    </div>
                                    
                                    <div className="card-body">
                                        <div className="info-row">
                                            <span className="label">ZONE</span>
                                            <span className="value">{obj.zone}</span>
                                        </div>
                                        <div className="info-row">
                                            <span className="label">DWELL</span>
                                            <span className="value">{obj.dwell_time}s</span>
                                        </div>
                                        <div className="info-row">
                                            <span className="label">VELOCITY</span>
                                            <span className="value">{obj.velocity.toFixed(0)} px/s</span>
                                        </div>
                                        <div className="info-row">
                                            <span className="label">STATE</span>
                                            <span className="value state-badge">{obj.state}</span>
                                        </div>
                                    </div>
                                    
                                    <div className="severity-micro">
                                        <div className="severity-bar">
                                            <div 
                                                className="severity-fill"
                                                style={{ 
                                                    width: `${obj.severity_breakdown.total_severity * 100}%`,
                                                    background: getStateColor(obj.state_machine)
                                                }}
                                            ></div>
                                        </div>
                                        <span className="severity-value">{(obj.severity_breakdown.total_severity * 100).toFixed(0)}%</span>
                                    </div>
                                </div>
                            ))
                        ) : (
                            <div className="empty-state">
                                <div className="empty-icon">👁️</div>
                                <p>No active tracks</p>
                                <span>Awaiting detection...</span>
                            </div>
                        )}
                    </div>
                </div>

                {/* Center Column - Severity Analysis */}
                <div className="grid-section analysis-section">
                    <div className="section-header">
                        <h2>SEVERITY ANALYSIS</h2>
                    </div>
                    
                    {reasoningData?.objects?.[0] ? (
                        <div className="analysis-content">
                            <div className="target-card">
                                <div className="target-header">
                                    <span className="target-label">PRIMARY TARGET</span>
                                    <span className="target-id">#{reasoningData.objects[0].object_id}</span>
                                </div>
                                
                                {/* Radar Chart */}
                                <div className="severity-radar">
                                    <svg viewBox="0 0 200 200" className="radar-svg">
                                        {/* Background circles */}
                                        <circle cx="100" cy="100" r="80" fill="none" stroke="rgba(0, 217, 255, 0.1)" strokeWidth="1"/>
                                        <circle cx="100" cy="100" r="60" fill="none" stroke="rgba(0, 217, 255, 0.1)" strokeWidth="1"/>
                                        <circle cx="100" cy="100" r="40" fill="none" stroke="rgba(0, 217, 255, 0.1)" strokeWidth="1"/>
                                        <circle cx="100" cy="100" r="20" fill="none" stroke="rgba(0, 217, 255, 0.1)" strokeWidth="1"/>
                                        
                                        {/* Axes */}
                                        <line x1="100" y1="100" x2="100" y2="20" stroke="rgba(0, 217, 255, 0.2)" strokeWidth="1"/>
                                        <line x1="100" y1="100" x2="176" y2="138" stroke="rgba(0, 217, 255, 0.2)" strokeWidth="1"/>
                                        <line x1="100" y1="100" x2="24" y2="138" stroke="rgba(0, 217, 255, 0.2)" strokeWidth="1"/>
                                        <line x1="100" y1="100" x2="148" y2="56" stroke="rgba(0, 217, 255, 0.2)" strokeWidth="1"/>
                                        <line x1="100" y1="100" x2="52" y2="56" stroke="rgba(0, 217, 255, 0.2)" strokeWidth="1"/>
                                        
                                        {/* Data polygon */}
                                        <polygon
                                            points={calculateRadarPoints(reasoningData.objects[0].severity_breakdown)}
                                            fill="rgba(0, 217, 255, 0.2)"
                                            stroke="#00d9ff"
                                            strokeWidth="2"
                                        />
                                        
                                        {/* Center circle */}
                                        <circle cx="100" cy="100" r="3" fill="#00d9ff"/>
                                    </svg>
                                    
                                    {/* Labels */}
                                    <div className="radar-labels">
                                        <div className="label-item" style={{top: '5%', left: '50%', transform: 'translateX(-50%)'}}>VELOCITY</div>
                                        <div className="label-item" style={{top: '25%', right: '5%'}}>ZONE</div>
                                        <div className="label-item" style={{bottom: '25%', right: '5%'}}>BEHAVIOR</div>
                                        <div className="label-item" style={{bottom: '25%', left: '5%'}}>TIME</div>
                                        <div className="label-item" style={{top: '25%', left: '5%'}}>DWELL</div>
                                    </div>
                                </div>
                                
                                {/* Factor Breakdown */}
                                <div className="factor-breakdown">
                                    {Object.entries(reasoningData.objects[0].severity_breakdown).map(([key, value]) => {
                                        if (key === 'total_severity') return null;
                                        return (
                                            <div key={key} className="factor-row">
                                                <span className="factor-label">{key.replace('_score', '').toUpperCase()}</span>
                                                <div className="factor-bar">
                                                    <div 
                                                        className="factor-fill"
                                                        style={{ width: `${value * 100}%` }}
                                                    ></div>
                                                </div>
                                                <span className="factor-value">{(value * 100).toFixed(0)}%</span>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                            
                            {/* State Machine */}
                            <div className="state-machine">
                                <div className="state-title">STATE MACHINE</div>
                                <div className="states-flow">
                                    <div className={`state-node ${reasoningData.objects[0].state_machine === 'LOW' ? 'active' : ''}`}>NORMAL</div>
                                    <div className="state-arrow">→</div>
                                    <div className={`state-node ${reasoningData.objects[0].state_machine === 'MEDIUM' ? 'active' : ''}`}>MONITORING</div>
                                    <div className="state-arrow">→</div>
                                    <div className={`state-node ${reasoningData.objects[0].state_machine === 'HIGH' ? 'active' : ''}`}>WARNING</div>
                                    <div className="state-arrow">→</div>
                                    <div className={`state-node ${reasoningData.objects[0].state_machine === 'CRITICAL' ? 'active' : ''}`}>CRITICAL</div>
                                </div>
                            </div>
                            
                            {/* Explanation */}
                            <div className="explanation-panel">
                                <div className="explanation-header">AI REASONING</div>
                                <p className="explanation-text">{reasoningData.objects[0].explanation}</p>
                            </div>
                        </div>
                    ) : (
                        <div className="empty-state">
                            <div className="empty-icon">📊</div>
                            <p>No analysis available</p>
                            <span>Awaiting target lock...</span>
                        </div>
                    )}
                </div>

                {/* Right Column - Event Log */}
                <div className="grid-section events-section">
                    <div className="section-header">
                        <h2>REASONING FEED</h2>
                        <div className="badge">{eventLog.length}</div>
                    </div>
                    
                    <div className="event-log" ref={logRef}>
                        {eventLog.length > 0 ? (
                            <AnimatePresence>
                                {eventLog.map((log) => (
                                    <motion.div 
                                        key={log.id} 
                                        className={`log-entry ${(log.severityLevel || log.type).toLowerCase()}`}
                                        initial={{ opacity: 0, x: -20, scale: 0.95 }}
                                        animate={{ opacity: 1, x: 0, scale: 1 }}
                                        exit={{ opacity: 0, x: 20, scale: 0.95 }}
                                        transition={{ 
                                            duration: 0.3,
                                            ease: "easeOut"
                                        }}
                                    >
                                        <div className="log-header">
                                            <div className="log-time">{log.timestamp}</div>
                                            {log.severityLevel && (
                                                <motion.div 
                                                    className={`severity-badge ${log.severityLevel.toLowerCase()}`}
                                                    initial={{ scale: 0 }}
                                                    animate={{ scale: 1 }}
                                                    transition={{ delay: 0.1, type: "spring", stiffness: 200 }}
                                                >
                                                    {log.severityLevel}
                                                </motion.div>
                                            )}
                                        </div>
                                        
                                        <div className="log-type-row">
                                            <span className="event-type-tag">{log.type}</span>
                                            {log.trackId && (
                                                <span className="track-id-tag">TRACK #{log.trackId}</span>
                                            )}
                                        </div>
                                        
                                        <div className="log-message">{log.message}</div>
                                        
                                        {log.duration && (
                                            <div className="log-footer">
                                                <span className="duration-tag">🕐 {log.duration.toFixed(1)}s</span>
                                            </div>
                                        )}
                                        
                                        <div className="log-severity">
                                            <motion.div 
                                                className="severity-indicator"
                                                style={{ background: getSeverityColor(log.severityLevel || log.type) }}
                                                initial={{ width: 0 }}
                                                animate={{ width: `${(log.severity || 0) * 100}%` }}
                                                transition={{ duration: 0.5, ease: "easeOut" }}
                                            ></motion.div>
                                        </div>
                                    </motion.div>
                                ))}
                            </AnimatePresence>
                        ) : (
                            <motion.div 
                                className="empty-state"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                transition={{ delay: 0.5 }}
                            >
                                <div className="empty-icon">📜</div>
                                <p>Event log empty</p>
                                <span>Monitoring in progress...</span>
                            </motion.div>
                        )}
                    </div>
                </div>
            </div>

            {/* System Status Bar */}
            <div className="status-bar">
                <div className="status-left">
                    <div className={`system-state ${reasoningData?.system_state?.toLowerCase() || 'idle'}`}>
                        <div className="state-pulse"></div>
                        <span>SYSTEM: {reasoningData?.system_state || 'IDLE'}</span>
                    </div>
                </div>
                
                <div className="status-center">
                    {reasoningData?.events?.map((event, i) => (
                        <div key={i} className="active-event">
                            <span className="event-icon">⚡</span>
                            <span>{event.type.replace('_', ' ')}</span>
                        </div>
                    ))}
                </div>
                
                <div className="status-right">
                    <div className="threat-meter">
                        <span className="threat-label">THREAT LEVEL</span>
                        <div className="threat-bar">
                            <div 
                                className="threat-fill"
                                style={{ 
                                    width: `${(reasoningData?.threat_level || 0) * 100}%`,
                                    background: getStateColor(reasoningData?.system_state || 'IDLE')
                                }}
                            ></div>
                        </div>
                        <span className="threat-value">{((reasoningData?.threat_level || 0) * 100).toFixed(0)}%</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

// Helper function to calculate radar chart points
const calculateRadarPoints = (breakdown) => {
    const factors = [
        breakdown.velocity_score,
        breakdown.zone_score,
        breakdown.behavior_score,
        breakdown.time_score,
        breakdown.dwell_score
    ];
    
    const angles = [0, 72, 144, 216, 288]; // 5 points, 360/5 = 72 degrees apart
    const center = 100;
    const maxRadius = 80;
    
    const points = factors.map((value, i) => {
        const angle = (angles[i] - 90) * (Math.PI / 180); // Rotate -90 to start at top
        const radius = value * maxRadius;
        const x = center + radius * Math.cos(angle);
        const y = center + radius * Math.sin(angle);
        return `${x},${y}`;
    });
    
    return points.join(' ');
};

export default IntelligenceCore;
