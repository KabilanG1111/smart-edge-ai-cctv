import React, { useEffect, useRef } from 'react';
import './CustomCursor.css';

/**
 * 🎯 AEGIS SURVEILLANCE CURSOR SYSTEM
 * 
 * Concept: AI Vision Targeting Reticle
 * - Follows mouse with slight inertia (0.12s delay) = feels tracked, not instant
 * - Hollow circle with crosshair = precision aiming interface
 * - Expands on interactive elements = target acquisition confirmation
 * - Pulse animation = continuous system monitoring
 * 
 * Why This Works for Surveillance:
 * 1. Visual Language: Matches CCTV camera overlays and targeting systems
 * 2. Precision Feedback: Users know exactly where they're pointing
 * 3. State Communication: Cursor changes = system recognizing interaction targets
 * 4. Professional Tone: No arrows, no hands, pure tactical interface
 */

const CustomCursor = () => {
    const cursorRef = useRef(null);
    const cursorDotRef = useRef(null);

    useEffect(() => {
        const cursor = cursorRef.current;
        const cursorDot = cursorDotRef.current;

        let mouseX = 0;
        let mouseY = 0;
        let cursorX = 0;
        let cursorY = 0;

        // Track mouse position
        const handleMouseMove = (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;

            // Center dot follows instantly
            if (cursorDot) {
                cursorDot.style.left = `${mouseX}px`;
                cursorDot.style.top = `${mouseY}px`;
            }
        };

        // Smooth inertia animation for outer ring
        const animateCursor = () => {
            // Inertia calculation (0.12 interpolation = slight lag)
            const dx = mouseX - cursorX;
            const dy = mouseY - cursorY;
            cursorX += dx * 0.12;
            cursorY += dy * 0.12;

            if (cursor) {
                cursor.style.left = `${cursorX}px`;
                cursor.style.top = `${cursorY}px`;
            }

            requestAnimationFrame(animateCursor);
        };

        // Interactive element detection
        const handleMouseOver = (e) => {
            const target = e.target;
            if (
                target.tagName === 'BUTTON' ||
                target.tagName === 'A' ||
                target.classList.contains('alert-item-card') ||
                target.classList.contains('ev-card') ||
                target.classList.contains('threat-card') ||
                target.classList.contains('ctx-node') ||
                target.closest('button') ||
                target.closest('a')
            ) {
                cursor?.classList.add('cursor-hover');
                
                // Critical action detection
                if (
                    target.classList.contains('dispatch') ||
                    target.classList.contains('term-btn')
                ) {
                    cursor?.classList.add('cursor-critical');
                }
            }
        };

        const handleMouseOut = (e) => {
            cursor?.classList.remove('cursor-hover', 'cursor-critical');
        };

        // Event listeners
        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseover', handleMouseOver, true);
        document.addEventListener('mouseout', handleMouseOut, true);

        // Start animation loop
        animateCursor();

        return () => {
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseover', handleMouseOver, true);
            document.removeEventListener('mouseout', handleMouseOut, true);
        };
    }, []);

    return (
        <>
            <div ref={cursorRef} className="custom-cursor"></div>
            <div ref={cursorDotRef} className="custom-cursor-dot"></div>
        </>
    );
};

export default CustomCursor;
