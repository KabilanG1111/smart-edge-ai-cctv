import React, { useState, useEffect, useRef } from 'react';
import './AICopilot.css';

const AICopilot = () => {
    const [input, setInput] = useState('');
    const [history, setHistory] = useState([
        { type: 'sys', text: 'SYSTEM INITIALIZED. CORE SYSTEMS ONLINE.' },
        { type: 'sys', text: 'AWAITING COMMAND...' }
    ]);
    const [status, setStatus] = useState('IDLE');
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [history]);

    const handleCommand = (e) => {
        if (e.key === 'Enter' && input.trim()) {
            const cmd = input.toUpperCase();
            setHistory(prev => [...prev, { type: 'user', text: `> ${cmd}` }]);
            setInput('');
            processCommand(cmd);
        }
    };

    const processCommand = (cmd) => {
        setStatus('ANALYZING');
        
        // Simulating processing delay and response
        setTimeout(() => {
            setStatus('EXECUTING');
            setTimeout(() => {
                const responses = generateResponse(cmd);
                streamResponse(responses);
            }, 800);
        }, 600);
    };

    const generateResponse = (cmd) => {
        if (cmd.includes('STATUS')) return ['DIAGNOSTIC COMPLETE.', 'ALL SYSTEMS NOMINAL.', 'SECURITY LEVEL: ALPHA.'];
        if (cmd.includes('SCAN')) return ['INITIATING DEEP SCAN...', 'SECTOR 4: CLEAR', 'SECTOR 9: ANOMALY DETECTED', 'SCAN COMPLETE.'];
        if (cmd.includes('HELP')) return ['AVAILABLE COMMANDS:', '- SYSTEM STATUS', '- INITIATE SCAN', '- DEPLOY DRONE ALPHA', '- ACCESS ARCHIVES'];
        return ['COMMAND UNRECOGNIZED.', 'PLEASE REFINE PARAMETERS.'];
    };

    const streamResponse = (lines) => {
        let i = 0;
        const interval = setInterval(() => {
            if (i < lines.length) {
                setHistory(prev => [...prev, { type: 'sys', text: lines[i] }]);
                i++;
            } else {
                clearInterval(interval);
                setStatus('IDLE');
            }
        }, 500);
    };

    return (
        <div className="copilot-interface">
            <div className="scanline-overlay"></div>
            <div className="noise-overlay"></div>
            <div className="grid-overlay"></div>
            
            <header className="interface-header">
                <div className="brand-block">
                    <span className="icon">◈</span>
                    <span className="title">AI REASONING CORE // TIER-1</span>
                </div>
                <div className="header-deco">
                    <span className="deco-line">SECURE_CHANNEL_ESTABLISHED</span>
                    <span className="deco-line">ENCRYPTION: QUANTUM-256</span>
                </div>
                <div className={`status-block ${status.toLowerCase()}`}>
                    <span className="label">SYSTEM STATUS:</span>
                    <span className="value blink">{status}</span>
                </div>
            </header>

            <main className="main-layout">
                {/* Left Telemetry Sidebar */}
                <aside className="telemetry-bar left">
                    <div className="telemetry-group">
                        <div className="t-label">CPU_LOAD</div>
                        <div className="t-bar"><div className="fill" style={{width: '45%'}}></div></div>
                    </div>
                    <div className="telemetry-group">
                        <div className="t-label">MEM_ALLOC</div>
                        <div className="t-bar"><div className="fill" style={{width: '72%'}}></div></div>
                    </div>
                    <div className="telemetry-divider"></div>
                     <div className="telemetry-stat">
                        <span className="s-label">UPTIME</span>
                        <span className="s-val">8492:12:44</span>
                    </div>
                </aside>

                <div className="console-container">
                    <div className="console-viewport">
                        {history.map((entry, idx) => (
                            <div key={idx} className={`console-entry ${entry.type}`}>
                                {entry.text}
                            </div>
                        ))}
                        <div ref={bottomRef} />
                    </div>
                    
                     {/* Corner Brackets */}
                    <div className="corner-bracket top-left"></div>
                    <div className="corner-bracket top-right"></div>
                    <div className="corner-bracket bottom-left"></div>
                    <div className="corner-bracket bottom-right"></div>
                </div>

                {/* Right Telemetry Sidebar */}
                <aside className="telemetry-bar right">
                    <div className="module-list">
                        <div className="module-item active">[VISION_MOD]</div>
                        <div className="module-item active">[AUDIO_MOD]</div>
                        <div className="module-item standby">[DRONE_UPLINK]</div>
                        <div className="module-item offline">[WEAPON_CTRL]</div>
                    </div>
                </aside>
            </main>

            <footer className="command-footer">
                <div className="cmd-prefix">COMMAND_INPUT_TERMINAL_V4</div>
                <div className="command-bar">
                    <span className="cursor-prompt">>></span>
                    <input 
                        type="text" 
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleCommand}
                        placeholder="INITIATE COMMAND SEQUENCE..."
                        spellCheck="false"
                        autoFocus
                    />
                    <div className="input-deco">_</div>
                </div>
            </footer>
        </div>
    );
};

export default AICopilot;
