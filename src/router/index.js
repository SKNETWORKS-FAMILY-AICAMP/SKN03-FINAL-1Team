import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import CardSection from '@/components/home/CardSection.vue'
import ChatbotView from '@/views/ChatbotView.vue'
import PaperDetailView from '@/views/PaperDetailView.vue'

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
    component: ChatbotView,
  },
  {
    path: '/paper',
    name: 'paper-detail',
    component: PaperDetailView,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
