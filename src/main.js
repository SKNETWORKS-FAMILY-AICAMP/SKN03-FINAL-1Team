import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './stores'
import 'bootstrap/dist/css/bootstrap.min.css'
import GAuth from 'vue3-google-oauth2'

const app = createApp(App)

const googleOauthClientId = import.meta.env.VITE_GOOGLE_OAUTH_CLIENT_ID

console.log('Google OAuth Client ID:', googleOauthClientId) // 콘솔 로그 추가

app.use(router)
app.use(pinia)
app.use(GAuth, {
  clientId: googleOauthClientId,
  scope: 'profile email',
  prompt: 'consent',
})

app.mount('#app')
