// pages/api/stream.js
// WebSocket bridge to FastAPI for real-time OMNIMIND data

export default function handler(req, res) {
  if (req.method === 'GET') {
    // Stub: In production, upgrade to WebSocket and proxy to FastAPI
    res.status(200).json({ message: 'WebSocket bridge not implemented yet.' });
  } else {
    res.status(405).end();
  }
} 