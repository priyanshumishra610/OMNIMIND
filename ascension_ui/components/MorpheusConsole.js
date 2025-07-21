import React, { useState } from 'react';
import PropTypes from 'prop-types';

/**
 * MorpheusConsole
 * Terminal-style panel with tabs for logs and manual command input.
 * Tabs: Chain-of-thought, Reflection, Intrusion, Ethics.
 */
const TABS = [
  { key: 'cot', label: 'Chain-of-Thought' },
  { key: 'reflection', label: 'Reflection' },
  { key: 'intrusion', label: 'Intrusion' },
  { key: 'ethics', label: 'Ethics' },
];
const logsStub = {
  cot: ['Thinking about: AGI', 'Next step: Simulate...'],
  reflection: ['Reflected: Success on task.'],
  intrusion: ['No intrusion detected.'],
  ethics: ['Dilemma: None.'],
};

export default function MorpheusConsole({ logs = logsStub }) {
  const [tab, setTab] = useState('cot');
  const [input, setInput] = useState('');
  const [history, setHistory] = useState([]);

  const handleCommand = (e) => {
    e.preventDefault();
    setHistory([...history, input]);
    setInput('');
  };

  return (
    <div className="w-full h-64 bg-console rounded-xl shadow-lg flex flex-col">
      <div className="flex border-b border-mesh">
        {TABS.map((t) => (
          <button
            key={t.key}
            className={`flex-1 py-2 font-mono text-sm ${tab === t.key ? 'bg-mesh text-black' : 'bg-console text-white'}`}
            onClick={() => setTab(t.key)}
          >
            {t.label}
          </button>
        ))}
      </div>
      <div className="flex-1 p-3 overflow-y-auto font-mono text-xs text-green-300 bg-black">
        {(logs[tab] || []).map((line, i) => (
          <div key={i}>{line}</div>
        ))}
        {tab === 'cot' && history.map((cmd, i) => (
          <div key={i} className="text-blue-400">$ {cmd}</div>
        ))}
      </div>
      <form onSubmit={handleCommand} className="flex border-t border-mesh">
        <input
          className="flex-1 bg-black text-white px-2 py-1 font-mono outline-none"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type command..."
        />
        <button type="submit" className="px-3 py-1 bg-mesh text-black font-bold">Send</button>
      </form>
    </div>
  );
}

MorpheusConsole.propTypes = {
  logs: PropTypes.object,
}; 