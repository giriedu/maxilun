# Web3D Engine Architecture & Multi-Runtime Playbook

Production engineering guide for high-performance 3D, WebGL, and Canvas 2D experiences in the browser. It consolidates architecture patterns from Three.js, React Three Fiber (R3F), Babylon.js, PlayCanvas, PixiJS, and WebXR into Maxilun engineering standards.

---

## 1. Production 3D Performance Budgets (Hardware Budgets)

Before rendering, set tolerance limits for a 60 FPS target on mobile and desktop devices:

| Performance Metric | Standard Desktop Target | Mobile / Low-Power Target | Remediation When Over Budget |
|---|---|---|---|
| **Draw Calls** | $\le 100$ | $\le 50$ | Use `InstancedMesh`, merge static geometry, texture atlases |
| **Triangles / Polygons** | $\le 300\text{k}$ | $\le 80\text{k}$ | Mesh decimation, Level of Detail (LOD), normal map baking |
| **Texture VRAM** | $\le 120\text{MB}$ | $\le 45\text{MB}$ | ORM channel packing, KTX2/Basis Universal, max resolution 1024px |
| **Shaders & Lights** | $\le 3$ active shadow lights | 1 directional shadow light | Replace dynamic shadows with contact shadow planes |
| **Device Pixel Ratio (DPR)** | `Math.min(window.devicePixelRatio, 2)` | `Math.min(window.devicePixelRatio, 1.5)` | Cap the maximum DPR to prevent GPU thermal throttling at 4K |

---

## 2. The 3-Layer Separation Pattern

Never mix application/DOM state logic into the WebGL render loop:

```
┌────────────────────────────────────────────────────────┐
│  1. DOM UI Layer (HTML, React, CSS, Semantic A11y)     │
│     - Navigation, action buttons, dialogs, screen reader │
├────────────────────────────────────────────────────────┤
│  2. Animation & Interaction Layer (GSAP / Motion)      │
│     - Timeline scroll, spring gestures, event bridge   │
├────────────────────────────────────────────────────────┤
│  3. 3D WebGL Engine Layer (Three.js / R3F / Babylon)   │
│     - Canvas WebGL, render loop, GPU scene graph       │
└────────────────────────────────────────────────────────┘
```

**Non-Allocating Render Cycle Rule (Zero GC Pressure in RAF)**:
- Never create new objects (`new THREE.Vector3()`, `new THREE.Matrix4()`) inside `requestAnimationFrame` or `useFrame()`.
- Allocate scratch variables once outside the loop to prevent garbage collector stutter.

---

## 3. Three.js WebGL Core & Memory Lifecycle

### A. Canvas Setup & Context Loss Handling
```javascript
import * as THREE from 'three';

export function createWebGLScene(canvas) {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
  camera.position.set(0, 2, 5);

  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    alpha: true,
    powerPreference: 'high-performance'
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  // Handle the context loss event gracefully
  canvas.addEventListener('webglcontextlost', (e) => {
    e.preventDefault();
    console.warn('[WebGL] Context lost. Pausing render loop.');
    cancelAnimationFrame(animationFrameId);
  }, false);

  canvas.addEventListener('webglcontextrestored', () => {
    console.info('[WebGL] Context restored. Re-initializing scene resources.');
    rebuildSceneResources();
  }, false);

  return { scene, camera, renderer };
}
```

### B. GPU Resource Cleanup Protocol (Deep Disposal Pattern)
WebGL does not free GPU memory automatically when a DOM element is removed:
```javascript
export function disposeScene(scene, renderer) {
  scene.traverse((object) => {
    if (!object.isMesh) return;

    // Dispose geometry
    if (object.geometry) {
      object.geometry.dispose();
    }

    // Dispose materials and every texture map
    if (object.material) {
      const materials = Array.isArray(object.material) ? object.material : [object.material];
      for (const mat of materials) {
        for (const key of Object.keys(mat)) {
          const prop = mat[key];
          if (prop && typeof prop.dispose === 'function') {
            prop.dispose();
          }
        }
        mat.dispose();
      }
    }
  });

  renderer.dispose();
  renderer.forceContextLoss();
}
```

---

## 4. React Three Fiber (R3F) & Drei Patterns

In the React ecosystem, R3F provides a declarative abstraction without extra compute overhead.

### R3F Canvas Production Pattern:
```tsx
import { Suspense, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Float, OrbitControls, useGLTF, Html, PerformanceMonitor } from '@react-three/drei';
import * as THREE from 'three';

// Scratch variables outside the render loop (Zero GC allocation)
const scratchVec = new THREE.Vector3();

export function ProductViewer({ modelUrl }: { modelUrl: string }) {
  return (
    <div className="relative w-full h-[600px] bg-stone-950 rounded-xl overflow-hidden">
      <Canvas
        camera={{ position: [0, 1.5, 4], fov: 45 }}
        gl={{ antialias: true, alpha: true, powerPreference: 'high-performance' }}
        dpr={[1, 2]}
      >
        <PerformanceMonitor onDecline={() => console.warn('DPR reduced due to framerate drop')} />
        <ambientLight intensity={0.7} />
        <directionalLight position={[5, 8, 5]} intensity={1.5} castShadow />

        <Suspense fallback={<Html center><span className="text-xs font-mono text-stone-400">LOADING 3D MODEL...</span></Html>}>
          <Float speed={2} rotationIntensity={0.5} floatIntensity={0.8}>
            <Model meshUrl={modelUrl} />
          </Float>
        </Suspense>

        <OrbitControls enableZoom={false} maxPolarAngle={Math.PI / 2} minPolarAngle={Math.PI / 4} />
      </Canvas>
    </div>
  );
}

function Model({ meshUrl }: { meshUrl: string }) {
  const { scene } = useGLTF(meshUrl);
  const meshRef = useRef<THREE.Group>(null);

  useFrame((state, delta) => {
    if (meshRef.current) {
      // Smooth frame-rate independent rotation
      meshRef.current.rotation.y += delta * 0.2;
    }
  });

  return <primitive ref={meshRef} object={scene} scale={1.2} />;
}
```

---

## 5. Multi-Engine Runtime Decision Matrix

| Project Need | Recommended Runtime | Reason & Trade-off |
|---|---|---|
| **E-commerce, Brand Showcase, Interactive Landing Page** | **Three.js / React Three Fiber** | Largest community ecosystem, measured bundle size (`~150KB` gzip core), smooth DOM integration via Drei. |
| **Complex Browser Games, Advanced Physics Simulation, CAD** | **Babylon.js** | Complete monolithic engine, built-in industrial-grade Havok physics integration, visual node material editor. |
| **Multi-User 3D Web Apps, Lightweight Scene Editor** | **PlayCanvas** | Pure Entity-Component System (ECS) architecture, ultra-light WebGL runtime, very small engine footprint. |
| **High-Performance 2D Data Visualization, Interactive Particle Cards** | **PixiJS** | Fastest 2D WebGL renderer, automatic batching for hundreds of thousands of sprites without 3D matrix overhead. |
| **Web VR/AR Headset Experiences (Apple Vision Pro, Meta Quest)** | **A-Frame / WebXR API** | Declarative HTML-like API for WebXR sessions, built-in spatial tracking and controller inputs. |
