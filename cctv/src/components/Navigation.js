import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import './Navigation.css';

const Navigation = () => {
    const [expanded, setExpanded] = useState(false);

    return (
        <aside 
            className={`elite-nav ${expanded ? 'expanded' : 'collapsed'}`}
            onMouseEnter={() => setExpanded(true)}
            onMouseLeave={() => setExpanded(false)}
        >
            <div className="nav-header">
                <div className="logo-icon"></div>
                <div className="logo-text">
                    <div className="brand">AEGIS</div>
                    <div className="sub">COMMAND</div>
                </div>
            </div>

            <nav className="nav-list">
                <NavItem to="/" icon="⦿" label="LIVE FEED" expanded={expanded} />
                <NavItem to="/alerts" icon="⚡" label="THREAT INTEL" expanded={expanded} />
                <NavItem to="/evidence" icon="📁" label="EVIDENCE" expanded={expanded} />
                <NavItem to="/copilot" icon="🤖" label="AI AGENT" expanded={expanded} />
            </nav>

            <div className={`nav-footer ${expanded ? 'show' : ''}`}>
                <div className="user-block">
                    <div className="avatar"></div>
                    <div>
                        <div className="u-name">CMD. REYES</div>
                        <div className="u-rank">LVL. 9 ACCESS</div>
                    </div>
                </div>
            </div>
        </aside>
    );
};

const NavItem = ({ to, icon, label, expanded }) => (
    <NavLink to={to} className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
        <div className="icon-box">{icon}</div>
        <div className="label-box">
            {label}
        </div>
        <div className="glow-bar"></div>
    </NavLink>
);

export default Navigation;
