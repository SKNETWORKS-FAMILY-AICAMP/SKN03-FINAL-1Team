import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import CardSection from '@/components/home/CardSection.vue'
import KeywordTransformationView from '@/views/MainView.vue'
import PaperDetailView from '@/views/PaperDetailView.vue'
import SignUpView from '@/views/SignUpView.vue' // 회원가입 뷰 임포트 추가
import TestView from '@/views/TestView.vue'
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
    path: '/keyword-transformation',
    name: 'keyword-transformation',
    component: KeywordTransformationView,
  },
  {
    path: '/paper',
    name: 'paper-detail',
    component: PaperDetailView,
  },
  {
    path: '/signup', // 회원가입 경로 추가
    name: 'signup',
    component: SignUpView,
  },
  {
    path: '/test',
    name: 'test',
    component: TestView,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
