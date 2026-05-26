import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  base: "/static/frontend/",
  plugins: [react()],
  build: {
    outDir: "../backend/static_src/frontend",
    emptyOutDir: true,
  },
  server: {
    port: 5173,
  },
});
