import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// For GitHub Pages, we inject BASE_PATH from the workflow as '/<repo>/'.
export default defineConfig({
  plugins: [react()],
  base: process.env.BASE_PATH || '/'
})
