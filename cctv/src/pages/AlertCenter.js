import React, { useState, useEffect } from "react";
import "./AlertCenter.css";

const API = process.env.REACT_APP_API_URL || "/api";

const AlertCenter = () => {
    const [alerts, setAlerts] = useState([]);

    useEffect(() => {
        fetch(`${API}/alerts/live?limit=30`)
            .then(res => res.json())
            .then(data => setAlerts(data.alerts || []))
            .catch(() => {});
    }, []);

    const getSeverityColor = (sev) => {
        switch(sev) {
            case 'CRITICAL': return 'var(--red-crit)';
            case 'HIGH': return 'var(--orange-high)';
            case 'MEDIUM': return 'var(--amber-med)';
            default: return 'var(--cyan-dim)';
        }
    };

    return (
        <div className="intel-view">
            <header className="intel-head">
                <h1>THREAT INTELLIGENCE STREAM</h1>
                <div className="head-metrics">
                    <span className="h-metric">ACTIVE THREATS: <b className="mono">{alerts.length}</b></span>
                    <span className="h-sep">|</span>
                    <div className="badge-live">LIVE ANALYTICS</div>
                </div>
            </header>
            
            <div className="intel-list">
                {alerts.map(alert => {
                    const color = getSeverityColor(alert.decision?.severity);
                    
                    return (
                        <div key={alert.alert_id} className={`intel-row ${alert.decision?.severity}`}>
                            <div className="row-severity">
                                <SeverityRing severity={alert.decision?.severity} color={color} />
                            </div>
                            
                            <div className="row-main">
                                <div className="r-type mono">{alert.event?.event_type}</div>
                                <div className="r-msg">{alert.decision?.message}</div>
                            </div>

                            <div className="row-meta">
                                <div className="r-conf mono">
                                    {(alert.decision?.confidence * 100).toFixed(0)}% CONF
                                </div>
                                <div className="r-time mono">
                                    {new Date(alert.timestamp).toLocaleTimeString([], {hour12:false})}
                                </div>
                            </div>
                        </div>
                    );
                })}

                {alerts.length === 0 && (
                     <div className="empty-state">
                        <div className="empty-icon">⚠️</div>
                        <div>NO ACTIVE THREAT SIGNATURES DETECTED</div>
                     </div>
                )}
            </div>
        </div>
    );
};

const SeverityRing = ({ severity, color }) => (
    <div className={`sev-ring-container ${severity}`}>
        <div className="ring-outer" style={{ borderColor: color, boxShadow: `0 0 10px ${color}` }}></div>
        <div className="ring-inner" style={{ backgroundColor: color }}></div>
    </div>
);

export default AlertCenter;
