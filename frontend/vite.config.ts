import { defineConfig } from "vite";

export default defineConfig({
  build: {
    outDir: "../custom_components/roedertal_anzeiger/frontend",
    emptyOutDir: true,
    lib: {
      entry: "src/main.ts",
      formats: ["es"],
      fileName: () => "panel.js",
    },
  },
});