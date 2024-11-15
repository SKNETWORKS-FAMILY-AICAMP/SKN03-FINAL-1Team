<script setup>
import { ref } from 'vue'
import SettingIcon from '@/assets/IconBar/SettingIcon.png' // 이미지 파일을 import
import HomeIcon from '@/assets/IconBar/HomeIcon.png'
import DocumentIcon from '@/assets/IconBar/DocumentIcon.png'

const footerIcons = ref([
  { id: 1, src: DocumentIcon },
  { id: 2, src: HomeIcon },
  { id: 3, src: SettingIcon },
])
</script>

<template>
  <div class="icon-list justify-content-end">
    <div
      v-for="icon in footerIcons"
      :key="icon.id"
      class="icon"
      :class="{ 'footer-icon-special': icon.id === 1 }"
    >
      <!-- 아이콘 이미지를 렌더링 -->
      <img :src="icon.src" alt="Footer Icon" class="icon-image" />
    </div>
  </div>
</template>

<style scoped>
.icon {
  margin: 10px 0;
  padding: 10px;
  background-color: #a04747; /* 아이콘의 배경 색상을 흰색으로 설정 */
  border-radius: 10px; /* 기본적으로 아이콘을 사각형으로 설정 */
  width: 50px; /* 아이콘의 너비 설정 */
  height: 50px; /* 아이콘의 높이 설정 */
  display: flex;
  align-items: center;
  justify-content: center;
}

.footer-icon-special {
  background-color: #ffffff; /* id가 1인 아이콘의 배경 색상 설정 */
  border-radius: 50%; /* id가 1인 아이콘을 동그랗게 설정 */
}

.icon-image {
  max-width: 100%;
  max-height: 100%;
}
</style>
