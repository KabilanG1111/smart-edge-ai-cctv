import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";

const EntranceAnimation = ({ onComplete }) => {
  const [bootPhase, setBootPhase] = useState("forbidden");

  // Generate star field (MORE DENSE)
  const [stars] = useState(() =>
    Array.from({ length: 450 }, () => ({
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: Math.random() * 2 + 0.5,
      opacity: Math.random() * 0.6 + 0.3,
      speed: 15 + Math.random() * 25,
    }))
  );

  // City buildings - Left cluster (TALLER, MORE BUILDINGS)
  const [leftBuildings] = useState([
    { height: 280, width: 45, x: 8, windows: 20 },
    { height: 320, width: 40, x: 12, windows: 24 },
    { height: 240, width: 50, x: 16, windows: 18 },
    { height: 300, width: 42, x: 20, windows: 22 },
    { height: 260, width: 38, x: 24, windows: 20 },
    { height: 340, width: 48, x: 28, windows: 26 },
    { height: 220, width: 36, x: 32, windows: 16 },
  ]);

  // City buildings - Right cluster (TALLER, MORE BUILDINGS)
  const [rightBuildings] = useState([
    { height: 290, width: 46, x: 68, windows: 21 },
    { height: 310, width: 38, x: 72, windows: 23 },
    { height: 250, width: 44, x: 76, windows: 19 },
    { height: 330, width: 40, x: 80, windows: 25 },
    { height: 270, width: 42, x: 84, windows: 20 },
    { height: 350, width: 46, x: 88, windows: 28 },
    { height: 230, width: 38, x: 92, windows: 17 },
    { height: 290, width: 36, x: 96, windows: 22 },
  ]);

  // Data vehicles (MORE TRAFFIC)
  const [dataVehicles] = useState(() =>
    Array.from({ length: 20 }, (_, i) => ({
      id: i,
      lane: (i % 7) - 3, // -3, -2, -1, 0, 1, 2, 3 (MORE LANES)
      delay: i * 0.9,
      speed: 10 + Math.random() * 5,
    }))
  );

  // Concentric rings configuration (SOME BROKEN FOR HUD FEEL)
  const rings = [
    { diameter: 380, speed: 85, opacity: 0.30, direction: 1, broken: false },
    { diameter: 560, speed: 105, opacity: 0.26, direction: -1, broken: true, arcLength: 280 },
    { diameter: 740, speed: 135, opacity: 0.22, direction: 1, broken: false },
    { diameter: 920, speed: 165, opacity: 0.18, direction: -1, broken: true, arcLength: 300 },
    { diameter: 1100, speed: 200, opacity: 0.14, direction: 1, broken: false },
    { diameter: 1280, speed: 240, opacity: 0.10, direction: -1, broken: true, arcLength: 320 },
    { diameter: 1460, speed: 285, opacity: 0.08, direction: 1, broken: false },
    { diameter: 1640, speed: 330, opacity: 0.06, direction: -1, broken: false },
    { diameter: 1820, speed: 380, opacity: 0.04, direction: 1, broken: false },
  ];

  // Orbital particles around core (NEW)
  const [orbitParticles] = useState(() =>
    Array.from({ length: 12 }, (_, i) => ({
      id: i,
      orbit: 200 + i * 35,
      speed: 8 + i * 2,
      size: 2 + Math.random() * 2,
      delay: i * 0.3,
    }))
  );

  // HUD glyphs and data markers (NEW)
  const [hudGlyphs] = useState(() =>
    Array.from({ length: 20 }, (_, i) => ({
      id: i,
      x: 15 + Math.random() * 70,
      y: 15 + Math.random() * 70,
      text: ['█', '▓', '▒', '░', '◢', '◣', '◤', '◥', '▀', '▄'][Math.floor(Math.random() * 10)],
      delay: Math.random() * 2,
      duration: 3 + Math.random() * 4,
    }))
  );

  // Hex grid overlays (MORE COVERAGE)
  const [hexGrids] = useState(() =>
    Array.from({ length: 16 }, (_, i) => ({
      id: i,
      x: 10 + Math.random() * 80,
      y: 10 + Math.random() * 80,
      delay: Math.random() * 3,
      duration: 2 + Math.random() * 3,
      size: 40 + Math.random() * 40,
    }))
  );

  // Micro glitches (MORE ACTIVITY)
  const [microGlitches] = useState(() =>
    Array.from({ length: 25 }, (_, i) => ({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      delay: Math.random() * 1.4,
      size: 1 + Math.random() * 2,
    }))
  );

  // Atmospheric fog layers (NEW)
  const fogLayers = [
    { y: 20, opacity: 0.08, speed: 40 },
    { y: 40, opacity: 0.06, speed: 50 },
    { y: 60, opacity: 0.05, speed: 60 },
  ];

  useEffect(() => {
    const timers = [
      setTimeout(() => setBootPhase("security-scan"), 1200),
      setTimeout(() => setBootPhase("rings-init"), 1400),
      setTimeout(() => setBootPhase("grid-activate"), 2000),
      setTimeout(() => setBootPhase("city-online"), 3000),
      setTimeout(() => setBootPhase("title-reveal"), 4500),
      setTimeout(() => setBootPhase("locked"), 5800),
      setTimeout(() => {
        sessionStorage.setItem("EDGE_AI_BOOT_COMPLETE", "true");
        if (onComplete) onComplete();
      }, 6500),
    ];

    return () => timers.forEach(clearTimeout);
  }, [onComplete]);

  const isLocked = bootPhase === "locked";

  return (
    <motion.div
      initial={{ opacity: 1 }}
      animate={{ opacity: isLocked ? 0 : 1 }}
      transition={{ duration: 1, ease: "easeOut" }}
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 9999,
        overflow: "hidden",
        background: "#000000",
        cursor: "none",
      }}
    >
      {/* LAYER 5: BACKGROUND - Star Field (CINEMATIC WITH VOLUMETRIC LIGHTING) */}
      <div style={{ position: "absolute", inset: 0, background: "linear-gradient(180deg, #000000 0%, #001520 40%, #001a25 70%, #001f2a 100%)" }}>
        {/* Volumetric light rays from center bottom */}
        <div style={{ position: "absolute", inset: 0, overflow: "hidden" }}>
          {[0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330].map((angle) => (
            <motion.div
              key={`ray-${angle}`}
              animate={{ opacity: [0.08, 0.15, 0.08] }}
              transition={{ duration: 4 + (angle % 3), ease: "easeInOut", repeat: Infinity, delay: angle / 120 }}
              style={{
                position: "absolute",
                bottom: "42%",
                left: "50%",
                width: "2px",
                height: "60%",
                background: `linear-gradient(180deg, transparent 0%, rgba(0, 240, 255, 0.15) 40%, rgba(0, 240, 255, 0.25) 70%, rgba(0, 240, 255, 0.4) 100%)`,
                transform: `rotate(${angle}deg)`,
                transformOrigin: "bottom center",
                filter: "blur(3px)",
              }}
            />
          ))}
        </div>
        
        {stars.map((star, i) => (
          <motion.div
            key={`star-${i}`}
            animate={{ opacity: [star.opacity * 0.6, star.opacity * 0.3, star.opacity * 0.6], y: [0, 8, 0] }}
            transition={{ duration: star.speed, repeat: Infinity, ease: "linear" }}
            style={{
              position: "absolute",
              left: `${star.x}%`,
              top: `${star.y}%`,
              width: `${star.size}px`,
              height: `${star.size}px`,
              background: "rgba(255, 255, 255, 0.8)",
              borderRadius: "50%",
              boxShadow: `0 0 ${star.size * 2}px rgba(0,240,255,${star.opacity * 0.3}), 0 0 ${star.size}px rgba(255,255,255,${star.opacity * 0.5})`,
            }}
          />
        ))}
        
        {/* Atmospheric fog layers (SUBTLE PARTICLES) */}
        {fogLayers.map((fog, i) => (
          <motion.div
            key={`fog-${i}`}
            animate={{ backgroundPositionX: ["0%", "100%"] }}
            transition={{ duration: fog.speed, repeat: Infinity, ease: "linear" }}
            style={{
              position: "absolute",
              left: 0,
              right: 0,
              top: `${fog.y}%`,
              height: "20%",
              background: `linear-gradient(90deg, transparent, rgba(0, 240, 255, ${fog.opacity * 0.5}) 50%, transparent)`,
              backgroundSize: "200% 100%",
              filter: "blur(50px)",
              pointerEvents: "none",
            }}
          />
        ))}
            }}
          />
        ))}
      </div>

      {/* FORBIDDEN ENTRY: Digital Noise Overlay */}
      {bootPhase === "forbidden" && (
        <motion.div
          animate={{ opacity: [0.03, 0.05, 0.03] }}
          transition={{ duration: 0.2, repeat: Infinity }}
          style={{
            position: "absolute",
            inset: 0,
            background: `repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,240,255,0.02) 2px, rgba(0,240,255,0.02) 4px)`,
            zIndex: 50,
          }}
        >
          {/* Micro glitches */}
          {microGlitches.map((glitch) => (
            <motion.div
              key={glitch.id}
              animate={{ opacity: [0, 0.9, 0] }}
              transition={{ duration: 0.08, delay: glitch.delay, repeat: 2, repeatDelay: 0.5 }}
              style={{
                position: "absolute",
                left: `${glitch.x}%`,
                top: `${glitch.y}%`,
                width: `${glitch.size}px`,
                height: `${glitch.size}px`,
                background: "rgba(0, 255, 240, 0.8)",
                boxShadow: `0 0 ${glitch.size * 2}px rgba(0, 255, 240, 1)`,
                borderRadius: "50%",
              }}
            />
          ))}
        </motion.div>
      )}

      {/* SECURITY SCAN FLASH */}
      {bootPhase === "security-scan" && (
        <motion.div
          initial={{ scaleX: 0, opacity: 0 }}
          animate={{ scaleX: [0, 1, 1, 0], opacity: [0, 1, 1, 0] }}
          transition={{ duration: 0.2, times: [0, 0.3, 0.7, 1] }}
          style={{
            position: "absolute",
            top: "50%",
            left: 0,
            right: 0,
            height: "1px",
            background: "linear-gradient(90deg, transparent, rgba(255,255,255,0.9) 30%, rgba(0,255,240,1) 50%, rgba(255,255,255,0.9) 70%, transparent)",
            boxShadow: "0 0 40px rgba(0,255,240,1), 0 0 80px rgba(0,255,240,0.6)",
            transformOrigin: "left",
            zIndex: 100,
          }}
        >
          <div
            style={{
              position: "absolute",
              top: "-5px",
              left: "48%",
              fontSize: "7px",
              color: "rgba(0, 255, 240, 0.8)",
              letterSpacing: "2px",
              fontFamily: "monospace",
              textShadow: "0 0 8px rgba(0, 255, 240, 1)",
            }}
          >
            ▓█▒░█▓▒░▓█
          </div>
        </motion.div>
      )}

      {/* LAYER 4: CITY BUILDINGS */}
      {bootPhase !== "forbidden" && bootPhase !== "security-scan" && (
        <>
          {/* Left buildings (BENEATH HUD) */}
          {leftBuildings.map((building, i) => (
            <motion.div
              key={`left-${i}`}
              initial={{ opacity: 0, scaleY: 0 }}
              animate={{ opacity: 1, scaleY: 1 }}
              transition={{ duration: 0.8, delay: 1.5 + i * 0.1, ease: "easeOut" }}
              style={{
                position: "absolute",
                left: `${building.x}%`,
                bottom: "0",
                width: `${building.width}px`,
                height: `${building.height}px`,
                background: "linear-gradient(180deg, #0d0d0d 0%, #060606 100%)",
                transformOrigin: "bottom",
                boxShadow: "inset 0 0 20px rgba(0, 240, 255, 0.05)",
                zIndex: 1,
              }}
            >
              {/* Windows */}
              {Array.from({ length: building.windows }).map((_, w) => (
                <motion.div
                  key={`window-${w}`}
                  animate={{
                    opacity: Math.random() > 0.5 ? [0.2, 0.7, 0.3, 0] : [0, 0.4, 0.6, 0.3],
                  }}
                  transition={{
                    duration: 3 + Math.random() * 4,
                    delay: 2 + Math.random() * 3,
                    repeat: Infinity,
                    ease: "easeInOut",
                  }}
                  style={{
                    position: "absolute",
                    left: `${10 + (w % 3) * 30}%`,
                    top: `${10 + Math.floor(w / 3) * 20}%`,
                    width: "3px",
                    height: "4px",
                    background: Math.random() > 0.6 ? "rgba(0, 240, 255, 0.7)" : "rgba(255, 200, 150, 0.7)",
                    boxShadow: Math.random() > 0.6 ? "0 0 4px rgba(0, 240, 255, 0.6)" : "0 0 4px rgba(255, 200, 150, 0.6)",
                  }}
                />
              ))}
            </motion.div>
          ))}

          {/* Right buildings (BENEATH HUD) */}
          {rightBuildings.map((building, i) => (
            <motion.div
              key={`right-${i}`}
              initial={{ opacity: 0, scaleY: 0 }}
              animate={{ opacity: 1, scaleY: 1 }}
              transition={{ duration: 0.8, delay: 1.5 + i * 0.1, ease: "easeOut" }}
              style={{
                position: "absolute",
                left: `${building.x}%`,
                bottom: "0",
                width: `${building.width}px`,
                height: `${building.height}px`,
                background: "linear-gradient(180deg, #0d0d0d 0%, #060606 100%)",
                transformOrigin: "bottom",
                boxShadow: "inset 0 0 20px rgba(0, 240, 255, 0.05)",
                zIndex: 1,
              }}
            >
              {Array.from({ length: building.windows }).map((_, w) => (
                <motion.div
                  key={`window-${w}`}
                  animate={{
                    opacity: Math.random() > 0.5 ? [0.2, 0.7, 0.3, 0] : [0, 0.4, 0.6, 0.3],
                  }}
                  transition={{
                    duration: 3 + Math.random() * 4,
                    delay: 2 + Math.random() * 3,
                    repeat: Infinity,
                    ease: "easeInOut",
                  }}
                  style={{
                    position: "absolute",
                    left: `${10 + (w % 3) * 30}%`,
                    top: `${10 + Math.floor(w / 3) * 20}%`,
                    width: "3px",
                    height: "4px",
                    background: Math.random() > 0.6 ? "rgba(0, 240, 255, 0.7)" : "rgba(255, 200, 150, 0.7)",
                    boxShadow: Math.random() > 0.6 ? "0 0 4px rgba(0, 240, 255, 0.6)" : "0 0 4px rgba(255, 200, 150, 0.6)",
                  }}
                />
              ))}
            </motion.div>
          ))}

          {/* Light rays from buildings to core (INFRASTRUCTURE CONNECTION) */}
          {bootPhase === "city-online" || bootPhase === "title-reveal" || bootPhase === "locked" ? (
            <>
              {[...leftBuildings, ...rightBuildings].slice(0, 8).map((building, i) => (
                <motion.div
                  key={`connection-${i}`}
                  initial={{ opacity: 0, scaleY: 0 }}
                  animate={{ opacity: [0, 0.15, 0.08, 0], scaleY: 1 }}
                  transition={{
                    opacity: { duration: 2, delay: i * 0.15, ease: "easeOut" },
                    scaleY: { duration: 0.8, delay: i * 0.15, ease: "easeOut" },
                  }}
                  style={{
                    position: "absolute",
                    left: `${building.x + building.width / 200}%`,
                    bottom: `${building.height}px`,
                    width: "1px",
                    height: "calc(58% - " + building.height + "px)",
                    background: "linear-gradient(180deg, rgba(0, 240, 255, 0.3), transparent)",
                    transformOrigin: "bottom",
                    filter: "blur(1px)",
                  }}
                />
              ))}
            </>
          ) : null}
        </>
      )}

      {/* LAYER 3: DIGITAL GRID FLOOR (EXTENDING INTO HORIZON) */}
      {bootPhase !== "forbidden" && bootPhase !== "security-scan" && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: bootPhase === "rings-init" ? 0.25 : 0.45 }}
          transition={{ duration: 1.2, ease: "easeOut" }}
          style={{
            position: "absolute",
            inset: 0,
            transform: "perspective(1000px) rotateX(75deg) translateY(35%)",
            transformOrigin: "center bottom",
            overflow: "hidden",
            zIndex: 2,
          }}
        >
          <motion.div
            animate={{ backgroundPositionY: ["0px", "100px"] }}
            transition={{ duration: 3, ease: "linear", repeat: Infinity }}
            style={{
              position: "absolute",
              inset: 0,
              backgroundImage: `
                linear-gradient(0deg, rgba(0, 240, 255, 0.25) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 240, 255, 0.2) 1px, transparent 1px)
              `,
              backgroundSize: "100px 100px",
              boxShadow: "inset 0 -50px 80px rgba(0, 240, 255, 0.08)",
            }}
          />

          {/* Flowing tech roads (BRIGHT GLOWING LANES) */}
          {[-240, -180, -120, -60, 0, 60, 120, 180, 240].map((offset) => (
            <motion.div
              key={`lane-${offset}`}
              animate={{ 
                opacity: [0.4, 0.8, 0.4],
                boxShadow: [
                  "0 0 8px rgba(0, 240, 255, 0.5), 0 0 16px rgba(0, 240, 255, 0.3)",
                  "0 0 16px rgba(0, 240, 255, 0.8), 0 0 32px rgba(0, 240, 255, 0.5)",
                  "0 0 8px rgba(0, 240, 255, 0.5), 0 0 16px rgba(0, 240, 255, 0.3)",
                ]
              }}
              transition={{ duration: 2.5, delay: offset / 120, repeat: Infinity, ease: "easeInOut" }}
              style={{
                position: "absolute",
                left: `calc(50% + ${offset}px)`,
                top: 0,
                bottom: 0,
                width: "3px",
                background: "linear-gradient(180deg, rgba(0, 240, 255, 0.7) 0%, rgba(0, 240, 255, 0.5) 50%, transparent 100%)",
              }}
            />
          ))}
        </motion.div>
      )}

      {/* DATA VEHICLES (FLOWING WITH BRIGHTER TRAILS) */}
      {bootPhase !== "forbidden" && bootPhase !== "security-scan" && bootPhase !== "rings-init" && (
        <div style={{ position: "absolute", inset: 0, zIndex: 3 }}>
          {dataVehicles.map((vehicle) => (
            <React.Fragment key={vehicle.id}>
              <motion.div
                initial={{ opacity: 0 }}
                animate={{
                  y: ["105%", "-5%"],
                  opacity: [0, 1, 1, 0],
                }}
                transition={{
                  duration: vehicle.speed,
                  delay: vehicle.delay,
                  ease: "linear",
                  repeat: Infinity,
                  repeatDelay: 2,
                }}
                style={{
                  position: "absolute",
                  left: `calc(50% + ${vehicle.lane * 50}px)`,
                  bottom: 0,
                  width: "4px",
                  height: "18px",
                  background: "linear-gradient(180deg, rgba(0, 240, 255, 1), rgba(0, 240, 255, 0.5))",
                  borderRadius: "2px",
                  boxShadow: "0 0 18px rgba(0, 240, 255, 1), 0 0 36px rgba(0, 240, 255, 0.8), 0 0 54px rgba(0, 240, 255, 0.5)",
                }}
              />
              <motion.div
                animate={{
                  y: ["105%", "-5%"],
                  opacity: [0, 0.6, 0.6, 0],
                }}
                transition={{
                  duration: vehicle.speed,
                  delay: vehicle.delay,
                  ease: "linear",
                  repeat: Infinity,
                  repeatDelay: 2,
                }}
                style={{
                  position: "absolute",
                  left: `calc(50% + ${vehicle.lane * 50}px - 1px)`,
                  bottom: 0,
                  width: "2px",
                  height: "50px",
                  background: "linear-gradient(180deg, transparent, rgba(0, 240, 255, 0.6))",
                }}
              />
            </React.Fragment>
          ))}
        </div>
      )}

      {/* LAYER 2: CONCENTRIC RINGS (SOME BROKEN FOR HUD FEEL) */}
      {bootPhase !== "forbidden" && bootPhase !== "security-scan" && (
        <div style={{ position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)", zIndex: 5 }}>
          {rings.map((ring, i) => (
            <React.Fragment key={`ring-${i}`}>
              {ring.broken ? (
                <svg
                  style={{
                    position: "absolute",
                    top: "50%",
                    left: "50%",
                    transform: "translate(-50%, -50%)",
                    width: `${ring.diameter}px`,
                    height: `${ring.diameter}px`,
                    overflow: "visible",
                  }}
                >
                  <motion.circle
                    initial={{ opacity: 0, scale: 0.7, rotate: 0 }}
                    animate={{
                      opacity: bootPhase === "rings-init" ? 0 : Math.min(ring.opacity * 2.5, 0.85),
                      scale: 1,
                      rotate: ring.direction === 1 ? 360 : -360,
                    }}
                    transition={{
                      opacity: { duration: 1.2, ease: "easeOut" },
                      scale: { duration: 1.2, ease: "easeOut" },
                      rotate: { duration: ring.speed, ease: "linear", repeat: Infinity },
                    }}
                    cx={ring.diameter / 2}
                    cy={ring.diameter / 2}
                    r={(ring.diameter - 5) / 2}
                    fill="none"
                    stroke="rgba(0, 240, 255, 0.45)"
                    strokeWidth="2.5"
                    strokeDasharray={`${ring.arcLength} ${Math.PI * ring.diameter - ring.arcLength}`}
                    style={{
                      filter: "drop-shadow(0 0 35px rgba(0, 240, 255, 0.35)) drop-shadow(0 0 70px rgba(0, 240, 255, 0.2))",
                      transformOrigin: "center",
                    }}
                  />
                </svg>
              ) : (
                <motion.div
                  initial={{ opacity: 0, scale: 0.7, rotate: 0 }}
                  animate={{
                    opacity: bootPhase === "rings-init" ? 0 : Math.min(ring.opacity * 2.5, 0.85),
                    scale: 1,
                    rotate: ring.direction === 1 ? 360 : -360,
                  }}
                  transition={{
                    opacity: { duration: 1.2, ease: "easeOut" },
                    scale: { duration: 1.2, ease: "easeOut" },
                    rotate: { duration: ring.speed, ease: "linear", repeat: Infinity },
                  }}
                  style={{
                    position: "absolute",
                    top: "50%",
                    left: "50%",
                    transform: "translate(-50%, -50%)",
                    width: `${ring.diameter}px`,
                    height: `${ring.diameter}px`,
                    border: "2.5px solid rgba(0, 240, 255, 0.45)",
                    borderRadius: "50%",
                    borderTopColor: "rgba(0, 240, 255, 0.85)",
                    borderRightColor: "rgba(0, 240, 255, 0.35)",
                    borderBottomColor: "rgba(0, 240, 255, 0.55)",
                    boxShadow: "inset 0 0 40px rgba(0, 240, 255, 0.15), 0 0 35px rgba(0, 240, 255, 0.35), 0 0 70px rgba(0, 240, 255, 0.2)",
                  }}
                />
              )}

              {/* Bright flowing spots on rings */}
              {[0, 45, 90, 135, 180, 225, 270, 315].map((angle) => (
                <motion.div
                  key={`spot-${i}-${angle}`}
                  animate={{
                    opacity: [0.6, 1, 0.6],
                    scale: [1, 1.3, 1],
                    rotate: ring.direction === 1 ? 360 : -360,
                  }}
                  transition={{
                    opacity: { duration: 1.5 + Math.random(), repeat: Infinity },
                    scale: { duration: 1.5 + Math.random(), repeat: Infinity },
                    rotate: { duration: ring.speed, ease: "linear", repeat: Infinity },
                  }}
                  style={{
                    position: "absolute",
                    top: "50%",
                    left: `calc(50% + ${(ring.diameter / 2) * Math.cos((angle * Math.PI) / 180)}px)`,
                    transform: `translate(-50%, calc(-50% + ${(ring.diameter / 2) * Math.sin((angle * Math.PI) / 180)}px))`,
                    width: "6px",
                    height: "6px",
                    background: "rgba(0, 240, 255, 1)",
                    borderRadius: "50%",
                    boxShadow: "0 0 20px rgba(0, 240, 255, 1), 0 0 40px rgba(0, 240, 255, 0.8), 0 0 60px rgba(0, 240, 255, 0.5)",
                  }}
                />
              ))}
            </React.Fragment>
          ))}
        </div>
      )}

      {/* CENTRAL ENERGY CORE (BOTTOM CENTER LIGHT SOURCE) */}
      {bootPhase !== "forbidden" && bootPhase !== "security-scan" && (
        <div style={{ position: "absolute", top: "58%", left: "50%", transform: "translate(-50%, -50%)", zIndex: 4 }}>
          {/* Volumetric bloom layers (BRIGHT CYAN GLOW) */}
          <motion.div
            animate={{ opacity: [0.4, 0.6, 0.4], scale: [0.95, 1.05, 0.95] }}
            transition={{ duration: 4, ease: "easeInOut", repeat: Infinity }}
            style={{
              position: "absolute",
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%)",
              width: "1600px",
              height: "1600px",
              background: "radial-gradient(circle, rgba(0, 240, 255, 0.2) 0%, rgba(0, 220, 255, 0.12) 30%, rgba(0, 200, 255, 0.06) 50%, transparent 75%)",
              filter: "blur(140px)",
            }}
          />
          <motion.div
            animate={{ opacity: [0.5, 0.75, 0.5], scale: [0.98, 1.02, 0.98] }}
            transition={{ duration: 3.5, ease: "easeInOut", repeat: Infinity }}
            style={{
              position: "absolute",
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%)",
              width: "1200px",
              height: "1200px",
              background: "radial-gradient(circle, rgba(0, 240, 255, 0.3) 0%, rgba(0, 230, 255, 0.18) 40%, rgba(0, 220, 255, 0.08) 60%, transparent 75%)",
              filter: "blur(100px)",
            }}
          />
          <motion.div
            animate={{ opacity: [0.6, 0.85, 0.6] }}
            transition={{ duration: 3, ease: "easeInOut", repeat: Infinity }}
            style={{
              position: "absolute",
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%)",
              width: "900px",
              height: "900px",
              background: "radial-gradient(circle, rgba(0, 240, 255, 0.5) 0%, rgba(0, 235, 255, 0.3) 40%, rgba(0, 230, 255, 0.15) 65%, transparent 85%)",
              filter: "blur(60px)",
            }}
          />

          {/* Core solid (BRIGHT CENTER WITH LOCK-IN PULSE) */}
          <motion.div
            animate={{
              scale: bootPhase === "locked" ? [1, 1.15, 1] : [1, 1.1, 1],
              opacity: bootPhase === "locked" ? [0.95, 1, 0.95] : [0.95, 1, 0.95],
            }}
            transition={{
              duration: bootPhase === "locked" ? 0.6 : 2.5,
              ease: "easeInOut",
              repeat: bootPhase === "locked" ? 2 : Infinity,
            }}
            style={{
              position: "absolute",
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%)",
              width: "130px",
              height: "130px",
              background: "radial-gradient(circle, rgba(255, 255, 255, 1) 0%, rgba(200, 250, 255, 0.95) 30%, rgba(0, 240, 255, 0.7) 100%)",
              borderRadius: "50%",
              boxShadow: bootPhase === "locked"
                ? "0 0 80px rgba(0, 240, 255, 1), 0 0 160px rgba(0, 240, 255, 0.9), 0 0 240px rgba(0, 240, 255, 0.7), 0 0 320px rgba(0, 240, 255, 0.5)"
                : "0 0 60px rgba(0, 240, 255, 1), 0 0 120px rgba(0, 240, 255, 0.8), 0 0 180px rgba(0, 240, 255, 0.5), 0 0 240px rgba(0, 240, 255, 0.3)",
            }}
          />

          {/* Cross beams (BRIGHT FLOWING) */}
          {[0, 90, 180, 270].map((angle) => (
            <motion.div
              key={`beam-${angle}`}
              animate={{ opacity: [0.4, 0.7, 0.4] }}
              transition={{ duration: 3, ease: "easeInOut", repeat: Infinity, delay: angle / 360 }}
              style={{
                position: "absolute",
                top: "50%",
                left: "50%",
                width: "700px",
                height: "180px",
                background: "linear-gradient(90deg, rgba(0, 240, 255, 0.5), rgba(0, 220, 255, 0.25), transparent)",
                transform: `translate(-50%, -50%) rotate(${angle}deg)`,
                transformOrigin: "left center",
                filter: "blur(8px)",
              }}
            />
          ))}

          {/* Orbital particles around core (NEW - RADIAL DATA MOTION) */}
          {orbitParticles.map((particle) => (
            <motion.div
              key={`orbit-${particle.id}`}
              animate={{
                rotate: 360,
              }}
              transition={{
                duration: particle.speed,
                ease: "linear",
                repeat: Infinity,
                delay: particle.delay,
              }}
              style={{
                position: "absolute",
                top: "50%",
                left: "50%",
                width: `${particle.orbit}px`,
                height: `${particle.orbit}px`,
                transform: "translate(-50%, -50%)",
              }}
            >
              <motion.div
                animate={{
                  opacity: [0.4, 0.9, 0.4],
                  scale: [0.8, 1.2, 0.8],
                }}
                transition={{
                  duration: 2 + Math.random(),
                  ease: "easeInOut",
                  repeat: Infinity,
                }}
                style={{
                  position: "absolute",
                  top: 0,
                  left: "50%",
                  width: `${particle.size}px`,
                  height: `${particle.size}px`,
                  background: "rgba(0, 240, 255, 1)",
                  borderRadius: "50%",
                  boxShadow: "0 0 12px rgba(0, 240, 255, 1), 0 0 24px rgba(0, 240, 255, 0.6)",
                  transform: "translateX(-50%)",
                }}
              />
            </motion.div>
          ))}

          {/* Dotted orbital paths (GRAVITATIONAL FEEL) */}
          {[220, 290, 360, 430].map((radius, i) => (
            <div
              key={`orbit-path-${i}`}
              style={{
                position: "absolute",
                top: "50%",
                left: "50%",
                width: `${radius}px`,
                height: `${radius}px`,
                border: "1px dashed rgba(0, 240, 255, 0.15)",
                borderRadius: "50%",
                transform: "translate(-50%, -50%)",
              }}
            />
          ))}
        </div>
      )}

      {/* HUD GLYPHS & DATA MARKERS (SYSTEM NOISE) */}
      {bootPhase !== "forbidden" && bootPhase !== "security-scan" && bootPhase !== "rings-init" && (
        <>
          {hudGlyphs.map((glyph) => (
            <motion.div
              key={`glyph-${glyph.id}`}
              animate={{
                opacity: [0, 0.4, 0],
              }}
              transition={{
                duration: glyph.duration,
                delay: glyph.delay,
                repeat: Infinity,
                repeatDelay: 1 + Math.random() * 2,
              }}
              style={{
                position: "absolute",
                left: `${glyph.x}%`,
                top: `${glyph.y}%`,
                fontSize: "10px",
                color: "rgba(0, 240, 255, 0.6)",
                fontFamily: "monospace",
                textShadow: "0 0 8px rgba(0, 240, 255, 0.8)",
                pointerEvents: "none",
                zIndex: 25,
              }}
            >
              {glyph.text}
            </motion.div>
          ))}
        </>
      )}

      {/* DEEP HACKER OVERLAY */}
      {bootPhase !== "forbidden" && bootPhase !== "security-scan" && bootPhase !== "rings-init" && (
        <>
          {/* Vertical data rain */}
          <motion.div
            animate={{ backgroundPositionY: ["0%", "100%"] }}
            transition={{ duration: 10, ease: "linear", repeat: Infinity }}
            style={{
              position: "absolute",
              inset: 0,
              backgroundImage: "linear-gradient(180deg, transparent 0%, rgba(0, 240, 255, 0.02) 50%, transparent 100%)",
              backgroundSize: "100% 300px",
              opacity: 0.12,
              pointerEvents: "none",
            }}
          />

          {/* Ghost hex grids (MORE VARIED SIZES) */}
          {hexGrids.map((hex) => (
            <motion.div
              key={hex.id}
              animate={{ opacity: [0, 0.06, 0], rotate: [45, 50, 45] }}
              transition={{
                duration: hex.duration,
                delay: hex.delay,
                repeat: Infinity,
                repeatDelay: 2,
              }}
              style={{
                position: "absolute",
                left: `${hex.x}%`,
                top: `${hex.y}%`,
                width: `${hex.size}px`,
                height: `${hex.size}px`,
                border: "1px solid rgba(0, 240, 255, 0.2)",
                transform: "rotate(45deg)",
                borderRadius: "4px",
              }}
            />
          ))}
        </>
      )}

      {/* TITLE MATERIALIZATION */}
      {(bootPhase === "title-reveal" || bootPhase === "locked") && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1.5, ease: "easeOut" }}
          style={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            textAlign: "center",
            zIndex: 30,
          }}
        >
          <motion.h1
            initial={{ filter: "blur(16px)", opacity: 0, letterSpacing: "0.5em" }}
            animate={{
              filter: ["blur(16px)", "blur(0px)"],
              opacity: [0, 1],
              letterSpacing: ["0.5em", "0.16em"],
            }}
            transition={{ duration: 1.4, ease: [0.23, 1, 0.32, 1] }}
            style={{
              fontFamily: "'Orbitron', 'Inter', sans-serif",
              fontSize: "clamp(40px, 7vw, 88px)",
              fontWeight: 700,
              color: "#ffffff",
              margin: 0,
              lineHeight: 1.1,
              textTransform: "uppercase",
              textShadow: "0 0 30px rgba(0, 240, 255, 0.6), 0 0 60px rgba(0, 240, 255, 0.3), 0 2px 8px rgba(0, 0, 0, 0.8)",
              WebkitFontSmoothing: "antialiased",
            }}
          >
            SMART AI CCTV
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.9, delay: 1.0, ease: [0.23, 1, 0.32, 1] }}
            style={{
              fontFamily: "'Inter', 'Roboto', sans-serif",
              fontSize: "clamp(12px, 2vw, 24px)",
              fontWeight: 400,
              color: "rgba(0, 240, 255, 0.95)",
              letterSpacing: "0.35em",
              margin: "16px 0 0 0",
              textTransform: "uppercase",
              textShadow: "0 0 20px rgba(0, 240, 255, 0.5), 0 1px 4px rgba(0, 0, 0, 0.8)",
              WebkitFontSmoothing: "antialiased",
            }}
          >
            SURVEILLANCE SYSTEM
          </motion.p>
        </motion.div>
      )}

      {/* CORNER UI BRACKETS (LARGER FOR MORE PRESENCE) */}
      {bootPhase !== "forbidden" && bootPhase !== "security-scan" && (
        <>
          {["top-left", "top-right", "bottom-left", "bottom-right"].map((corner) => {
            const isTop = corner.includes("top");
            const isLeft = corner.includes("left");
            return (
              <motion.div
                key={corner}
                initial={{ opacity: 0 }}
                animate={{ opacity: [0.35, 0.7, 0.35] }}
                transition={{
                  duration: 3.5,
                  ease: "easeInOut",
                  repeat: Infinity,
                  delay: corner === "top-left" ? 0 : corner === "top-right" ? 0.6 : corner === "bottom-right" ? 1.2 : 1.8,
                }}
                style={{
                  position: "absolute",
                  [isTop ? "top" : "bottom"]: "18px",
                  [isLeft ? "left" : "right"]: "18px",
                  width: "75px",
                  height: "75px",
                  borderTop: isTop ? "2px solid rgba(0, 240, 255, 0.45)" : "none",
                  borderBottom: !isTop ? "2px solid rgba(0, 240, 255, 0.45)" : "none",
                  borderLeft: isLeft ? "2px solid rgba(0, 240, 255, 0.45)" : "none",
                  borderRight: !isLeft ? "2px solid rgba(0, 240, 255, 0.45)" : "none",
                  boxShadow: isTop
                    ? (isLeft ? "0 -2px 12px rgba(0, 240, 255, 0.3), -2px 0 12px rgba(0, 240, 255, 0.3)" : "0 -2px 12px rgba(0, 240, 255, 0.3), 2px 0 12px rgba(0, 240, 255, 0.3)")
                    : (isLeft ? "0 2px 12px rgba(0, 240, 255, 0.3), -2px 0 12px rgba(0, 240, 255, 0.3)" : "0 2px 12px rgba(0, 240, 255, 0.3), 2px 0 12px rgba(0, 240, 255, 0.3)"),
                }}
              />
            );
          })}
        </>
      )}

      {/* Radial scanning arcs (BRIGHT SWEEPING EFFECTS) */}
      {bootPhase !== "forbidden" && bootPhase !== "security-scan" && bootPhase !== "rings-init" && (
        <>
          {[0, 120, 240].map((angle) => (
            <motion.div
              key={`arc-${angle}`}
              animate={{
                opacity: [0, 0.35, 0],
                rotate: [angle, angle + 35],
              }}
              transition={{
                opacity: { duration: 2.5, ease: "easeInOut" },
                rotate: { duration: 2.5, ease: "easeInOut" },
                repeat: Infinity,
                delay: angle / 120,
                repeatDelay: 4,
              }}
              style={{
                position: "absolute",
                top: "50%",
                left: "50%",
                width: "450px",
                height: "450px",
                border: "2px solid transparent",
                borderTopColor: "rgba(0, 240, 255, 0.5)",
                borderRadius: "50%",
                transform: "translate(-50%, -50%)",
                boxShadow: "0 0 30px rgba(0, 240, 255, 0.3), inset 0 0 30px rgba(0, 240, 255, 0.2)",
                zIndex: 6,
              }}
            />
          ))}
        </>
      )}
    </motion.div>
  );
};

export default EntranceAnimation;
