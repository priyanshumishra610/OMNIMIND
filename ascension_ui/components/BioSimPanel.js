import React from 'react';
import PropTypes from 'prop-types';

/**
 * BioSimPanel
 * Displays virtual body stats: energy, fatigue, sleep state.
 * Uses SVG silhouette/blob, animates when agent sleeps.
 */
export default function BioSimPanel({ state = { energy: 0.8, fatigue: 0.2, sleeping: false } }) {
  const { energy, fatigue, sleeping } = state;
  return (
    <div className="w-full h-48 bg-ambient rounded-xl shadow-lg flex flex-col items-center justify-center relative">
      <svg width="120" height="120" viewBox="0 0 120 120">
        <ellipse
          cx="60" cy="60" rx={40 + energy * 10} ry={40 - fatigue * 20}
          fill={sleeping ? 'url(#sleep)' : 'url(#awake)'}
          style={{ filter: sleeping ? 'blur(4px)' : 'drop-shadow(0 0 16px #00ff6a)' }}
        />
        <defs>
          <radialGradient id="awake" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#00ff6a" />
            <stop offset="100%" stopColor="#0f172a" />
          </radialGradient>
          <radialGradient id="sleep" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#6e00ff" />
            <stop offset="100%" stopColor="#0f172a" />
          </radialGradient>
        </defs>
      </svg>
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 text-center">
        <div className="font-mono text-lg">Energy: {(energy * 100).toFixed(0)}%</div>
        <div className="font-mono text-lg">Fatigue: {(fatigue * 100).toFixed(0)}%</div>
        <div className={`font-mono text-lg ${sleeping ? 'text-plasma' : 'text-biosim'}`}>{sleeping ? 'Sleeping...' : 'Awake'}</div>
      </div>
    </div>
  );
}

BioSimPanel.propTypes = {
  state: PropTypes.object,
}; 