// EthicsGuardian.js — Lights up if loops are about to violate the constitution
import React from 'react';

export default function EthicsGuardian({ violation = false }) {
  return (
    <div style={{
      width: 80,
      height: 80,
      borderRadius: '50%',
      background: violation ? 'radial-gradient(circle, #f44 60%, #a00 100%)' : 'radial-gradient(circle, #4fa 60%, #0a4 100%)',
      boxShadow: violation ? '0 0 30px #f44' : '0 0 20px #4fa',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: '#fff',
      fontWeight: 'bold',
      margin: 16,
      border: violation ? '3px solid #f44' : '3px solid #4fa',
      transition: 'all 0.3s'
    }}>
      {violation ? '⚠️ Constitution Risk' : '✓ Constitution Safe'}
    </div>
  );
} 