import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import MainPage from '@/components/MainPage.vue'
import CardSection from '@/components/home/CardSection.vue'
import ChatbotView from '@/views/ChatbotView.vue' // 여기를 수정했습니다.

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    children: [
      {
        path: 'card-section',
        name: 'CardSection',
        component: CardSection,
      },
    ],
  },
  {
    path: '/chatbot',
    name: 'chatbot',
    component: ChatbotView, // 여기를 수정했습니다.
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
