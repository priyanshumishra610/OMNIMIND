import React, { useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import PropTypes from 'prop-types';

/**
 * PluginChamber
 * 3D rotating cubes/cards for all plugins. Hover: explode into details. Click: reconfigure.
 */
const pluginsStub = [
  { id: 1, name: 'WebSearch', status: 'active', permissions: 'read', lastUsed: 'now' },
  { id: 2, name: 'Wolfram', status: 'idle', permissions: 'compute', lastUsed: '1h ago' },
  { id: 3, name: 'NewsFeed', status: 'active', permissions: 'read', lastUsed: '5m ago' },
];

function PluginCube({ position, plugin, hovered, onPointerOver, onPointerOut, onClick }) {
  const mesh = useRef();
  useFrame(() => {
    if (mesh.current && !hovered) {
      mesh.current.rotation.y += 0.01;
      mesh.current.rotation.x += 0.005;
    }
  });
  return (
    <mesh
      ref={mesh}
      position={position}
      onPointerOver={onPointerOver}
      onPointerOut={onPointerOut}
      onClick={onClick}
      scale={hovered ? [1.4, 1.4, 1.4] : [1, 1, 1]}
    >
      <boxGeometry args={[0.8, 0.8, 0.8]} />
      <meshStandardMaterial color={hovered ? '#ff007c' : '#00ffe7'} />
      {hovered && (
        <Html center className="bg-console text-white p-2 rounded-xl shadow-xl">
          <div className="font-bold">{plugin.name}</div>
          <div>Status: {plugin.status}</div>
          <div>Permissions: {plugin.permissions}</div>
          <div>Last Used: {plugin.lastUsed}</div>
        </Html>
      )}
    </mesh>
  );
}

PluginCube.propTypes = {
  position: PropTypes.array.isRequired,
  plugin: PropTypes.object.isRequired,
  hovered: PropTypes.bool,
  onPointerOver: PropTypes.func,
  onPointerOut: PropTypes.func,
  onClick: PropTypes.func,
};

export default function PluginChamber({ plugins = pluginsStub }) {
  const [hovered, setHovered] = useState(null);
  const [selected, setSelected] = useState(null);
  return (
    <div className="w-full h-64 bg-ambient rounded-xl shadow-lg">
      <Canvas camera={{ position: [0, 0, 6], fov: 60 }}>
        <ambientLight intensity={0.8} />
        <pointLight position={[10, 10, 10]} intensity={1.2} />
        {plugins.map((plugin, i) => (
          <PluginCube
            key={plugin.id}
            position={[Math.cos(i * 2) * 2, Math.sin(i * 2) * 2, 0]}
            plugin={plugin}
            hovered={hovered === plugin.id}
            onPointerOver={() => setHovered(plugin.id)}
            onPointerOut={() => setHovered(null)}
            onClick={() => setSelected(plugin)}
          />
        ))}
      </Canvas>
      {selected && (
        <div className="absolute top-4 right-4 bg-console text-white p-4 rounded-xl shadow-xl z-10">
          <h2 className="font-display text-lg mb-2">{selected.name} Config</h2>
          <p>Status: {selected.status}</p>
          <p>Permissions: {selected.permissions}</p>
          <p>Last Used: {selected.lastUsed}</p>
          <button className="mt-2 px-3 py-1 bg-plugin rounded" onClick={() => setSelected(null)}>Close</button>
        </div>
      )}
    </div>
  );
} 