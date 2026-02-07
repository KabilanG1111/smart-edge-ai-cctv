import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navigation from "./components/Navigation";
import CustomCursor from "./components/CustomCursor";
import EntranceAnimation from "./components/EntranceAnimation";
import LiveStream from "./pages/LiveStream";
import EvidenceVault from "./pages/EvidenceVault";
import AlertCenter from "./pages/AlertCenter";
import AICopilot from "./pages/AICopilot";
import "./App.css";

function App() {
  const [animationComplete, setAnimationComplete] = useState(() => {
    return sessionStorage.getItem("entrance-complete") === "true";
  });

  const handleEntranceComplete = () => {
    sessionStorage.setItem("entrance-complete", "true");
    setAnimationComplete(true);
  };

  if (!animationComplete) {
    return <EntranceAnimation onComplete={handleEntranceComplete} />;
  }

  return (
    <Router>
      <CustomCursor />
      <div className="layout-frame">
        <Navigation />

        <main className="main-stage">
          <div className="stage-content">
            <Routes>
              <Route path="/" element={<LiveStream />} />
              <Route path="/evidence" element={<EvidenceVault />} />
              <Route path="/alerts" element={<AlertCenter />} />
              <Route path="/copilot" element={<AICopilot />} />
            </Routes>
          </div>

          <div className="security-badge">
            <div className="badge-icon">🔒</div>
            <div className="badge-text">
              <div className="b-main">100% LOCAL PROCESSING</div>
              <div className="b-sub">ZERO CLOUD UPLOAD // GDPR COMPLIANT</div>
            </div>
          </div>
        </main>
      </div>
    </Router>
  );
}

export default App;
