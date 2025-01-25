import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Expose le serveur sur toutes les interfaces réseau
    port: 5173,      // Vous pouvez aussi spécifier un autre port si nécessaire
    historyApiFallback: true,
  },
})
