import React, { useRef, useEffect, useState } from 'react';
import * as d3 from 'd3';
import PropTypes from 'prop-types';

/**
 * MindTimeline
 * Draggable, interactive timeline of tasks, reflections, successes, failures.
 * Visual markers for streaks. Jump to past/future projections.
 */
const timelineStub = [
  { time: '08:00', type: 'task', label: 'Start Session', status: 'success' },
  { time: '09:00', type: 'reflection', label: 'Reflected on task', status: 'success' },
  { time: '10:00', type: 'task', label: 'Failed Task', status: 'failure' },
  { time: '11:00', type: 'projection', label: 'Future Plan', status: 'pending' },
];

export default function MindTimeline({ events = timelineStub }) {
  const svgRef = useRef();
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    const width = 600, height = 120;
    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height);
    svg.selectAll('*').remove();
    const x = d3.scalePoint()
      .domain(events.map(e => e.time))
      .range([60, width - 60]);
    svg.append('line')
      .attr('x1', 60).attr('x2', width - 60)
      .attr('y1', height / 2).attr('y2', height / 2)
      .attr('stroke', '#6e00ff').attr('stroke-width', 4);
    svg.selectAll('circle')
      .data(events)
      .enter()
      .append('circle')
      .attr('cx', d => x(d.time))
      .attr('cy', height / 2)
      .attr('r', 18)
      .attr('fill', d => d.status === 'success' ? '#00ff6a' : d.status === 'failure' ? '#ff007c' : '#ffb300')
      .attr('stroke', '#fff').attr('stroke-width', 2)
      .on('click', (e, d) => setSelected(d));
    svg.selectAll('text')
      .data(events)
      .enter()
      .append('text')
      .attr('x', d => x(d.time))
      .attr('y', height / 2 + 40)
      .attr('text-anchor', 'middle')
      .attr('fill', '#e0e7ef')
      .attr('font-size', 14)
      .text(d => d.label);
  }, [events]);

  return (
    <div className="w-full h-40 bg-ambient rounded-xl shadow-lg p-4 relative">
      <svg ref={svgRef} className="w-full h-full cursor-pointer" />
      {selected && (
        <div className="absolute top-2 left-2 bg-console text-white p-3 rounded-xl shadow-xl z-10">
          <h3 className="font-display text-base mb-1">{selected.label}</h3>
          <p>Type: {selected.type}</p>
          <p>Status: {selected.status}</p>
          <button className="mt-2 px-2 py-1 bg-timeline rounded" onClick={() => setSelected(null)}>Close</button>
        </div>
      )}
    </div>
  );
}

MindTimeline.propTypes = {
  events: PropTypes.array,
}; 