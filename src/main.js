import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './stores' // 기존 store 대신 Pinia 불러오기
import 'bootstrap/dist/css/bootstrap.min.css'
import Vue3GoogleOauth from 'vue3-google-oauth2' // 기본 내보내기 사용

const app = createApp(App)

const googleOauthClientId = import.meta.env.VITE_GOOGLE_OAUTH_CLIENT_ID // 환경 변수 가져오기

if (!googleOauthClientId) {
  console.error('Google OAuth Client ID is missing. Please check your .env file.')
} else {
  console.log('Google OAuth Client ID:', googleOauthClientId) // 환경 변수 검증 및 로그

  app.use(router)
  app.use(pinia) // Pinia 사용
  app.use(Vue3GoogleOauth, {
    clientId: googleOauthClientId, // .env 파일에 저장된 클라이언트 ID
    scope: 'profile email https://www.googleapis.com/auth/plus.login',
    prompt: 'consent', // 동의 화면 명시적으로 요청
  })

  app.mount('#app')
}
