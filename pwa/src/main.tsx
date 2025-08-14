// React entry + Service Worker registration for Dasher Protect PWA.
//
// 1) Mount App.tsx into #root
// 2) In PROD: register SW (/sw.js). In DEV: unregister any SW to avoid
//    intercepting Vite HMR endpoints.

import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './styles.css'

// ---- 1) Mount the React app ----
const rootEl = document.getElementById('root')
if (!rootEl) {
  throw new Error('Root element #root not found — check index.html')
}

ReactDOM.createRoot(rootEl).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)

// ---- 2) Register/unregister the Service Worker ----
if ('serviceWorker' in navigator) {
  if (import.meta.env.PROD) {
    // PROD: register SW
    window.addEventListener('load', () => {
      navigator.serviceWorker
        .register('/sw.js')
        .then((reg) => {
          console.info('[SW] registered:', reg.scope)
          reg.addEventListener('updatefound', () => {
            const nw = reg.installing
            if (!nw) return
            nw.addEventListener('statechange', () => {
              console.info('[SW] state:', nw.state)
            })
          })
        })
        .catch((err) => {
          console.warn('[SW] registration failed:', err)
        })
    })
  } else {
    // DEV: make sure there is no active SW
    navigator.serviceWorker.getRegistrations?.().then((regs) => {
      regs.forEach((r) => r.unregister())
    })
  }

  // When a new SW takes control
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    console.info('[SW] controller changed (new service worker active)')
  })
}
