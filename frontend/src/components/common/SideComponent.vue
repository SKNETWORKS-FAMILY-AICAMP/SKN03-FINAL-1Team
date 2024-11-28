<script setup>
import { ref } from 'vue'

import NevigationBar from '@/components/common/NevigationBar.vue'
import BookmarkList from '@/components/common/BookmarkList.vue'

import AccodionButtonImage from '@/assets/accordion-button.png'

const isSidebarOpen = ref(true)

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}
</script>

<template>
  <div class="container m-0 p-0 h-100">
    <div :class="['left-side-content', { collapsed: !isSidebarOpen }]">
      <NevigationBar />
      <BookmarkList v-if="isSidebarOpen" />
      <div class="d-flex">
        <button class="accordion-button" @click="toggleSidebar">
          <img :src="AccodionButtonImage" />
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  height: 100vh;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: row;
}

.left-side-content {
  display: flex;
  flex-direction: row; /* 가로 정렬 */
  background-color: #a04747;
  width: 435px;
  height: 100%;
  color: #ffffff;
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
  box-shadow: 2px 0px 10px 4px #515151; /* 섀도우 속성 추가 */
  margin-right: 20px;
  transition: width 0.3s; /* 애니메이션 효과 */
}

.left-side-content.collapsed {
  width: 80px; /* 접히면 너비 감소 */
}

.accordion-button {
  background-color: transparent;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 20px;
  padding: 10px;
  margin: 10px;
}

.accordion-button {
  padding-left: 11px;
  margin: 0px;
}
</style>
