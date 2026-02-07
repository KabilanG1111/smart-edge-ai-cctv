import React, { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const EntranceAnimation = ({ onComplete }) => {
  const [show, setShow] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShow(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  const handleExitComplete = () => {
    if (onComplete) onComplete();
  };

  return (
    <AnimatePresence onExitComplete={handleExitComplete}>
      {show && (
        <motion.div
          initial={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.8, ease: "easeInOut" }}
          style={{
            position: "fixed",
            inset: 0,
            zIndex: 9999,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            background: "linear-gradient(135deg, #000000 0%, #0a0e1a 50%, #000814 100%)",
            overflow: "hidden",
          }}
        >
          {/* Animated Grid Background */}
          <div
            style={{
              position: "absolute",
              inset: 0,
              backgroundImage: `
                linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px)
              `,
              backgroundSize: "60px 60px",
              animation: "gridPulse 4s ease-in-out infinite",
            }}
          />

          {/* Central Glow */}
          <motion.div
            animate={{
              scale: [1, 1.3, 1],
              opacity: [0.3, 0.6, 0.3],
            }}
            transition={{
              duration: 3,
              ease: "easeInOut",
              repeat: Infinity,
            }}
            style={{
              position: "absolute",
              width: "600px",
              height: "600px",
              borderRadius: "50%",
              background: "radial-gradient(circle, rgba(0, 240, 255, 0.25) 0%, transparent 70%)",
              filter: "blur(60px)",
            }}
          />

          {/* Rotating Rings */}
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              animate={{ rotate: 360 }}
              transition={{
                duration: 15 + i * 5,
                ease: "linear",
                repeat: Infinity,
              }}
              style={{
                position: "absolute",
                width: `${300 + i * 100}px`,
                height: `${300 + i * 100}px`,
                border: "1px solid rgba(0, 240, 255, 0.15)",
                borderRadius: "50%",
                borderTopColor: "rgba(0, 240, 255, 0.5)",
                borderRightColor: "rgba(0, 240, 255, 0.3)",
              }}
            />
          ))}

          {/* Main Text */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            style={{
              position: "relative",
              zIndex: 10,
              textAlign: "center",
            }}
          >
            <motion.h1
              animate={{
                textShadow: [
                  "0 0 20px rgba(0, 240, 255, 0.5)",
                  "0 0 40px rgba(0, 240, 255, 0.8)",
                  "0 0 20px rgba(0, 240, 255, 0.5)",
                ],
              }}
              transition={{
                duration: 2,
                ease: "easeInOut",
                repeat: Infinity,
              }}
              style={{
                fontFamily: "'Orbitron', sans-serif",
                fontSize: "clamp(32px, 5vw, 56px)",
                fontWeight: 900,
                color: "#ffffff",
                letterSpacing: "0.15em",
                margin: 0,
                marginBottom: "16px",
              }}
            >
              SMART EDGE AI CCTV
            </motion.h1>

            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6, duration: 0.8 }}
              style={{
                fontFamily: "'Inter', sans-serif",
                fontSize: "clamp(12px, 1.5vw, 18px)",
                fontWeight: 600,
                color: "rgba(0, 240, 255, 0.9)",
                letterSpacing: "0.25em",
                margin: 0,
                textTransform: "uppercase",
              }}
            >
              Surveillance System
            </motion.p>
          </motion.div>

          {/* Scanning Line */}
          <motion.div
            animate={{
              y: ["-100%", "100%"],
            }}
            transition={{
              duration: 2,
              ease: "linear",
              repeat: Infinity,
            }}
            style={{
              position: "absolute",
              left: 0,
              right: 0,
              height: "2px",
              background: "linear-gradient(90deg, transparent, rgba(0, 240, 255, 0.8), transparent)",
              boxShadow: "0 0 20px rgba(0, 240, 255, 0.6)",
            }}
          />

          {/* Corner Brackets */}
          {["top-left", "top-right", "bottom-left", "bottom-right"].map((corner) => {
            const isTop = corner.includes("top");
            const isLeft = corner.includes("left");

            return (
              <motion.div
                key={corner}
                initial={{ opacity: 0 }}
                animate={{ opacity: [0.3, 1, 0.3] }}
                transition={{
                  delay: 0.2,
                  duration: 2,
                  repeat: Infinity,
                }}
                style={{
                  position: "absolute",
                  [isTop ? "top" : "bottom"]: "40px",
                  [isLeft ? "left" : "right"]: "40px",
                  width: "60px",
                  height: "60px",
                  borderTop: isTop ? "2px solid rgba(0, 240, 255, 0.6)" : "none",
                  borderBottom: !isTop ? "2px solid rgba(0, 240, 255, 0.6)" : "none",
                  borderLeft: isLeft ? "2px solid rgba(0, 240, 255, 0.6)" : "none",
                  borderRight: !isLeft ? "2px solid rgba(0, 240, 255, 0.6)" : "none",
                }}
              />
            );
          })}

          {/* CSS Keyframes */}
          <style>{`
            @keyframes gridPulse {
              0%, 100% { opacity: 0.3; }
              50% { opacity: 0.6; }
            }
          `}</style>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default EntranceAnimation;
