import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    rollupOptions: {
      input: ['src/App.js', 'src/AuthComponent.js', 'src/PostComponent.js'],
    },
    manifest: true,
  },
  plugins: [svelte()],
})
