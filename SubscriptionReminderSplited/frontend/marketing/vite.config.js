import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    host: 'localhost',  // Change from '0.0.0.0' to 'localhost'
    port: 5173,
    hmr: {
      host: 'localhost',  // Force HMR to use localhost
      protocol: 'ws',     // Use WebSocket protocol
    },
    proxy: {
      '/register': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/token': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/subscriptions': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/users': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
