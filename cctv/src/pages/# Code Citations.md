# Code Citations

## License: unknown
https://github.com/Andy-set-studio/personal-site-hylia/blob/765710f65eaee9ab6d3bd5170e6a4c61d3e95534/src/posts/a-modern-css-reset.md

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:
```


## License: unknown
https://github.com/Andy-set-studio/personal-site-hylia/blob/765710f65eaee9ab6d3bd5170e6a4c61d3e95534/src/posts/a-modern-css-reset.md

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:
```


## License: unknown
https://github.com/Andy-set-studio/personal-site-hylia/blob/765710f65eaee9ab6d3bd5170e6a4c61d3e95534/src/posts/a-modern-css-reset.md

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:
```


## License: unknown
https://github.com/Andy-set-studio/personal-site-hylia/blob/765710f65eaee9ab6d3bd5170e6a4c61d3e95534/src/posts/a-modern-css-reset.md

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:
```


## License: unknown
https://github.com/Andy-set-studio/personal-site-hylia/blob/765710f65eaee9ab6d3bd5170e6a4c61d3e95534/src/posts/a-modern-css-reset.md

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:
```


## License: unknown
https://github.com/Andy-set-studio/personal-site-hylia/blob/765710f65eaee9ab6d3bd5170e6a4c61d3e95534/src/posts/a-modern-css-reset.md

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:
```


## License: unknown
https://github.com/Andy-set-studio/personal-site-hylia/blob/765710f65eaee9ab6d3bd5170e6a4c61d3e95534/src/posts/a-modern-css-reset.md

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:
```


## License: unknown
https://github.com/Andy-set-studio/personal-site-hylia/blob/765710f65eaee9ab6d3bd5170e6a4c61d3e95534/src/posts/a-modern-css-reset.md

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:
```


## License: unknown
https://github.com/Andy-set-studio/personal-site-hylia/blob/765710f65eaee9ab6d3bd5170e6a4c61d3e95534/src/posts/a-modern-css-reset.md

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:
```


## License: unknown
https://github.com/Riku115/Riku115/blob/801e8813f86845d8d23b4f7868ce02885faad799/assets/theme.css

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:hover {
    transform: none;
  }
}
```

### **GPU Optimization**
```css
/* Force GPU acceleration for animated elements */
.animated-element {
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

/* Remove will-change after animation */
.animated-element.animation-complete {
  will-change: auto;
}
```

### **Frame Rate Control**
```javascript
// Throttle to 30fps for background effects
let lastFrameTime = 0;
const targetFPS = 30;
const frameInterval = 1000 / targetFPS;

function animate(currentTime) {
  requestAnimationFrame(animate);
  
  const elapsed = currentTime - lastFrameTime;
  if (elapsed < frameInterval) return;
  
  lastFrameTime = currentTime - (elapsed % frameInterval);
  
  // Animation logic here
}
```

### **Canvas Isolation**
```javascript
// Separate canvas for 3D, prevent layout thrashing
const Canvas3D = () => (
  <Canvas
    style={{
      position: 'fixed',
      top: 0,
      left: 0,
      zIndex: 0,
      pointerEvents: 'none'
    }}
    dpr={[1, 2]} // Limit pixel ratio to 2x max
    performance={{ min: 0.5 }} // Throttle to 30fps if needed
  >
    <Scene />
  </Canvas>
);

// 2D UI overlay
const UIOverlay = () => (
  <div style={{ position: 'relative', zIndex: 1 }}>
    {/* All UI components */}
  </div>
);
```

### **Conditional Rendering by Device**
```javascript
const [show3D, setShow3D] = useState(false);

useEffect(() => {
  const shouldShow = 
    window.innerWidth > 1024 && // Desktop only
    !window.matchMedia('(prefers-reduced-motion: reduce)').matches &&
    navigator.hardwareConcurrency > 4; // 4+ CPU cores
  
  setShow3D(shouldShow);
}, []);

return show3D ? <Canvas3D /> : <StaticBackground />;
```

---

## 5️⃣ Required Design Constraints

### **Color Palette (Strict)**
```css
:root {
  /* Base */
  --core-dark: #050505;
  --core-panel: #0a0c10;
  --core-border: rgba(255, 255, 255, 0.08);
  
  /* Accent */
  --cyan-bright: #00f0ff;
  --cyan-dim: #005f66;
  
  /* Semantic */
  --critical: #ff1744;
  --high: #ff9100;
  --medium: #ffea00;
  --success: #00e676;
  
  /* Text */
  --text-primary: #ffffff;
  --text-secondary: #aaaaaa;
  --text-tertiary: #666666;
}
```

### **Motion Timing Standards**
```css
:root {
  /* Easing */
  --ease-military: cubic-bezier(0.4, 0, 0.6, 1);
  --ease-tech: cubic-bezier(0.4, 0, 0.2, 1);
  
  /* Durations */
  --duration-instant: 150ms;
  --duration-quick: 250ms;
  --duration-normal: 400ms;
  --duration-deliberate: 600ms;
  --duration-slow: 800ms;
}

/* Rules */
nothing_faster_than: 150ms;  // Feels instant
nothing_slower_than: 800ms;  // Feels laggy
default_duration: 400ms;      // Balanced
```

### **Animation Density Limits**
```javascript
constraints = {
  maxParticles: 0,              // No particle systems
  maxConcurrentAnimations: 5,   // Prevent jank
  backgroundMotionCount: 3,     // Grid + sweep + neural lines
  glowEffects: "focused elements only",
  pulsingElements: "critical alerts only (<2s cycles)"
}
```

### **Typography System**
```css
:root {
  --font-tech: 'Orbitron', sans-serif;   // Headers, system labels
  --font-ui: 'Inter', sans-serif;        // UI text, paragraphs
  --font-mono: 'JetBrains Mono', monospace; // Data, code, IDs
}

/* Size scale */
--text-xs: 10px;   // Labels
--text-sm: 12px;   // UI text
--text-base: 14px; // Body
--text-lg: 16px;   // Subheadings
--text-xl: 24px;   // Section headers
--text-2xl: 48px;  // Hero headlines
```

### **Spacing System (8px base)**
```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-8: 64px;
}
```

### **Information
```


## License: unknown
https://github.com/Riku115/Riku115/blob/801e8813f86845d8d23b4f7868ce02885faad799/assets/theme.css

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:hover {
    transform: none;
  }
}
```

### **GPU Optimization**
```css
/* Force GPU acceleration for animated elements */
.animated-element {
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

/* Remove will-change after animation */
.animated-element.animation-complete {
  will-change: auto;
}
```

### **Frame Rate Control**
```javascript
// Throttle to 30fps for background effects
let lastFrameTime = 0;
const targetFPS = 30;
const frameInterval = 1000 / targetFPS;

function animate(currentTime) {
  requestAnimationFrame(animate);
  
  const elapsed = currentTime - lastFrameTime;
  if (elapsed < frameInterval) return;
  
  lastFrameTime = currentTime - (elapsed % frameInterval);
  
  // Animation logic here
}
```

### **Canvas Isolation**
```javascript
// Separate canvas for 3D, prevent layout thrashing
const Canvas3D = () => (
  <Canvas
    style={{
      position: 'fixed',
      top: 0,
      left: 0,
      zIndex: 0,
      pointerEvents: 'none'
    }}
    dpr={[1, 2]} // Limit pixel ratio to 2x max
    performance={{ min: 0.5 }} // Throttle to 30fps if needed
  >
    <Scene />
  </Canvas>
);

// 2D UI overlay
const UIOverlay = () => (
  <div style={{ position: 'relative', zIndex: 1 }}>
    {/* All UI components */}
  </div>
);
```

### **Conditional Rendering by Device**
```javascript
const [show3D, setShow3D] = useState(false);

useEffect(() => {
  const shouldShow = 
    window.innerWidth > 1024 && // Desktop only
    !window.matchMedia('(prefers-reduced-motion: reduce)').matches &&
    navigator.hardwareConcurrency > 4; // 4+ CPU cores
  
  setShow3D(shouldShow);
}, []);

return show3D ? <Canvas3D /> : <StaticBackground />;
```

---

## 5️⃣ Required Design Constraints

### **Color Palette (Strict)**
```css
:root {
  /* Base */
  --core-dark: #050505;
  --core-panel: #0a0c10;
  --core-border: rgba(255, 255, 255, 0.08);
  
  /* Accent */
  --cyan-bright: #00f0ff;
  --cyan-dim: #005f66;
  
  /* Semantic */
  --critical: #ff1744;
  --high: #ff9100;
  --medium: #ffea00;
  --success: #00e676;
  
  /* Text */
  --text-primary: #ffffff;
  --text-secondary: #aaaaaa;
  --text-tertiary: #666666;
}
```

### **Motion Timing Standards**
```css
:root {
  /* Easing */
  --ease-military: cubic-bezier(0.4, 0, 0.6, 1);
  --ease-tech: cubic-bezier(0.4, 0, 0.2, 1);
  
  /* Durations */
  --duration-instant: 150ms;
  --duration-quick: 250ms;
  --duration-normal: 400ms;
  --duration-deliberate: 600ms;
  --duration-slow: 800ms;
}

/* Rules */
nothing_faster_than: 150ms;  // Feels instant
nothing_slower_than: 800ms;  // Feels laggy
default_duration: 400ms;      // Balanced
```

### **Animation Density Limits**
```javascript
constraints = {
  maxParticles: 0,              // No particle systems
  maxConcurrentAnimations: 5,   // Prevent jank
  backgroundMotionCount: 3,     // Grid + sweep + neural lines
  glowEffects: "focused elements only",
  pulsingElements: "critical alerts only (<2s cycles)"
}
```

### **Typography System**
```css
:root {
  --font-tech: 'Orbitron', sans-serif;   // Headers, system labels
  --font-ui: 'Inter', sans-serif;        // UI text, paragraphs
  --font-mono: 'JetBrains Mono', monospace; // Data, code, IDs
}

/* Size scale */
--text-xs: 10px;   // Labels
--text-sm: 12px;   // UI text
--text-base: 14px; // Body
--text-lg: 16px;   // Subheadings
--text-xl: 24px;   // Section headers
--text-2xl: 48px;  // Hero headlines
```

### **Spacing System (8px base)**
```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-8: 64px;
}
```

### **Information
```


## License: unknown
https://github.com/Riku115/Riku115/blob/801e8813f86845d8d23b4f7868ce02885faad799/assets/theme.css

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:hover {
    transform: none;
  }
}
```

### **GPU Optimization**
```css
/* Force GPU acceleration for animated elements */
.animated-element {
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

/* Remove will-change after animation */
.animated-element.animation-complete {
  will-change: auto;
}
```

### **Frame Rate Control**
```javascript
// Throttle to 30fps for background effects
let lastFrameTime = 0;
const targetFPS = 30;
const frameInterval = 1000 / targetFPS;

function animate(currentTime) {
  requestAnimationFrame(animate);
  
  const elapsed = currentTime - lastFrameTime;
  if (elapsed < frameInterval) return;
  
  lastFrameTime = currentTime - (elapsed % frameInterval);
  
  // Animation logic here
}
```

### **Canvas Isolation**
```javascript
// Separate canvas for 3D, prevent layout thrashing
const Canvas3D = () => (
  <Canvas
    style={{
      position: 'fixed',
      top: 0,
      left: 0,
      zIndex: 0,
      pointerEvents: 'none'
    }}
    dpr={[1, 2]} // Limit pixel ratio to 2x max
    performance={{ min: 0.5 }} // Throttle to 30fps if needed
  >
    <Scene />
  </Canvas>
);

// 2D UI overlay
const UIOverlay = () => (
  <div style={{ position: 'relative', zIndex: 1 }}>
    {/* All UI components */}
  </div>
);
```

### **Conditional Rendering by Device**
```javascript
const [show3D, setShow3D] = useState(false);

useEffect(() => {
  const shouldShow = 
    window.innerWidth > 1024 && // Desktop only
    !window.matchMedia('(prefers-reduced-motion: reduce)').matches &&
    navigator.hardwareConcurrency > 4; // 4+ CPU cores
  
  setShow3D(shouldShow);
}, []);

return show3D ? <Canvas3D /> : <StaticBackground />;
```

---

## 5️⃣ Required Design Constraints

### **Color Palette (Strict)**
```css
:root {
  /* Base */
  --core-dark: #050505;
  --core-panel: #0a0c10;
  --core-border: rgba(255, 255, 255, 0.08);
  
  /* Accent */
  --cyan-bright: #00f0ff;
  --cyan-dim: #005f66;
  
  /* Semantic */
  --critical: #ff1744;
  --high: #ff9100;
  --medium: #ffea00;
  --success: #00e676;
  
  /* Text */
  --text-primary: #ffffff;
  --text-secondary: #aaaaaa;
  --text-tertiary: #666666;
}
```

### **Motion Timing Standards**
```css
:root {
  /* Easing */
  --ease-military: cubic-bezier(0.4, 0, 0.6, 1);
  --ease-tech: cubic-bezier(0.4, 0, 0.2, 1);
  
  /* Durations */
  --duration-instant: 150ms;
  --duration-quick: 250ms;
  --duration-normal: 400ms;
  --duration-deliberate: 600ms;
  --duration-slow: 800ms;
}

/* Rules */
nothing_faster_than: 150ms;  // Feels instant
nothing_slower_than: 800ms;  // Feels laggy
default_duration: 400ms;      // Balanced
```

### **Animation Density Limits**
```javascript
constraints = {
  maxParticles: 0,              // No particle systems
  maxConcurrentAnimations: 5,   // Prevent jank
  backgroundMotionCount: 3,     // Grid + sweep + neural lines
  glowEffects: "focused elements only",
  pulsingElements: "critical alerts only (<2s cycles)"
}
```

### **Typography System**
```css
:root {
  --font-tech: 'Orbitron', sans-serif;   // Headers, system labels
  --font-ui: 'Inter', sans-serif;        // UI text, paragraphs
  --font-mono: 'JetBrains Mono', monospace; // Data, code, IDs
}

/* Size scale */
--text-xs: 10px;   // Labels
--text-sm: 12px;   // UI text
--text-base: 14px; // Body
--text-lg: 16px;   // Subheadings
--text-xl: 24px;   // Section headers
--text-2xl: 48px;  // Hero headlines
```

### **Spacing System (8px base)**
```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-8: 64px;
}
```

### **Information
```


## License: unknown
https://github.com/Riku115/Riku115/blob/801e8813f86845d8d23b4f7868ce02885faad799/assets/theme.css

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:hover {
    transform: none;
  }
}
```

### **GPU Optimization**
```css
/* Force GPU acceleration for animated elements */
.animated-element {
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

/* Remove will-change after animation */
.animated-element.animation-complete {
  will-change: auto;
}
```

### **Frame Rate Control**
```javascript
// Throttle to 30fps for background effects
let lastFrameTime = 0;
const targetFPS = 30;
const frameInterval = 1000 / targetFPS;

function animate(currentTime) {
  requestAnimationFrame(animate);
  
  const elapsed = currentTime - lastFrameTime;
  if (elapsed < frameInterval) return;
  
  lastFrameTime = currentTime - (elapsed % frameInterval);
  
  // Animation logic here
}
```

### **Canvas Isolation**
```javascript
// Separate canvas for 3D, prevent layout thrashing
const Canvas3D = () => (
  <Canvas
    style={{
      position: 'fixed',
      top: 0,
      left: 0,
      zIndex: 0,
      pointerEvents: 'none'
    }}
    dpr={[1, 2]} // Limit pixel ratio to 2x max
    performance={{ min: 0.5 }} // Throttle to 30fps if needed
  >
    <Scene />
  </Canvas>
);

// 2D UI overlay
const UIOverlay = () => (
  <div style={{ position: 'relative', zIndex: 1 }}>
    {/* All UI components */}
  </div>
);
```

### **Conditional Rendering by Device**
```javascript
const [show3D, setShow3D] = useState(false);

useEffect(() => {
  const shouldShow = 
    window.innerWidth > 1024 && // Desktop only
    !window.matchMedia('(prefers-reduced-motion: reduce)').matches &&
    navigator.hardwareConcurrency > 4; // 4+ CPU cores
  
  setShow3D(shouldShow);
}, []);

return show3D ? <Canvas3D /> : <StaticBackground />;
```

---

## 5️⃣ Required Design Constraints

### **Color Palette (Strict)**
```css
:root {
  /* Base */
  --core-dark: #050505;
  --core-panel: #0a0c10;
  --core-border: rgba(255, 255, 255, 0.08);
  
  /* Accent */
  --cyan-bright: #00f0ff;
  --cyan-dim: #005f66;
  
  /* Semantic */
  --critical: #ff1744;
  --high: #ff9100;
  --medium: #ffea00;
  --success: #00e676;
  
  /* Text */
  --text-primary: #ffffff;
  --text-secondary: #aaaaaa;
  --text-tertiary: #666666;
}
```

### **Motion Timing Standards**
```css
:root {
  /* Easing */
  --ease-military: cubic-bezier(0.4, 0, 0.6, 1);
  --ease-tech: cubic-bezier(0.4, 0, 0.2, 1);
  
  /* Durations */
  --duration-instant: 150ms;
  --duration-quick: 250ms;
  --duration-normal: 400ms;
  --duration-deliberate: 600ms;
  --duration-slow: 800ms;
}

/* Rules */
nothing_faster_than: 150ms;  // Feels instant
nothing_slower_than: 800ms;  // Feels laggy
default_duration: 400ms;      // Balanced
```

### **Animation Density Limits**
```javascript
constraints = {
  maxParticles: 0,              // No particle systems
  maxConcurrentAnimations: 5,   // Prevent jank
  backgroundMotionCount: 3,     // Grid + sweep + neural lines
  glowEffects: "focused elements only",
  pulsingElements: "critical alerts only (<2s cycles)"
}
```

### **Typography System**
```css
:root {
  --font-tech: 'Orbitron', sans-serif;   // Headers, system labels
  --font-ui: 'Inter', sans-serif;        // UI text, paragraphs
  --font-mono: 'JetBrains Mono', monospace; // Data, code, IDs
}

/* Size scale */
--text-xs: 10px;   // Labels
--text-sm: 12px;   // UI text
--text-base: 14px; // Body
--text-lg: 16px;   // Subheadings
--text-xl: 24px;   // Section headers
--text-2xl: 48px;  // Hero headlines
```

### **Spacing System (8px base)**
```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-8: 64px;
}
```

### **Information
```


## License: unknown
https://github.com/Riku115/Riku115/blob/801e8813f86845d8d23b4f7868ce02885faad799/assets/theme.css

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:hover {
    transform: none;
  }
}
```

### **GPU Optimization**
```css
/* Force GPU acceleration for animated elements */
.animated-element {
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

/* Remove will-change after animation */
.animated-element.animation-complete {
  will-change: auto;
}
```

### **Frame Rate Control**
```javascript
// Throttle to 30fps for background effects
let lastFrameTime = 0;
const targetFPS = 30;
const frameInterval = 1000 / targetFPS;

function animate(currentTime) {
  requestAnimationFrame(animate);
  
  const elapsed = currentTime - lastFrameTime;
  if (elapsed < frameInterval) return;
  
  lastFrameTime = currentTime - (elapsed % frameInterval);
  
  // Animation logic here
}
```

### **Canvas Isolation**
```javascript
// Separate canvas for 3D, prevent layout thrashing
const Canvas3D = () => (
  <Canvas
    style={{
      position: 'fixed',
      top: 0,
      left: 0,
      zIndex: 0,
      pointerEvents: 'none'
    }}
    dpr={[1, 2]} // Limit pixel ratio to 2x max
    performance={{ min: 0.5 }} // Throttle to 30fps if needed
  >
    <Scene />
  </Canvas>
);

// 2D UI overlay
const UIOverlay = () => (
  <div style={{ position: 'relative', zIndex: 1 }}>
    {/* All UI components */}
  </div>
);
```

### **Conditional Rendering by Device**
```javascript
const [show3D, setShow3D] = useState(false);

useEffect(() => {
  const shouldShow = 
    window.innerWidth > 1024 && // Desktop only
    !window.matchMedia('(prefers-reduced-motion: reduce)').matches &&
    navigator.hardwareConcurrency > 4; // 4+ CPU cores
  
  setShow3D(shouldShow);
}, []);

return show3D ? <Canvas3D /> : <StaticBackground />;
```

---

## 5️⃣ Required Design Constraints

### **Color Palette (Strict)**
```css
:root {
  /* Base */
  --core-dark: #050505;
  --core-panel: #0a0c10;
  --core-border: rgba(255, 255, 255, 0.08);
  
  /* Accent */
  --cyan-bright: #00f0ff;
  --cyan-dim: #005f66;
  
  /* Semantic */
  --critical: #ff1744;
  --high: #ff9100;
  --medium: #ffea00;
  --success: #00e676;
  
  /* Text */
  --text-primary: #ffffff;
  --text-secondary: #aaaaaa;
  --text-tertiary: #666666;
}
```

### **Motion Timing Standards**
```css
:root {
  /* Easing */
  --ease-military: cubic-bezier(0.4, 0, 0.6, 1);
  --ease-tech: cubic-bezier(0.4, 0, 0.2, 1);
  
  /* Durations */
  --duration-instant: 150ms;
  --duration-quick: 250ms;
  --duration-normal: 400ms;
  --duration-deliberate: 600ms;
  --duration-slow: 800ms;
}

/* Rules */
nothing_faster_than: 150ms;  // Feels instant
nothing_slower_than: 800ms;  // Feels laggy
default_duration: 400ms;      // Balanced
```

### **Animation Density Limits**
```javascript
constraints = {
  maxParticles: 0,              // No particle systems
  maxConcurrentAnimations: 5,   // Prevent jank
  backgroundMotionCount: 3,     // Grid + sweep + neural lines
  glowEffects: "focused elements only",
  pulsingElements: "critical alerts only (<2s cycles)"
}
```

### **Typography System**
```css
:root {
  --font-tech: 'Orbitron', sans-serif;   // Headers, system labels
  --font-ui: 'Inter', sans-serif;        // UI text, paragraphs
  --font-mono: 'JetBrains Mono', monospace; // Data, code, IDs
}

/* Size scale */
--text-xs: 10px;   // Labels
--text-sm: 12px;   // UI text
--text-base: 14px; // Body
--text-lg: 16px;   // Subheadings
--text-xl: 24px;   // Section headers
--text-2xl: 48px;  // Hero headlines
```

### **Spacing System (8px base)**
```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-8: 64px;
}
```

### **Information
```


## License: unknown
https://github.com/Riku115/Riku115/blob/801e8813f86845d8d23b4f7868ce02885faad799/assets/theme.css

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:hover {
    transform: none;
  }
}
```

### **GPU Optimization**
```css
/* Force GPU acceleration for animated elements */
.animated-element {
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

/* Remove will-change after animation */
.animated-element.animation-complete {
  will-change: auto;
}
```

### **Frame Rate Control**
```javascript
// Throttle to 30fps for background effects
let lastFrameTime = 0;
const targetFPS = 30;
const frameInterval = 1000 / targetFPS;

function animate(currentTime) {
  requestAnimationFrame(animate);
  
  const elapsed = currentTime - lastFrameTime;
  if (elapsed < frameInterval) return;
  
  lastFrameTime = currentTime - (elapsed % frameInterval);
  
  // Animation logic here
}
```

### **Canvas Isolation**
```javascript
// Separate canvas for 3D, prevent layout thrashing
const Canvas3D = () => (
  <Canvas
    style={{
      position: 'fixed',
      top: 0,
      left: 0,
      zIndex: 0,
      pointerEvents: 'none'
    }}
    dpr={[1, 2]} // Limit pixel ratio to 2x max
    performance={{ min: 0.5 }} // Throttle to 30fps if needed
  >
    <Scene />
  </Canvas>
);

// 2D UI overlay
const UIOverlay = () => (
  <div style={{ position: 'relative', zIndex: 1 }}>
    {/* All UI components */}
  </div>
);
```

### **Conditional Rendering by Device**
```javascript
const [show3D, setShow3D] = useState(false);

useEffect(() => {
  const shouldShow = 
    window.innerWidth > 1024 && // Desktop only
    !window.matchMedia('(prefers-reduced-motion: reduce)').matches &&
    navigator.hardwareConcurrency > 4; // 4+ CPU cores
  
  setShow3D(shouldShow);
}, []);

return show3D ? <Canvas3D /> : <StaticBackground />;
```

---

## 5️⃣ Required Design Constraints

### **Color Palette (Strict)**
```css
:root {
  /* Base */
  --core-dark: #050505;
  --core-panel: #0a0c10;
  --core-border: rgba(255, 255, 255, 0.08);
  
  /* Accent */
  --cyan-bright: #00f0ff;
  --cyan-dim: #005f66;
  
  /* Semantic */
  --critical: #ff1744;
  --high: #ff9100;
  --medium: #ffea00;
  --success: #00e676;
  
  /* Text */
  --text-primary: #ffffff;
  --text-secondary: #aaaaaa;
  --text-tertiary: #666666;
}
```

### **Motion Timing Standards**
```css
:root {
  /* Easing */
  --ease-military: cubic-bezier(0.4, 0, 0.6, 1);
  --ease-tech: cubic-bezier(0.4, 0, 0.2, 1);
  
  /* Durations */
  --duration-instant: 150ms;
  --duration-quick: 250ms;
  --duration-normal: 400ms;
  --duration-deliberate: 600ms;
  --duration-slow: 800ms;
}

/* Rules */
nothing_faster_than: 150ms;  // Feels instant
nothing_slower_than: 800ms;  // Feels laggy
default_duration: 400ms;      // Balanced
```

### **Animation Density Limits**
```javascript
constraints = {
  maxParticles: 0,              // No particle systems
  maxConcurrentAnimations: 5,   // Prevent jank
  backgroundMotionCount: 3,     // Grid + sweep + neural lines
  glowEffects: "focused elements only",
  pulsingElements: "critical alerts only (<2s cycles)"
}
```

### **Typography System**
```css
:root {
  --font-tech: 'Orbitron', sans-serif;   // Headers, system labels
  --font-ui: 'Inter', sans-serif;        // UI text, paragraphs
  --font-mono: 'JetBrains Mono', monospace; // Data, code, IDs
}

/* Size scale */
--text-xs: 10px;   // Labels
--text-sm: 12px;   // UI text
--text-base: 14px; // Body
--text-lg: 16px;   // Subheadings
--text-xl: 24px;   // Section headers
--text-2xl: 48px;  // Hero headlines
```

### **Spacing System (8px base)**
```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-8: 64px;
}
```

### **Information
```


## License: unknown
https://github.com/Riku115/Riku115/blob/801e8813f86845d8d23b4f7868ce02885faad799/assets/theme.css

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:hover {
    transform: none;
  }
}
```

### **GPU Optimization**
```css
/* Force GPU acceleration for animated elements */
.animated-element {
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

/* Remove will-change after animation */
.animated-element.animation-complete {
  will-change: auto;
}
```

### **Frame Rate Control**
```javascript
// Throttle to 30fps for background effects
let lastFrameTime = 0;
const targetFPS = 30;
const frameInterval = 1000 / targetFPS;

function animate(currentTime) {
  requestAnimationFrame(animate);
  
  const elapsed = currentTime - lastFrameTime;
  if (elapsed < frameInterval) return;
  
  lastFrameTime = currentTime - (elapsed % frameInterval);
  
  // Animation logic here
}
```

### **Canvas Isolation**
```javascript
// Separate canvas for 3D, prevent layout thrashing
const Canvas3D = () => (
  <Canvas
    style={{
      position: 'fixed',
      top: 0,
      left: 0,
      zIndex: 0,
      pointerEvents: 'none'
    }}
    dpr={[1, 2]} // Limit pixel ratio to 2x max
    performance={{ min: 0.5 }} // Throttle to 30fps if needed
  >
    <Scene />
  </Canvas>
);

// 2D UI overlay
const UIOverlay = () => (
  <div style={{ position: 'relative', zIndex: 1 }}>
    {/* All UI components */}
  </div>
);
```

### **Conditional Rendering by Device**
```javascript
const [show3D, setShow3D] = useState(false);

useEffect(() => {
  const shouldShow = 
    window.innerWidth > 1024 && // Desktop only
    !window.matchMedia('(prefers-reduced-motion: reduce)').matches &&
    navigator.hardwareConcurrency > 4; // 4+ CPU cores
  
  setShow3D(shouldShow);
}, []);

return show3D ? <Canvas3D /> : <StaticBackground />;
```

---

## 5️⃣ Required Design Constraints

### **Color Palette (Strict)**
```css
:root {
  /* Base */
  --core-dark: #050505;
  --core-panel: #0a0c10;
  --core-border: rgba(255, 255, 255, 0.08);
  
  /* Accent */
  --cyan-bright: #00f0ff;
  --cyan-dim: #005f66;
  
  /* Semantic */
  --critical: #ff1744;
  --high: #ff9100;
  --medium: #ffea00;
  --success: #00e676;
  
  /* Text */
  --text-primary: #ffffff;
  --text-secondary: #aaaaaa;
  --text-tertiary: #666666;
}
```

### **Motion Timing Standards**
```css
:root {
  /* Easing */
  --ease-military: cubic-bezier(0.4, 0, 0.6, 1);
  --ease-tech: cubic-bezier(0.4, 0, 0.2, 1);
  
  /* Durations */
  --duration-instant: 150ms;
  --duration-quick: 250ms;
  --duration-normal: 400ms;
  --duration-deliberate: 600ms;
  --duration-slow: 800ms;
}

/* Rules */
nothing_faster_than: 150ms;  // Feels instant
nothing_slower_than: 800ms;  // Feels laggy
default_duration: 400ms;      // Balanced
```

### **Animation Density Limits**
```javascript
constraints = {
  maxParticles: 0,              // No particle systems
  maxConcurrentAnimations: 5,   // Prevent jank
  backgroundMotionCount: 3,     // Grid + sweep + neural lines
  glowEffects: "focused elements only",
  pulsingElements: "critical alerts only (<2s cycles)"
}
```

### **Typography System**
```css
:root {
  --font-tech: 'Orbitron', sans-serif;   // Headers, system labels
  --font-ui: 'Inter', sans-serif;        // UI text, paragraphs
  --font-mono: 'JetBrains Mono', monospace; // Data, code, IDs
}

/* Size scale */
--text-xs: 10px;   // Labels
--text-sm: 12px;   // UI text
--text-base: 14px; // Body
--text-lg: 16px;   // Subheadings
--text-xl: 24px;   // Section headers
--text-2xl: 48px;  // Hero headlines
```

### **Spacing System (8px base)**
```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-8: 64px;
}
```

### **Information
```


## License: unknown
https://github.com/Riku115/Riku115/blob/801e8813f86845d8d23b4f7868ce02885faad799/assets/theme.css

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:hover {
    transform: none;
  }
}
```

### **GPU Optimization**
```css
/* Force GPU acceleration for animated elements */
.animated-element {
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

/* Remove will-change after animation */
.animated-element.animation-complete {
  will-change: auto;
}
```

### **Frame Rate Control**
```javascript
// Throttle to 30fps for background effects
let lastFrameTime = 0;
const targetFPS = 30;
const frameInterval = 1000 / targetFPS;

function animate(currentTime) {
  requestAnimationFrame(animate);
  
  const elapsed = currentTime - lastFrameTime;
  if (elapsed < frameInterval) return;
  
  lastFrameTime = currentTime - (elapsed % frameInterval);
  
  // Animation logic here
}
```

### **Canvas Isolation**
```javascript
// Separate canvas for 3D, prevent layout thrashing
const Canvas3D = () => (
  <Canvas
    style={{
      position: 'fixed',
      top: 0,
      left: 0,
      zIndex: 0,
      pointerEvents: 'none'
    }}
    dpr={[1, 2]} // Limit pixel ratio to 2x max
    performance={{ min: 0.5 }} // Throttle to 30fps if needed
  >
    <Scene />
  </Canvas>
);

// 2D UI overlay
const UIOverlay = () => (
  <div style={{ position: 'relative', zIndex: 1 }}>
    {/* All UI components */}
  </div>
);
```

### **Conditional Rendering by Device**
```javascript
const [show3D, setShow3D] = useState(false);

useEffect(() => {
  const shouldShow = 
    window.innerWidth > 1024 && // Desktop only
    !window.matchMedia('(prefers-reduced-motion: reduce)').matches &&
    navigator.hardwareConcurrency > 4; // 4+ CPU cores
  
  setShow3D(shouldShow);
}, []);

return show3D ? <Canvas3D /> : <StaticBackground />;
```

---

## 5️⃣ Required Design Constraints

### **Color Palette (Strict)**
```css
:root {
  /* Base */
  --core-dark: #050505;
  --core-panel: #0a0c10;
  --core-border: rgba(255, 255, 255, 0.08);
  
  /* Accent */
  --cyan-bright: #00f0ff;
  --cyan-dim: #005f66;
  
  /* Semantic */
  --critical: #ff1744;
  --high: #ff9100;
  --medium: #ffea00;
  --success: #00e676;
  
  /* Text */
  --text-primary: #ffffff;
  --text-secondary: #aaaaaa;
  --text-tertiary: #666666;
}
```

### **Motion Timing Standards**
```css
:root {
  /* Easing */
  --ease-military: cubic-bezier(0.4, 0, 0.6, 1);
  --ease-tech: cubic-bezier(0.4, 0, 0.2, 1);
  
  /* Durations */
  --duration-instant: 150ms;
  --duration-quick: 250ms;
  --duration-normal: 400ms;
  --duration-deliberate: 600ms;
  --duration-slow: 800ms;
}

/* Rules */
nothing_faster_than: 150ms;  // Feels instant
nothing_slower_than: 800ms;  // Feels laggy
default_duration: 400ms;      // Balanced
```

### **Animation Density Limits**
```javascript
constraints = {
  maxParticles: 0,              // No particle systems
  maxConcurrentAnimations: 5,   // Prevent jank
  backgroundMotionCount: 3,     // Grid + sweep + neural lines
  glowEffects: "focused elements only",
  pulsingElements: "critical alerts only (<2s cycles)"
}
```

### **Typography System**
```css
:root {
  --font-tech: 'Orbitron', sans-serif;   // Headers, system labels
  --font-ui: 'Inter', sans-serif;        // UI text, paragraphs
  --font-mono: 'JetBrains Mono', monospace; // Data, code, IDs
}

/* Size scale */
--text-xs: 10px;   // Labels
--text-sm: 12px;   // UI text
--text-base: 14px; // Body
--text-lg: 16px;   // Subheadings
--text-xl: 24px;   // Section headers
--text-2xl: 48px;  // Hero headlines
```

### **Spacing System (8px base)**
```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-8: 64px;
}
```

### **Information
```


## License: unknown
https://github.com/Riku115/Riku115/blob/801e8813f86845d8d23b4f7868ce02885faad799/assets/theme.css

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:hover {
    transform: none;
  }
}
```

### **GPU Optimization**
```css
/* Force GPU acceleration for animated elements */
.animated-element {
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

/* Remove will-change after animation */
.animated-element.animation-complete {
  will-change: auto;
}
```

### **Frame Rate Control**
```javascript
// Throttle to 30fps for background effects
let lastFrameTime = 0;
const targetFPS = 30;
const frameInterval = 1000 / targetFPS;

function animate(currentTime) {
  requestAnimationFrame(animate);
  
  const elapsed = currentTime - lastFrameTime;
  if (elapsed < frameInterval) return;
  
  lastFrameTime = currentTime - (elapsed % frameInterval);
  
  // Animation logic here
}
```

### **Canvas Isolation**
```javascript
// Separate canvas for 3D, prevent layout thrashing
const Canvas3D = () => (
  <Canvas
    style={{
      position: 'fixed',
      top: 0,
      left: 0,
      zIndex: 0,
      pointerEvents: 'none'
    }}
    dpr={[1, 2]} // Limit pixel ratio to 2x max
    performance={{ min: 0.5 }} // Throttle to 30fps if needed
  >
    <Scene />
  </Canvas>
);

// 2D UI overlay
const UIOverlay = () => (
  <div style={{ position: 'relative', zIndex: 1 }}>
    {/* All UI components */}
  </div>
);
```

### **Conditional Rendering by Device**
```javascript
const [show3D, setShow3D] = useState(false);

useEffect(() => {
  const shouldShow = 
    window.innerWidth > 1024 && // Desktop only
    !window.matchMedia('(prefers-reduced-motion: reduce)').matches &&
    navigator.hardwareConcurrency > 4; // 4+ CPU cores
  
  setShow3D(shouldShow);
}, []);

return show3D ? <Canvas3D /> : <StaticBackground />;
```

---

## 5️⃣ Required Design Constraints

### **Color Palette (Strict)**
```css
:root {
  /* Base */
  --core-dark: #050505;
  --core-panel: #0a0c10;
  --core-border: rgba(255, 255, 255, 0.08);
  
  /* Accent */
  --cyan-bright: #00f0ff;
  --cyan-dim: #005f66;
  
  /* Semantic */
  --critical: #ff1744;
  --high: #ff9100;
  --medium: #ffea00;
  --success: #00e676;
  
  /* Text */
  --text-primary: #ffffff;
  --text-secondary: #aaaaaa;
  --text-tertiary: #666666;
}
```

### **Motion Timing Standards**
```css
:root {
  /* Easing */
  --ease-military: cubic-bezier(0.4, 0, 0.6, 1);
  --ease-tech: cubic-bezier(0.4, 0, 0.2, 1);
  
  /* Durations */
  --duration-instant: 150ms;
  --duration-quick: 250ms;
  --duration-normal: 400ms;
  --duration-deliberate: 600ms;
  --duration-slow: 800ms;
}

/* Rules */
nothing_faster_than: 150ms;  // Feels instant
nothing_slower_than: 800ms;  // Feels laggy
default_duration: 400ms;      // Balanced
```

### **Animation Density Limits**
```javascript
constraints = {
  maxParticles: 0,              // No particle systems
  maxConcurrentAnimations: 5,   // Prevent jank
  backgroundMotionCount: 3,     // Grid + sweep + neural lines
  glowEffects: "focused elements only",
  pulsingElements: "critical alerts only (<2s cycles)"
}
```

### **Typography System**
```css
:root {
  --font-tech: 'Orbitron', sans-serif;   // Headers, system labels
  --font-ui: 'Inter', sans-serif;        // UI text, paragraphs
  --font-mono: 'JetBrains Mono', monospace; // Data, code, IDs
}

/* Size scale */
--text-xs: 10px;   // Labels
--text-sm: 12px;   // UI text
--text-base: 14px; // Body
--text-lg: 16px;   // Subheadings
--text-xl: 24px;   // Section headers
--text-2xl: 48px;  // Hero headlines
```

### **Spacing System (8px base)**
```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-8: 64px;
}
```

### **Information
```


## License: unknown
https://github.com/Riku115/Riku115/blob/801e8813f86845d8d23b4f7868ce02885faad799/assets/theme.css

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:hover {
    transform: none;
  }
}
```

### **GPU Optimization**
```css
/* Force GPU acceleration for animated elements */
.animated-element {
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

/* Remove will-change after animation */
.animated-element.animation-complete {
  will-change: auto;
}
```

### **Frame Rate Control**
```javascript
// Throttle to 30fps for background effects
let lastFrameTime = 0;
const targetFPS = 30;
const frameInterval = 1000 / targetFPS;

function animate(currentTime) {
  requestAnimationFrame(animate);
  
  const elapsed = currentTime - lastFrameTime;
  if (elapsed < frameInterval) return;
  
  lastFrameTime = currentTime - (elapsed % frameInterval);
  
  // Animation logic here
}
```

### **Canvas Isolation**
```javascript
// Separate canvas for 3D, prevent layout thrashing
const Canvas3D = () => (
  <Canvas
    style={{
      position: 'fixed',
      top: 0,
      left: 0,
      zIndex: 0,
      pointerEvents: 'none'
    }}
    dpr={[1, 2]} // Limit pixel ratio to 2x max
    performance={{ min: 0.5 }} // Throttle to 30fps if needed
  >
    <Scene />
  </Canvas>
);

// 2D UI overlay
const UIOverlay = () => (
  <div style={{ position: 'relative', zIndex: 1 }}>
    {/* All UI components */}
  </div>
);
```

### **Conditional Rendering by Device**
```javascript
const [show3D, setShow3D] = useState(false);

useEffect(() => {
  const shouldShow = 
    window.innerWidth > 1024 && // Desktop only
    !window.matchMedia('(prefers-reduced-motion: reduce)').matches &&
    navigator.hardwareConcurrency > 4; // 4+ CPU cores
  
  setShow3D(shouldShow);
}, []);

return show3D ? <Canvas3D /> : <StaticBackground />;
```

---

## 5️⃣ Required Design Constraints

### **Color Palette (Strict)**
```css
:root {
  /* Base */
  --core-dark: #050505;
  --core-panel: #0a0c10;
  --core-border: rgba(255, 255, 255, 0.08);
  
  /* Accent */
  --cyan-bright: #00f0ff;
  --cyan-dim: #005f66;
  
  /* Semantic */
  --critical: #ff1744;
  --high: #ff9100;
  --medium: #ffea00;
  --success: #00e676;
  
  /* Text */
  --text-primary: #ffffff;
  --text-secondary: #aaaaaa;
  --text-tertiary: #666666;
}
```

### **Motion Timing Standards**
```css
:root {
  /* Easing */
  --ease-military: cubic-bezier(0.4, 0, 0.6, 1);
  --ease-tech: cubic-bezier(0.4, 0, 0.2, 1);
  
  /* Durations */
  --duration-instant: 150ms;
  --duration-quick: 250ms;
  --duration-normal: 400ms;
  --duration-deliberate: 600ms;
  --duration-slow: 800ms;
}

/* Rules */
nothing_faster_than: 150ms;  // Feels instant
nothing_slower_than: 800ms;  // Feels laggy
default_duration: 400ms;      // Balanced
```

### **Animation Density Limits**
```javascript
constraints = {
  maxParticles: 0,              // No particle systems
  maxConcurrentAnimations: 5,   // Prevent jank
  backgroundMotionCount: 3,     // Grid + sweep + neural lines
  glowEffects: "focused elements only",
  pulsingElements: "critical alerts only (<2s cycles)"
}
```

### **Typography System**
```css
:root {
  --font-tech: 'Orbitron', sans-serif;   // Headers, system labels
  --font-ui: 'Inter', sans-serif;        // UI text, paragraphs
  --font-mono: 'JetBrains Mono', monospace; // Data, code, IDs
}

/* Size scale */
--text-xs: 10px;   // Labels
--text-sm: 12px;   // UI text
--text-base: 14px; // Body
--text-lg: 16px;   // Subheadings
--text-xl: 24px;   // Section headers
--text-2xl: 48px;  // Hero headlines
```

### **Spacing System (8px base)**
```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-8: 64px;
}
```

### **Information
```


## License: unknown
https://github.com/Riku115/Riku115/blob/801e8813f86845d8d23b4f7868ce02885faad799/assets/theme.css

```
## 1️⃣ Required Visual & Motion Effects

### **Cursor System**
```javascript
// Custom surveillance reticle cursor
{
  outerRing: "20px hollow circle, 1px stroke",
  centerDot: "2px solid dot",
  behavior: "120ms inertia lag on outer ring, instant center",
  states: {
    default: "base cyan #00f0ff",
    interactive: "28px expansion + pulse",
    critical: "red shift #ff1744"
  }
}
```

### **Scanning Animations**
```css
/* Slow horizontal sweep - 12s cycle */
.radar-sweep {
  width: 200px;
  gradient: "transparent → rgba(0,240,255,0.08) → transparent";
  timing: "cubic-bezier(0.2, 0, 0.2, 1)";
  frequency: "12s infinite";
}

/* Grid pulse overlay */
.grid-pulse {
  pattern: "100px grid squares";
  opacity: "0.03 base, 0.08 peak";
  cycle: "4s staggered";
}
```

### **Page Transitions**
```javascript
// Camera focus metaphor
pageTransition = {
  exit: {
    opacity: [1, 0],
    scale: [1, 1.02],
    filter: "blur(0px) → blur(4px)",
    duration: 400
  },
  enter: {
    opacity: [0, 1],
    scale: [0.98, 1],
    filter: "blur(4px) → blur(0px)",
    duration: 600
  }
}
```

### **Parallax Depth**
```javascript
// 3-layer system only
layers = {
  background: { speed: 0.2, elements: "grid, noise texture" },
  midground: { speed: 0.5, elements: "cards, feeds" },
  foreground: { speed: 1.0, elements: "nav, overlays" }
}
```

### **Background Motion**
```css
/* Neural network lines - diagonal subtle pulse */
.neural-line {
  width: "100%";
  height: "1px";
  angle: "135deg";
  gradient: "transparent → rgba(0,240,255,0.1) → transparent";
  animation: "pulse 4s ease-in-out infinite";
  count: "3-5 lines, staggered delays";
}

/* Static tactical grid */
.tactical-grid {
  background: "repeating-linear-gradient(0deg/90deg, rgba(0,240,255,0.03))";
  cellSize: "100px";
  static: true; // No animation
}
```

### **AI Detection Indicators**
```javascript
// Bounding box draw-in
bbox = {
  entry: "clip-path polygon 0 0 → 100% 100% over 400ms",
  style: "2px solid, corner brackets only (12px)",
  label: "top tag with track ID + confidence",
  hover: "metadata panel slide-down 250ms"
}

// Confidence pulse
confidenceBadge = {
  default: "solid border, no animation",
  uncertain: "<70% → orange + subtle pulse 2s",
  critical: "<50% → red + striped background"
}
```

### **Alert State Motion**
```javascript
// Normal → Alert escalation
alertTransition = {
  phase1: { // Detection lock (0-200ms)
    scale: "1 → 1.02",
    easing: "cubic-bezier(0.4, 0, 1, 1)"
  },
  phase2: { // Border intensify (200-400ms)
    borderColor: "rgba(255,255,255,0.1) → #ff1744",
    boxShadow: "0 → 0 0 20px rgba(255,23,68,0.3)"
  },
  phase3: { // Severity deploy (400-600ms)
    badge: "scale(0) rotate(-180deg) → scale(1) rotate(0)"
  },
  totalDuration: "600ms"
}
```

### **Glow Effects**
```css
/* Minimal, purposeful only */
.focus-glow {
  boxShadow: "0 0 20px rgba(0,240,255,0.3)"; // Active elements
}

.critical-glow {
  boxShadow: "0 0 20px rgba(255,23,68,0.4)"; // Alerts
}

.led-glow {
  boxShadow: "0 0 12px currentColor, inset 0 0 4px #fff"; // Status indicators
}
```

---

## 2️⃣ Required 3D & Depth Elements

### **3D CCTV Camera Model**
```javascript
model = {
  format: ".glb (GLTF binary)",
  triangles: "≤5,000",
  materials: {
    body: "metallic black, roughness 0.4",
    lens: "glass shader, Fresnel reflections",
    led: "emissive red, animated strength"
  },
  animation: {
    rotation: "0.1 rad/s Y-axis auto-rotate",
    parallax: "mouse.x * 0.2, mouse.y * 0.3 (±15° limit)",
    interactive: "click → scanning pulse animation"
  },
  lighting: [
    { type: "ambient", intensity: 0.3 },
    { type: "spot", position: [10,10,10], color: "#00f0ff", intensity: 0.8 }
  ],
  placement: "Hero section only"
}
```

### **Vision Cone Visualization**
```javascript
visionCone = {
  geometry: "ConeGeometry(radius, height: 15, segments: 32)",
  angle: "60° FOV",
  material: {
    color: "#00f0ff",
    opacity: 0.15,
    wireframe: true,
    doubleSided: true
  },
  animation: {
    opacity: "pulse 0.1 → 0.25 over 2s",
    scanLine: "horizontal ring bottom→top every 3s"
  },
  placement: "Live stream page, adjacent to feed"
}
```

### **Spatial Grid (City Map)**
```javascript
cityGrid = {
  base: "GridHelper(size: 100, divisions: 50, color: #00f0ff/0.3, #003337)",
  buildings: {
    count: 20,
    geometry: "BoxGeometry(4, randomHeight, 4)",
    material: "wireframe, color: #00f0ff",
    instanced: true // Single draw call
  },
  markers: {
    cameras: "SphereGeometry(0.3)",
    material: "emissive #ff0030, intensity 2",
    positions: "array of [x, y, z] coordinates"
  },
  camera: {
    controls: "OrbitControls",
    autoRotate: "0.05 rad/s",
    limits: { minDistance: 20, maxDistance: 80 }
  },
  placement: "Dashboard background (optional, not mobile)"
}
```

### **Z-Axis Layered Depth**
```javascript
// CSS transform layers for cards
cardDepth = {
  default: "translateZ(0)",
  hover: "translateZ(20px) rotateX(-2deg)",
  active: "translateZ(30px) scale(1.02)",
  timing: "250ms cubic-bezier(0.4, 0, 0.2, 1)",
  parent: "perspective(1000px) on container"
}
```

### **Interactive Hover Depth**
```css
.detection-card {
  transform: translateZ(0);
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.detection-card:hover {
  transform: translateZ(20px) scale(1.02);
  box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* Parent container */
.card-container {
  perspective: 1000px;
  transform-style: preserve-3d;
}
```

---

## 3️⃣ Required Frontend Tech Stack

### **Core Framework**
```json
{
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "react-router-dom": "^6.20.0"
}
```

### **Build Tool**
```json
{
  "vite": "^5.0.0",
  "@vitejs/plugin-react": "^4.2.1"
}
```

### **Styling**
```json
{
  "approach": "CSS Variables + CSS Modules",
  "rationale": "Full control over dark theme, no Tailwind overhead for this spec"
}
```

### **Animation Libraries**
```json
{
  "framer-motion": "^11.0.0",  // Micro-interactions, page transitions
  "gsap": "^3.12.5",           // Timeline animations, ScrollTrigger
  "gsap/ScrollTrigger": "^3.12.5"
}
```

### **3D Rendering**
```json
{
  "three": "^0.160.0",
  "@react-three/fiber": "^8.15.0",  // React renderer for Three.js
  "@react-three/drei": "^9.92.0",   // Helpers (OrbitControls, useGLTF, PerspectiveCamera)
  "@react-three/postprocessing": "^2.16.0" // Optional: bloom effects
}
```

### **Performance Utilities**
```javascript
// Built-in Web APIs (no packages needed)
{
  requestAnimationFrame: "real-time frame loop",
  IntersectionObserver: "scroll trigger, lazy load",
  ResizeObserver: "responsive canvas sizing"
}
```

### **Type Safety**
```json
{
  "typescript": "^5.3.3",
  "@types/react": "^18.2.45",
  "@types/three": "^0.160.0"
}
```

---

## 4️⃣ Required Performance & UX Controls

### **Lazy Loading Strategy**
```javascript
// 3D model lazy load
const CCTVModel = lazy(() => import('./components/CCTVModel'));

// Intersection-based loading
const ModelWrapper = () => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setShouldLoad(true),
      { threshold: 0.1 }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref}>
      {shouldLoad && <Suspense fallback={<Loader />}><CCTVModel /></Suspense>}
    </div>
  );
};
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Disable 3D transforms */
  .detection-card:hover {
    transform: none;
  }
}
```

### **GPU Optimization**
```css
/* Force GPU acceleration for animated elements */
.animated-element {
  will-change: transform;
  transform: translateZ(0);
  backface-visibility: hidden;
}

/* Remove will-change after animation */
.animated-element.animation-complete {
  will-change: auto;
}
```

### **Frame Rate Control**
```javascript
// Throttle to 30fps for background effects
let lastFrameTime = 0;
const targetFPS = 30;
const frameInterval = 1000 / targetFPS;

function animate(currentTime) {
  requestAnimationFrame(animate);
  
  const elapsed = currentTime - lastFrameTime;
  if (elapsed < frameInterval) return;
  
  lastFrameTime = currentTime - (elapsed % frameInterval);
  
  // Animation logic here
}
```

### **Canvas Isolation**
```javascript
// Separate canvas for 3D, prevent layout thrashing
const Canvas3D = () => (
  <Canvas
    style={{
      position: 'fixed',
      top: 0,
      left: 0,
      zIndex: 0,
      pointerEvents: 'none'
    }}
    dpr={[1, 2]} // Limit pixel ratio to 2x max
    performance={{ min: 0.5 }} // Throttle to 30fps if needed
  >
    <Scene />
  </Canvas>
);

// 2D UI overlay
const UIOverlay = () => (
  <div style={{ position: 'relative', zIndex: 1 }}>
    {/* All UI components */}
  </div>
);
```

### **Conditional Rendering by Device**
```javascript
const [show3D, setShow3D] = useState(false);

useEffect(() => {
  const shouldShow = 
    window.innerWidth > 1024 && // Desktop only
    !window.matchMedia('(prefers-reduced-motion: reduce)').matches &&
    navigator.hardwareConcurrency > 4; // 4+ CPU cores
  
  setShow3D(shouldShow);
}, []);

return show3D ? <Canvas3D /> : <StaticBackground />;
```

---

## 5️⃣ Required Design Constraints

### **Color Palette (Strict)**
```css
:root {
  /* Base */
  --core-dark: #050505;
  --core-panel: #0a0c10;
  --core-border: rgba(255, 255, 255, 0.08);
  
  /* Accent */
  --cyan-bright: #00f0ff;
  --cyan-dim: #005f66;
  
  /* Semantic */
  --critical: #ff1744;
  --high: #ff9100;
  --medium: #ffea00;
  --success: #00e676;
  
  /* Text */
  --text-primary: #ffffff;
  --text-secondary: #aaaaaa;
  --text-tertiary: #666666;
}
```

### **Motion Timing Standards**
```css
:root {
  /* Easing */
  --ease-military: cubic-bezier(0.4, 0, 0.6, 1);
  --ease-tech: cubic-bezier(0.4, 0, 0.2, 1);
  
  /* Durations */
  --duration-instant: 150ms;
  --duration-quick: 250ms;
  --duration-normal: 400ms;
  --duration-deliberate: 600ms;
  --duration-slow: 800ms;
}

/* Rules */
nothing_faster_than: 150ms;  // Feels instant
nothing_slower_than: 800ms;  // Feels laggy
default_duration: 400ms;      // Balanced
```

### **Animation Density Limits**
```javascript
constraints = {
  maxParticles: 0,              // No particle systems
  maxConcurrentAnimations: 5,   // Prevent jank
  backgroundMotionCount: 3,     // Grid + sweep + neural lines
  glowEffects: "focused elements only",
  pulsingElements: "critical alerts only (<2s cycles)"
}
```

### **Typography System**
```css
:root {
  --font-tech: 'Orbitron', sans-serif;   // Headers, system labels
  --font-ui: 'Inter', sans-serif;        // UI text, paragraphs
  --font-mono: 'JetBrains Mono', monospace; // Data, code, IDs
}

/* Size scale */
--text-xs: 10px;   // Labels
--text-sm: 12px;   // UI text
--text-base: 14px; // Body
--text-lg: 16px;   // Subheadings
--text-xl: 24px;   // Section headers
--text-2xl: 48px;  // Hero headlines
```

### **Spacing System (8px base)**
```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-8: 64px;
}
```

### **Information
```

