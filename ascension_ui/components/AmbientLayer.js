import React, { useRef, useEffect } from 'react';

/**
 * AmbientLayer
 * Subtle animated background: flowing code, neural pulses, matrix-like rain.
 * Reacts to user hover/click.
 */
const codeRainChars = '01ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');

export default function AmbientLayer() {
  const canvasRef = useRef();

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    let width = window.innerWidth;
    let height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
    let columns = Math.floor(width / 20);
    let drops = Array(columns).fill(1);
    let animationId;

    function draw() {
      ctx.fillStyle = 'rgba(15, 23, 42, 0.15)';
      ctx.fillRect(0, 0, width, height);
      ctx.font = '18px Fira Mono, monospace';
      ctx.fillStyle = '#6e00ff';
      for (let i = 0; i < drops.length; i++) {
        const text = codeRainChars[Math.floor(Math.random() * codeRainChars.length)];
        ctx.fillText(text, i * 20, drops[i] * 20);
        if (Math.random() > 0.975) drops[i] = 0;
        drops[i]++;
        if (drops[i] * 20 > height) drops[i] = 0;
      }
      animationId = requestAnimationFrame(draw);
    }
    draw();
    return () => cancelAnimationFrame(animationId);
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed top-0 left-0 w-full h-full z-0 pointer-events-auto"
      style={{ opacity: 0.7 }}
      onMouseMove={e => {
        // Optionally: trigger neural pulse effect
      }}
      onClick={e => {
        // Optionally: trigger code burst
      }}
    />
  );
} 