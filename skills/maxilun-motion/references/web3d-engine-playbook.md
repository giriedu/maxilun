# Web3D Engine Architecture & Multi-Runtime Playbook

Panduan rekayasa produksi untuk pengalaman 3D, WebGL, dan Canvas 2D performa tinggi di peramban. Mengonsolidasi pola arsitektur dari Three.js, React Three Fiber (R3F), Babylon.js, PlayCanvas, PixiJS, dan WebXR ke dalam standar rekayasa Maxilun.

---

## 1. Anggaran Kinerja 3D Produksi (Hardware Budgets)

Sebelum memulai rendering, tetapkan batas toleransi untuk target 60 FPS pada perangkat seluler dan desktop:

| Metrik Kinerja | Target Desktop Standar | Target Mobile / Low-Power | Tindakan Remediasi Jika Melampaui Batas |
|---|---|---|---|
| **Draw Calls** | $\le 100$ | $\le 50$ | Gunakan `InstancedMesh`, gabungkan geometri statis, atlas tekstur |
| **Triangles / Polygons** | $\le 300\text{k}$ | $\le 80\text{k}$ | Mesh decimation, Level of Detail (LOD), normal map baking |
| **Texture VRAM** | $\le 120\text{MB}$ | $\le 45\text{MB}$ | ORM channel packing, KTX2/Basis Universal, resolusi maks 1024px |
| **Shaders & Lights** | $\le 3$ active shadow lights | 1 directional shadow light | Ganti dynamic shadows dengan contact shadow planes |
| **Device Pixel Ratio (DPR)** | `Math.min(window.devicePixelRatio, 2)` | `Math.min(window.devicePixelRatio, 1.5)` | Cap DPR maksimum untuk mencegah thermal throttling GPU 4K |

---

## 2. Pola Arsitektur Tiga Lapisan (The 3-Layer Separation)

Dilarang keras mencampur logika status aplikasi/DOM ke dalam render loop WebGL:

```
┌────────────────────────────────────────────────────────┐
│  1. DOM UI Layer (HTML, React, CSS, Semantic A11y)     │
│     - Navigasi, tombol aksi, dialog, pembaca layar     │
├────────────────────────────────────────────────────────┤
│  2. Animation & Interaction Layer (GSAP / Motion)      │
│     - Timeline scroll, spring gestures, event bridge   │
├────────────────────────────────────────────────────────┤
│  3. 3D WebGL Engine Layer (Three.js / R3F / Babylon)   │
│     - Canvas WebGL, render loop, GPU scene graph       │
└────────────────────────────────────────────────────────┘
```

**Aturan Siklus Render Non-Allocating (Zero GC Pressure in RAF)**:
- Dilarang membuat objek baru (`new THREE.Vector3()`, `new THREE.Matrix4()`) di dalam fungsi `requestAnimationFrame` atau `useFrame()`.
- Alokasikan variabel penampung (*scratch variables*) satu kali di luar loop untuk mencegah *garbage collector stutter*.

---

## 3. Three.js WebGL Core & Siklus Hidup Memori

### A. Setup Kanvas & Penanganan Kehilangan Konteks (Context Loss)
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

  // Tangani event context loss secara elegan
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

### B. Protokol Pembersihan Sumber Daya GPU (Deep Disposal Pattern)
WebGL tidak membersihkan memori GPU secara otomatis saat elemen DOM dilepas:
```javascript
export function disposeScene(scene, renderer) {
  scene.traverse((object) => {
    if (!object.isMesh) return;

    // Bersihkan geometri
    if (object.geometry) {
      object.geometry.dispose();
    }

    // Bersihkan material dan seluruh peta tekstur
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

Pada ekosistem React, R3F menyediakan abstraksi deklaratif tanpa overhead komputasi tambahan.

### Pola Produksi R3F Canvas:
```tsx
import { Suspense, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Float, OrbitControls, useGLTF, Html, PerformanceMonitor } from '@react-three/drei';
import * as THREE from 'three';

// Scratch variables di luar render loop (Zero GC allocation)
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

        <Suspense fallback={<Html center><span className="text-xs font-mono text-stone-400">MEMUAT MODEL 3D...</span></Html>}>
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
      // Rotasi halus frame-rate independent
      meshRef.current.rotation.y += delta * 0.2;
    }
  });

  return <primitive ref={meshRef} object={scene} scale={1.2} />;
}
```

---

## 5. Multi-Engine Runtime Decision Matrix

| Kebutuhan Proyek | Runtime Direkomendasikan | Alasan & Trade-off |
|---|---|---|
| **E-commerce, Brand Showcase, Landing Page Interaktif** | **Three.js / React Three Fiber** | Ekosistem komunitas terbesar, ukuran bundle terukur (`~150KB` gzip core), integrasi DOM mulus via Drei. |
| **Game Browser Kompleks, Simulasi Fisika Tingkat Lanjut, CAD** | **Babylon.js** | Engine monolitik lengkap, integrasi fisika Havok kelas industri bawaan, material node editor visual. |
| **Aplikasi Web 3D Multi-User, Scene Editor Ringan** | **PlayCanvas** | Arsitektur Entity-Component System (ECS) murni, runtime WebGL ultra-ringan, engine footprint sangat kecil. |
| **Visualisasi Data 2D Berperforma Tinggi, Kartu Interaktif Partikel** | **PixiJS** | Renderer 2D WebGL tercepat, batching otomatis untuk ratusan ribu sprite tanpa overhead matriks 3D. |
| **Pengalaman VR/AR Web Headset (Apple Vision Pro, Meta Quest)** | **A-Frame / WebXR API** | Deklaratif HTML-like untuk WebXR session, spatial tracking dan controller inputs bawaan. |
