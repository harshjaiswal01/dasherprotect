/**
 * Minimal API wrapper for Dasher Protect (dev).
 * Reads VITE_API_BASE (default http://localhost:5001).
 * Uses safe text->JSON parsing to avoid "Unexpected end of JSON input".
 */

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5001';

export async function pingHello() {
  const url = `${API_BASE}/v1/hello`;

  const res = await fetch(url, {
    method: 'GET',
    headers: { 'Accept': 'application/json' }
  });

  // Non-2xx -> throw a readable error
  if (!res.ok) {
    const body = await res.text().catch(() => '');
    throw new Error(`HTTP ${res.status} ${res.statusText} — ${body || 'no body'}`);
  }

  // Safe parse: handle empty body without throwing
  const text = await res.text();
  return text ? JSON.parse(text) : {};
}
