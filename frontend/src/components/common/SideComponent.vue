<script setup>
import { ref } from 'vue'
import { useNavbarStore } from '@/stores/navbarStore'

import NavigationBar from '@/components/common/NavigationBar.vue'
import BookmarkList from '@/components/common/BookmarkList.vue'
import PriorPaperList from '@/components/common/PriorPaperList.vue'
import PaperSummary from '@/components/common/PaperSummary.vue'
import AccordionButtonImage from '@/assets/accordion-button.png'

const isSidebarOpen = ref(false)
const navbarStore = useNavbarStore()

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

const view = 'bookmark'
navbarStore.setSelectedNavItem(view)
</script>

<template>
  <div class="container m-0 p-0 vh-100">
    <div :class="['left-side-content', { collapsed: !isSidebarOpen }]">
      <NavigationBar />
      <BookmarkList v-if="isSidebarOpen && navbarStore.selectedNavItem === 'bookmark'" />
      <PaperSummary v-if="isSidebarOpen && navbarStore.selectedNavItem === 'paper-summary'" />
      <PriorPaperList v-if="isSidebarOpen && navbarStore.selectedNavItem === 'prior-paper-list'" />
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
  display: flex;
}

.left-side-content {
  display: flex;
  background-color: #a04747;
  width: 435px;
  color: #ffffff;
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
  box-shadow: 2px 0px 10px 4px #515151;
  margin-right: 20px;
  transition: width 0.3s ease;
}

.left-side-content.collapsed {
  width: 80px;
  transition: width 0.3s ease;
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
