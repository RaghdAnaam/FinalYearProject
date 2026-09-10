import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// https://vite.dev/config/
export default defineConfig({
	plugins: [vue()],
	server: {
		host: true, // Expose to external network
		port: 5173, // Make sure port 5173 is used
		strictPort: true, // Prevent fallback to other ports
	},
});
