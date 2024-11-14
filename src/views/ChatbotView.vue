<script setup>
import LeftSection from '@/components/Chatbot/LeftSection.vue'
import RightSection from '@/components/Chatbot/RightSection.vue'
</script>

<template>
  <div class="container-fluid d-flex flex-row m-0 p-0">
    <div class="left-section-wrapper p-0">
      <left-section />
    </div>
    <div class="right-section-wrapper d-flex justify-content-center align-items-center p-0 m-0">
      <RightSection />
    </div>
  </div>
</template>

<style scoped>
.container-fluid {
  height: 100vh;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: row;
}

.icon-bar-wrapper {
  display: flex;
  flex: 0 0 80px; /* icon-bar의 너비를 80px로 고정 */
}

.left-section-wrapper {
  flex: 0 0 350px; /* left-section의 너비를 300px로 고정 */
  max-width: 350px;
}

.right-section-wrapper {
  flex-grow: 1; /* 나머지 공간을 차지하도록 설정 */
  display: flex;
  justify-content: center; /* 수평 중앙 정렬 */
  align-items: center; /* 수직 중앙 정렬 */
}
</style>
