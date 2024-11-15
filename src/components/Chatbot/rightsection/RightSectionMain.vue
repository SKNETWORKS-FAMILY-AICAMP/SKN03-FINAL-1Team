<script setup>
import { ref } from 'vue'
import ToggleSwitch from './ToggleSwitch.vue'
import ChatPage from './ChatPage.vue'
import PaperSearchPage from './PaperSearchPage.vue'

const isToggled = ref(false) // 토글 상태 저장

const toggleChat = () => {
  isToggled.value = !isToggled.value
}
</script>

<template>
  <div class="right-side-content d-flex flex-column justify-content-between align-items-center p-4">
    <toggle-switch :isToggled="isToggled" @toggleChat="toggleChat" />
    <transition name="slide-fade" mode="out-in">
      <div v-if="!isToggled" class="page">
        <chat-page />
      </div>
      <div v-else class="page">
        <paper-search-page />
      </div>
    </transition>
  </div>
</template>

<style scoped>
.right-side-content {
  background-color: #ffffff;
  width: 100%;
  height: 100%;
  padding: 40px; /* 내부 여백을 크게 추가 */
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 상단과 하단으로 공간 분배 */
  align-items: center; /* 수평 중앙 정렬 */
  max-width: 900px;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition:
    opacity 0.5s,
    transform 0.5s;
}

.slide-fade-enter,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
