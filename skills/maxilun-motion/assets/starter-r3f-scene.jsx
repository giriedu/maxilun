import React, { Suspense, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Float, OrbitControls, useGLTF, Html, PerformanceMonitor } from '@react-three/drei';
import * as THREE from 'three';

// Scratch variable allocated once outside loop to prevent GC allocations
const scratchRotation = new THREE.Euler();

export function StarterR3FExperience({ modelPath = '/models/sample.glb' }) {
  return (
    <div className="relative w-full h-[500px] bg-stone-950 rounded-2xl overflow-hidden border border-stone-800">
      <Canvas
        camera={{ position: [0, 1.8, 3.5], fov: 45 }}
        gl={{ antialias: true, alpha: true, powerPreference: 'high-performance' }}
        dpr={[1, 2]}
      >
        <PerformanceMonitor onDecline={() => console.warn('[R3F] Performance dipped: Scaling down DPR')} />

        <ambientLight intensity={0.6} />
        <directionalLight position={[6, 8, 6]} intensity={1.4} castShadow shadow-mapSize={1024} />

        <Suspense
          fallback={
            <Html center>
              <div className="text-center font-mono text-xs text-stone-400">
                <span className="block mb-2 font-semibold text-stone-200">MEMUAT MODEL 3D</span>
                <span>Menginisialisasi GPU Mesh...</span>
              </div>
            </Html>
          }
        >
          <Float speed={1.8} rotationIntensity={0.4} floatIntensity={0.6}>
            <SceneModel modelPath={modelPath} />
          </Float>
        </Suspense>

        <OrbitControls
          enableZoom={false}
          maxPolarAngle={Math.PI / 2}
          minPolarAngle={Math.PI / 3.5}
          dampingFactor={0.05}
        />
      </Canvas>

      {/* Accessible DOM Overlay */}
      <div className="absolute bottom-4 left-4 right-4 flex items-center justify-between pointer-events-none">
        <span className="font-mono text-xs text-stone-400 bg-stone-900/80 px-2.5 py-1 rounded border border-stone-800">
          Putar dengan drag kursor
        </span>
      </div>
    </div>
  );
}

function SceneModel({ modelPath }) {
  const { scene } = useGLTF(modelPath);
  const groupRef = useRef();

  useFrame((state, delta) => {
    if (groupRef.current) {
      groupRef.current.rotation.y += delta * 0.15;
    }
  });

  return <primitive ref={groupRef} object={scene} scale={1.0} />;
}
