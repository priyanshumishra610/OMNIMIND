// tailwind.config.js
module.exports = {
  mode: 'jit',
  darkMode: 'class',
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './styles/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        plasma: '#6e00ff',
        mesh: '#00ffe7',
        timeline: '#ffb300',
        biosim: '#00ff6a',
        console: '#22223b',
        plugin: '#ff007c',
        ambient: '#0f172a',
      },
      fontFamily: {
        mono: ['Fira Mono', 'monospace'],
        display: ['Orbitron', 'sans-serif'],
      },
    },
  },
  plugins: [],
}; 