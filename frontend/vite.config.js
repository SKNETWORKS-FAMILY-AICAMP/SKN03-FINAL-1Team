import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import dotenv from 'dotenv'
import { resolve } from 'path'

// .env 파일 로드
dotenv.config()

// 현재 작업 디렉토리를 환경 변수로 설정
const PROJECT_ROOT = process.cwd()

export default defineConfig({
  plugins: [vue(), vueDevTools()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // 백엔드 서버 주소 변경
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
  define: {
    'process.env': {
      ...process.env,
      VITE_PROJECT_ROOT: PROJECT_ROOT,
      VITE_APP_CLIENT_ID: process.env.VITE_APP_CLIENT_ID,
    },
  },
})
