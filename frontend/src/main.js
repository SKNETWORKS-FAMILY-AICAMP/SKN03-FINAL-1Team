import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './stores'
import 'bootstrap/dist/css/bootstrap.min.css'
import axios from 'axios'

const app = createApp(App)

// Axios를 글로벌로 설정하기
app.config.globalProperties.$http = axios

app.use(router)
app.use(pinia)

app.mount('#app')
