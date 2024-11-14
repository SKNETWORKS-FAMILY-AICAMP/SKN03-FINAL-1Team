<script setup>
import { ref } from 'vue'
import SettingIcon from '@/assets/IconBar/SettingIcon.png' // 이미지 파일을 import

const icons = ref([
  { id: 2, name: '아이콘2' },
  { id: 3, name: '아이콘3' },
  { id: 3, src: SettingIcon }, // 이미지 파일을 사용
])
</script>

<template>
  <div class="icon-bar-container">
    <div class="icon-list">
      <div v-for="icon in icons" :key="icon.id" class="icon">
        <!-- 아이콘 이미지를 렌더링 -->
        <img v-if="icon.src" :src="icon.src" alt="Icon" class="icon-image" />
        <!-- 기존 텍스트 아이콘을 대체 -->
        <span v-else>{{ icon.name }}</span>
      </div>
    </div>
    <div class="icon-bar-footer">
      <!-- 푸터 콘텐츠 추가 -->
      <span>Footer Content</span>
    </div>
  </div>
</template>

<style scoped>
.icon-bar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
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
  border-radius: 10px;
  width: 50px; /* 아이콘의 너비 설정 */
  height: 50px; /* 아이콘의 높이 설정 */
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-image {
  max-width: 100%;
  max-height: 100%;
}

.icon-bar-footer {
  padding: 10px;
  background-color: #ffffff;
  border-radius: 10px;
  width: 100%;
  text-align: center;
  margin-top: 10px; /* 아이콘과의 여백 설정 */
}
</style>
