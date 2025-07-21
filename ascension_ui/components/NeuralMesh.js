import React, { useRef, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Html } from '@react-three/drei';
import * as THREE from 'three';
import PropTypes from 'prop-types';

/**
 * NeuralMesh
 * 3D force-directed node graph visualizing OMNIMIND's memory mesh.
 * Nodes: episodic (blue), semantic (green), procedural (orange).
 * Animated pulses show active thought paths. Click node to zoom and show details.
 */
const NODE_TYPES = {
  episodic: '#3b82f6',
  semantic: '#22d3ee',
  procedural: '#f59e42',
};

const nodesStub = [
  { id: 1, type: 'episodic', position: [0, 0, 0], label: 'E1' },
  { id: 2, type: 'semantic', position: [2, 1, -1], label: 'S1' },
  { id: 3, type: 'procedural', position: [-2, -1, 1], label: 'P1' },
];
const linksStub = [
  { source: 1, target: 2 },
  { source: 2, target: 3 },
];

function Node({ position, color, label, onClick, active }) {
  const mesh = useRef();
  return (
    <mesh position={position} ref={mesh} onClick={onClick}>
      <sphereGeometry args={[0.25, 32, 32]} />
      <meshStandardMaterial color={color} emissive={active ? color : '#222'} emissiveIntensity={active ? 1.5 : 0.2} />
      <Html center style={{ pointerEvents: 'none', fontWeight: 'bold', color: color }}>{label}</Html>
    </mesh>
  );
}

Node.propTypes = {
  position: PropTypes.array.isRequired,
  color: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  onClick: PropTypes.func,
  active: PropTypes.bool,
};

export default function NeuralMesh({ nodes = nodesStub, links = linksStub }) {
  const [activeNode, setActiveNode] = useState(null);
  return (
    <div className="w-full h-full bg-ambient rounded-xl shadow-lg">
      <Canvas camera={{ position: [0, 0, 8], fov: 60 }}>
        <ambientLight intensity={0.7} />
        <pointLight position={[10, 10, 10]} intensity={1.2} />
        {nodes.map((node) => (
          <Node
            key={node.id}
            position={node.position}
            color={NODE_TYPES[node.type]}
            label={node.label}
            onClick={() => setActiveNode(node)}
            active={activeNode && activeNode.id === node.id}
          />
        ))}
        {links.map((link, i) => {
          const source = nodes.find((n) => n.id === link.source);
          const target = nodes.find((n) => n.id === link.target);
          if (!source || !target) return null;
          return (
            <line key={i}>
              <bufferGeometry>
                <bufferAttribute
                  attach="attributes-position"
                  count={2}
                  array={new Float32Array([...source.position, ...target.position])}
                  itemSize={3}
                />
              </bufferGeometry>
              <lineBasicMaterial color="#fff" linewidth={2} />
            </line>
          );
        })}
        <OrbitControls enablePan enableZoom enableRotate />
      </Canvas>
      {activeNode && (
        <div className="absolute top-4 right-4 bg-console text-white p-4 rounded-xl shadow-xl z-10">
          <h2 className="font-display text-lg mb-2">{activeNode.label} Details</h2>
          <p>Type: {activeNode.type}</p>
          <p>Chain-of-thought: ...</p>
          <button className="mt-2 px-3 py-1 bg-mesh rounded" onClick={() => setActiveNode(null)}>Close</button>
        </div>
      )}
    </div>
  );
} 