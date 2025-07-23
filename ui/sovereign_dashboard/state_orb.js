// StateOrb.js — Shows “health” of mind: stress, energy, constitution status
import React from 'react';

export default function StateOrb({ stress = 0.1, energy = 100, constitution = 'OK' }) {
  return (
    <div style={{
      borderRadius: '50%',
      width: 120,
      height: 120,
      background: 'radial-gradient(circle, #aaf 60%, #44a 100%)',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      boxShadow: '0 0 20px #44a',
      color: '#fff',
      fontWeight: 'bold',
      margin: 16
    }}>
      <div>Stress: {stress}</div>
      <div>Energy: {energy}</div>
      <div>Constitution: {constitution}</div>
    </div>
  );
} 