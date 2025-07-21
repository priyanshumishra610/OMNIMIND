import React, { useRef, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { shaderMaterial } from '@react-three/drei';
import * as THREE from 'three';
import PropTypes from 'prop-types';

/**
 * EmotionPlasma
 * Fluid shader-based orb that reacts to emotion states.
 * Colors and morphing shapes reflect stress, focus, curiosity.
 * Optionally plays heartbeat sound FX (stub).
 */

// Stub: Replace with actual GLSL shader in /public/shaders/plasma.glsl
const vertexShader = `
varying vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}`;
const fragmentShader = `
varying vec2 vUv;
void main() {
  float d = length(vUv - 0.5);
  float intensity = 0.7 - d * 1.2;
  gl_FragColor = vec4(0.43 + intensity, 0.0 + intensity, 1.0 - intensity, 0.85);
}`;

function PlasmaOrb({ emotion = { stress: 0.2, focus: 0.8, curiosity: 0.5 } }) {
  const mesh = useRef();
  useFrame(({ clock }) => {
    if (mesh.current) {
      mesh.current.rotation.y += 0.003 + emotion.stress * 0.01;
      mesh.current.scale.set(1 + emotion.stress * 0.2, 1 + emotion.focus * 0.1, 1 + emotion.curiosity * 0.15);
    }
  });
  return (
    <mesh ref={mesh} position={[0, 0, 0]}>
      <sphereGeometry args={[1.2, 64, 64]} />
      <shaderMaterial attach="material" vertexShader={vertexShader} fragmentShader={fragmentShader} transparent />
    </mesh>
  );
}

PlasmaOrb.propTypes = {
  emotion: PropTypes.object,
};

export default function EmotionPlasma({ emotion }) {
  // Optionally: play heartbeat sound based on emotion.stress (stub)
  useEffect(() => {
    // TODO: Web Audio API for heartbeat FX
  }, [emotion]);
  return (
    <div className="w-full h-full bg-ambient flex items-center justify-center rounded-xl shadow-lg">
      <Canvas camera={{ position: [0, 0, 4], fov: 50 }}>
        <ambientLight intensity={0.8} />
        <pointLight position={[5, 5, 5]} intensity={1.2} />
        <PlasmaOrb emotion={emotion} />
      </Canvas>
    </div>
  );
} 