<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router' // Vue Router 사용

import IconBarFooter from '@/components/Chatbot/IconBar/IconBarFooter.vue'

import DocumentIcon from '@/assets/IconBar/DocumentIcon.png'
import LogoIcon from '@/assets/logo.png'
import HamburgerIcon from '@/assets/IconBar/HamburgerIcon.png'

const router = useRouter()

const icons = ref([
  { id: 2, src: HamburgerIcon, action: () => router.push('/chatbot') },
  { id: 3, src: DocumentIcon, action: () => router.push('/paper') }, // HomeIcon 클릭 시 메인 화면으로 이동
])
</script>

<template>
  <div class="icon-bar-container">
    <img :src="LogoIcon" alt="Logo" class="logo mb-3" @click="goToHomePage" />
    <div class="icon-list">
      <div
        v-for="icon in icons"
        :key="icon.id"
        class="icon"
        :class="{ 'logo-icon-bg': icon.id === 1 }"
        @click="icon.action && icon.action()"
      >
        <img v-if="icon.src" :src="icon.src" alt="Icon" class="icon-image" />
        <span v-else>{{ icon.name }}</span>
      </div>
      <icon-bar-footer />
    </div>
  </div>
</template>

<style scoped>
.icon-bar-container {
  height: 100vh;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #a04747; /* 배경 색상을 #a04747로 설정 */
  width: 55px;
  box-shadow: 2px 0px 10px 4px #515151; /* 섀도우 속성 추가 */
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
}

.icon-list {
  flex-grow: 1; /* 나머지 공간을 차지하도록 설정 */
  display: flex;
  flex-direction: column;
  align-items: center;
}

.icon {
  margin: 10px 0;
  padding: 8px;
  background-color: #ffffff; /* 아이콘의 배경 색상을 흰색으로 설정 */
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.logo-icon-bg {
  background-color: #a04747; /* LogoIcon의 배경 색상을 빨간색으로 설정 */
}

.icon-image {
  max-width: 100%;
  max-height: 100%;
}
</style>
