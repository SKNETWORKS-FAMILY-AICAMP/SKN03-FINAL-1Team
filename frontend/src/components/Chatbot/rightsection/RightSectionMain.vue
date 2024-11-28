<script setup>
import { ref } from 'vue'
import ToggleSwitch from '@/components/common/ToggleSwitch.vue'
import KeywordSearch from './KeywordSearch.vue'
import PaperSearchPage from './PaperSearchPage.vue'

const isToggled = ref(false) // 토글 상태 저장

const toggleChat = () => {
  isToggled.value = !isToggled.value
}
</script>

<template>
  <div class="right-side-content d-flex flex-column align-items-center p-4">
    <toggle-switch :isToggled="isToggled" @toggleChat="toggleChat" />
    <transition name="slide-fade" mode="out-in">
      <div :key="isToggled ? 'paper-search' : 'chat'" v-if="!isToggled" class="page">
        <keyword-search />
      </div>
      <div :key="isToggled ? 'chat' : 'paper-search'" v-else class="page">
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
  align-items: center; /* 수평 중앙 정렬 */
  max-width: 900px;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition:
    opacity 0.5s,
    transform 0.5s;
}
</style>
