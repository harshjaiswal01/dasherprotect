import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// VITE_API_BASE controls your backend URL (defaults in code to http://localhost:5001)
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true
    // If you want to proxy API in dev instead of using VITE_API_BASE, uncomment:
    // proxy: { '/v1': 'http://localhost:5001', '/healthz': 'http://localhost:5001' }
  },
  build: {
    sourcemap: true, // handy for debugging
    outDir: 'dist',  // default, explicit here for clarity
    emptyOutDir: true
  }
})
