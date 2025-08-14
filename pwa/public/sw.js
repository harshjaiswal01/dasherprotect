/* Dasher Protect SW (M0) — safe in dev + offline in prod.
   - Ignores Vite dev endpoints so HMR keeps working
   - Precache minimal shell (best-effort)
   - Network-first for API (/v1, /healthz)
   - Cache-first for static assets
   - Offline navigation fallback to '/'
   - Supports SKIP_WAITING via postMessage
*/

const CACHE_VERSION = 'v1';
const PRECACHE = `precache-${CACHE_VERSION}`;
const RUNTIME = `runtime-${CACHE_VERSION}`;

// Minimal shell to precache (best-effort; missing files won't break install)
const PRECACHE_URLS = [
  '/', // index.html
  '/manifest.webmanifest',
  '/icons/icon-192.png'
];

// ---- Install: best-effort precache (don’t fail if a file is missing) ----
self.addEventListener('install', (event) => {
  event.waitUntil(
    (async () => {
      try {
        const cache = await caches.open(PRECACHE);
        await Promise.all(
          PRECACHE_URLS.map(async (u) => {
            try {
              const res = await fetch(u, { cache: 'no-cache' });
              if (res.ok) await cache.put(u, res.clone());
            } catch {
              // ignore single-file errors (e.g., icon missing in dev)
            }
          })
        );
      } finally {
        self.skipWaiting();
      }
    })()
  );
});

// ---- Activate: clean old caches ----
self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      const names = await caches.keys();
      await Promise.all(
        names
          .filter((n) => ![PRECACHE, RUNTIME].includes(n))
          .map((n) => caches.delete(n))
      );
      await self.clients.claim();
    })()
  );
});

// Helper: should this request be ignored by the SW?
function shouldBypass(req, url) {
  // Only same-origin GET requests
  if (req.method !== 'GET') return true;
  if (url.origin !== self.location.origin) return true;

  // Ignore Vite dev/HMR endpoints and source files
  if (
    url.pathname.startsWith('/@vite') ||
    url.pathname.startsWith('/@react-refresh') ||
    url.pathname.startsWith('/src/')
  ) return true;

  // Avoid Chrome bug when request.cache === 'only-if-cached' and mode !== 'same-origin'
  if (req.cache === 'only-if-cached' && req.mode !== 'same-origin') return true;

  return false;
}

// ---- Fetch: network-first for API; cache-first for static; navigation fallback ----
self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);

  if (shouldBypass(req, url)) return;

  const isAPI =
    url.pathname.startsWith('/v1') ||
    url.pathname.startsWith('/healthz');

  if (isAPI) {
    // Network-first for API
    event.respondWith(
      (async () => {
        try {
          const fresh = await fetch(req);
          const cache = await caches.open(RUNTIME);
          cache.put(req, fresh.clone());
          return fresh;
        } catch {
          const cache = await caches.open(RUNTIME);
          const cached = await cache.match(req);
          return cached || new Response('Offline', { status: 503 });
        }
      })()
    );
    return;
  }

  // For navigation requests, try cache then network, then fallback to '/'
  const isNavigation = req.mode === 'navigate' ||
    (req.headers.get('accept') || '').includes('text/html');

  if (isNavigation) {
    event.respondWith(
      (async () => {
        const cache = await caches.open(PRECACHE);
        const cached = await cache.match('/');
        try {
          const fresh = await fetch(req);
          const rcache = await caches.open(RUNTIME);
          rcache.put(req, fresh.clone());
          return fresh;
        } catch {
          return cached || Response.error();
        }
      })()
    );
    return;
  }

  // Static assets: cache-first
  event.respondWith(
    (async () => {
      const cached = await caches.match(req);
      if (cached) return cached;
      const res = await fetch(req);
      const cache = await caches.open(RUNTIME);
      cache.put(req, res.clone());
      return res;
    })()
  );
});

// ---- Messages: allow immediate activation ----
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
