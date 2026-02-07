import React, { useState, useEffect, useRef } from "react";
import "./AICopilot.css";

/* 
   MOCK INTELLIGENCE ENGINE
   Simulates a high-level AI reasoning process rather than a simple chatbot response.
*/
const REASONING_TEMPLATES = [
    {
        type: 'ANALYSIS',
        steps: [
            { label: 'PARSING INTENT', value: 'Semantic vector extraction complete.' },
            { label: 'DATA CORRELATION', value: 'Cross-referencing 14 active streams against behavior baseline.' },
            { label: 'PATTERN RECOGNITION', value: 'Deviation detected in sector Logic-7.' }
        ],
        conclusion: 'Subject exhibits non-standard dwell time. Recommendation: Increase surveillance priority.'
    },
    {
        type: 'INFERENCE',
        steps: [
            { label: 'QUERY SCOPE', value: 'Historical archive // T-Minus 48h.' },
            { label: 'ENTITY TRACKING', value: 'Subject ID #9921 isolated in 3 frames.' },
            { label: 'BEHAVIORAL MATCH', value: '94% match with known loitering pattern.' }
        ],
        conclusion: 'Confirmed visual contact. Entity movement suggests pre-event reconnaissance.'
    },
    {
        type: 'SYSTEM',
        steps: [
            { label: 'SYSTEM CHECK', value: 'Encryption layer integrity: 100%.' },
            { label: 'NODE STATUS', value: 'All edge nodes active. Latency < 12ms.' }
        ],
        conclusion: 'System operational. Ready for high-load inference.'
    }
];

const AICopilot = () => {
    const [inputValue, setInputValue] = useState("");
    const [history, setHistory] = useState([
        { 
            id: 'init-1', 
            role: 'system', 
            timestamp: new Date().toISOString(),
            content: { 
                type: 'SYSTEM', 
                steps: [{ label: 'INITIALIZATION', value: 'Cognitive Core Online.' }], 
                conclusion: 'Awaiting intent injection.' 
            }
        }
    ]);
    const [isProcessing, setIsProcessing] = useState(false);
    const [systemState, setSystemState] = useState('IDLE'); // IDLE, PARSING, CORRELATING, SYNTHESIZING
    const bottomRef = useRef(null);

    // Auto-scroll to bottom of cognitive field
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [history, isProcessing]);

    const handleInjectIntent = () => {
        if (!inputValue.trim()) return;

        // 1. Inject User Intent
        const newIntent = {
            id: Date.now(),
            role: 'user',
            timestamp: new Date().toISOString(),
            content: inputValue
        };

        setHistory(prev => [...prev, newIntent]);
        setInputValue("");
        setIsProcessing(true);
        setSystemState('PARSING');

        // 2. Simulate AI Reasoning Process
        setTimeout(() => {
            setSystemState('CORRELATING');
            
            setTimeout(() => {
                setSystemState('SYNTHESIZING');
                
                // Select Random Template
                const template = REASONING_TEMPLATES[Math.floor(Math.random() * REASONING_TEMPLATES.length)];
                
                const responseNode = {
                    id: Date.now() + 1,
                    role: 'ai',
                    timestamp: new Date().toISOString(),
                    content: template
                };

                setTimeout(() => {
                    setHistory(prev => [...prev, responseNode]);
                    setIsProcessing(false);
                    setSystemState('IDLE');
                }, 800);
            }, 1200);
        }, 1000);
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleInjectIntent();
        }
    };

    return (
        <div className="copilot-interface">
            {/* ZONE C: CONTEXT MEMORY STRIP (SIDE) */}
            <aside className="context-strip">
                <div className="ctx-header">ACTIVE CONTEXT</div>
                <div className="ctx-list">
                    <ContextNode label="ZONE_ALPHA_01" active={true} />
                    <ContextNode label="SUBJECT_9921" active={false} />
                    <ContextNode label="ALERT_LVL_3" active={false} />
                    <ContextNode label="ARCHIVE_SEARCH" active={false} />
                </div>
                
                <div className="system-metrics">
                    <div className="metric-row">
                        <span className="lbl">LOAD</span>
                        <div className="bar"><div className="fill" style={{width: '34%'}}></div></div>
                    </div>
                    <div className="metric-row">
                        <span className="lbl">MEM</span>
                        <div className="bar"><div className="fill" style={{width: '62%'}}></div></div>
                    </div>
                </div>
            </aside>

            {/* ZONE B: COGNITIVE FIELD (CENTER) */}
            <main className="cognitive-field">
                {/* ZONE D: SYSTEM CONSCIOUSNESS (OVERLAY) */}
                <div className="consciousness-hud">
                    <div className="state-indicator">
                        <div className={`status-dot ${systemState}`}></div>
                        <span className="status-text">{systemState}</span>
                    </div>
                    <div className="neural-id">NODE: AEGIS-PRIME // V.9.0.4</div>
                </div>

                <div className="thought-stream">
                    {history.map((node) => (
                        <CognitiveNode key={node.id} data={node} />
                    ))}
                    
                    {isProcessing && (
                         <div className="processing-indicator">
                            <span className="blink">_</span> PROCESSING STREAM
                         </div>
                    )}
                    <div ref={bottomRef}></div>
                </div>
            </main>

            {/* ZONE A: INTENT ZONE (BOTTOM) */}
            <div className="intent-zone">
                <div className="intent-wrapper">
                    <div className="intent-prefix">>>></div>
                    <input 
                        type="text" 
                        className="intent-input"
                        placeholder="INJECT INTENT PARAMETERS..."
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={handleKeyDown}
                        disabled={isProcessing}
                        autoFocus
                    />
                    <button 
                        className={`inject-btn ${inputValue ? 'active' : ''}`}
                        onClick={handleInjectIntent}
                    >
                        EXECUTE
                    </button>
                </div>
            </div>
        </div>
    );
};

/* Sub-components */
const ContextNode = ({ label, active }) => (
    <div className={`ctx-node ${active ? 'active' : ''}`}>
        <div className="ctx-dot"></div>
        <span className="ctx-lbl">{label}</span>
    </div>
);

const CognitiveNode = ({ data }) => {
    const isUser = data.role === 'user';
    
    if (isUser) {
        return (
            <div className="node-wrapper user-intent">
                <div className="intent-marker">USER INTENT INJECTION</div>
                <div className="intent-content">"{data.content}"</div>
            </div>
        );
    }

    // AI Response (Cognitive Block)
    return (
        <div className="node-wrapper ai-reasoning">
            <div className="reasoning-header">
                <span className="rh-type">{data.content.type} BLOCK</span>
                <span className="rh-time">{data.timestamp.split('T')[1].substring(0,8)}</span>
            </div>
            
            <div className="reasoning-body">
                {/* Steps Section */}
                <div className="reasoning-steps">
                    {data.content.steps.map((step, i) => (
                        <div key={i} className="r-step" style={{animationDelay: `${i * 0.15}s`}}>
                            <span className="step-label">{step.label}</span>
                            <span className="step-line"></span>
                            <span className="step-val">{step.value}</span>
                        </div>
                    ))}
                </div>

                {/* Conclusion Section */}
                <div className="reasoning-conclusion">
                    <div className="conc-icon"></div>
                    <div className="conc-text">{data.content.conclusion}</div>
                </div>
            </div>
        </div>
    );
};

export default AICopilot;
