<script setup>
import { ref } from 'vue'

import NavigationBar from '@/components/common/NavigationBar.vue'
import BookmarkList from '@/components/common/BookmarkList.vue'

import AccordionButtonImage from '@/assets/accordion-button.png'

const isSidebarOpen = ref(true)

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}
</script>

<template>
  <div class="container m-0 p-0 h-100">
    <div :class="['left-side-content', { collapsed: !isSidebarOpen }]">
      <NavigationBar />
      <BookmarkList v-if="isSidebarOpen" />
      <div class="d-flex">
        <button class="accordion-button" @click="toggleSidebar">
          <img :src="AccordionButtonImage" />
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
  box-shadow: 2px 0px 10px 4px #515151;
  margin-right: 20px;
  transition: width 0.3s;
}

.left-side-content.collapsed {
  width: 80px;
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

.paper-entry {
  margin-top: 10px;
}

.pagination button {
  background-color: #fff;
  border: 1px solid #ccc;
  color: #333;
  padding: 10px 15px;
  margin: 0 5px;
  cursor: pointer;
}

.pagination button.active {
  background-color: #a04747;
  color: white;
}

.accordion-button {
  padding-left: 11px;
  margin: 0px;
}
</style>
