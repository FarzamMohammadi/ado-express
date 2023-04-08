import { svelte } from '@sveltejs/vite-plugin-svelte';
import { defineConfig } from 'vite';

// https://vitejs.dev/config/
const isProduction = process.env.NODE_ENV === 'production';

export default defineConfig({
  plugins: [svelte()],
  base: isProduction ? '/ado-express/' : '/',
});
