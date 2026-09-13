/// <reference types="vitest/config" />
import { copyFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

function githubPagesBase(): string {
  if (process.env.VITE_BASE) return process.env.VITE_BASE;
  const repo = process.env.GITHUB_REPOSITORY;
  if (!repo) return "/";
  const name = repo.split("/")[1];
  if (!name || name.endsWith(".github.io")) return "/";
  return `/${name}/`;
}

export default defineConfig({
  base: githubPagesBase(),
  plugins: [
    react(),
    {
      name: "spa-github-pages-404",
      closeBundle() {
        const index = resolve(__dirname, "dist/index.html");
        const dest = resolve(__dirname, "dist/404.html");
        if (existsSync(index)) copyFileSync(index, dest);
      },
    },
  ],
  test: {
    environment: "node",
    include: ["src/**/*.test.ts", "src/**/*.test.tsx"],
  },
});
