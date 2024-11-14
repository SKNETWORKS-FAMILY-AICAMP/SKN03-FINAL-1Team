<script setup>
import { ref } from 'vue'

import IconBarFooter from '@/components/Chatbot/IconBar/IconBarFooter.vue'

import LogoIcon from '@/assets/logo.png'
import HamburgerIcon from '@/assets/IconBar/HamburgerIcon.png'
import SettingIcon from '@/assets/IconBar/SettingIcon.png'

const icons = ref([
  { id: 2, src: HamburgerIcon },
  { id: 3, src: SettingIcon }, // 이미지 파일을 사용
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
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  height: 100%; /* 세로로 꽉 차도록 설정 */
  background-color: #a04747; /* 배경 색상을 #a04747로 설정 */
  width: 80px;
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
  padding: 10px;
  background-color: #ffffff; /* 아이콘의 배경 색상을 흰색으로 설정 */
  border-radius: 50%;
  width: 50px; /* 아이콘의 너비 설정 */
  height: 50px; /* 아이콘의 높이 설정 */
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-icon-bg {
  background-color: #a04747; /* LogoIcon의 배경 색상을 빨간색으로 설정 */
}

.icon-image {
  max-width: 100%;
  max-height: 100%;
}
</style>
