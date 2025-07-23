// SwarmVisualizer.js — Animated swarm map
import React from 'react';

const nodes = [
  { id: 1, x: 40, y: 60 },
  { id: 2, x: 80, y: 30 },
  { id: 3, x: 120, y: 90 },
  { id: 4, x: 60, y: 120 },
];

export default function SwarmVisualizer() {
  return (
    <svg width={160} height={160} style={{ background: '#111', borderRadius: 12, margin: 16 }}>
      {nodes.map(node => (
        <circle key={node.id} cx={node.x} cy={node.y} r={14} fill="#4af" stroke="#fff" strokeWidth={2}>
          <animate
            attributeName="r"
            values="14;18;14"
            dur="1.5s"
            repeatCount="indefinite"
          />
        </circle>
      ))}
    </svg>
  );
} 