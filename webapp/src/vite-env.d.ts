/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_DATA_REV?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
