import react from '@vitejs/plugin-react'
import path from 'path'
import { defineConfig } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
  root: 'src',
  base: '/app/',
  build: {
    outDir: '../Dist',
    assetsDir: 'assetsapp',
    rollupOptions: {
      input: 'src/App.html'
    }

  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  plugins: [react()],
  esbuild: {
    loader: 'jsx',
  },
  optimizeDeps: {
    esbuildOptions: {
      loader: {
        '.js': 'jsx',
      },
    },
  },
})
