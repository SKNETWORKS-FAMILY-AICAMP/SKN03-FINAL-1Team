<script setup>
import { defineProps } from 'vue'

// props 정의
const props = defineProps({
  isSidebarOpen: {
    type: Boolean,
    required: true,
  },
})
</script>

<template>
  <div class="book-mark d-flex flex-column">
    <div class="bookmark-list mt-5 text-start">북마크 리스트</div>
    <div class="content my-2"></div>
  </div>
</template>

<style scoped>
.book-mark {
  flex-grow: 1; /* 남은 공간을 차지하도록 설정 */
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.bookmark-list {
  position: relative;
  margin-top: 20px;
  padding: 10px 0;
  font-size: 20px;
  color: white;
}

.bookmark-list::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background-color: white;
}
</style>
