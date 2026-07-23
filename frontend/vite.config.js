import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/auto-evaluate': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/evaluate': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/evaluations': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
});

