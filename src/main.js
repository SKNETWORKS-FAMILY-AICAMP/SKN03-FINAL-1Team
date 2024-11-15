import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './stores' // 기존 store 대신 Pinia 불러오기

import 'bootstrap/dist/css/bootstrap.min.css'

const app = createApp(App)

app.use(router)
app.use(pinia) // Pinia 사용
app.mount('#app')
