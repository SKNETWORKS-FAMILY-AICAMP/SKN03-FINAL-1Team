<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useNavbarStore } from '@/stores/navbarStore'
import DocumentIcon from '@/assets/IconBar/DocumentIcon.png'
import LogoIcon from '@/assets/logo.png'
import HamburgerIcon from '@/assets/IconBar/HamburgerIcon.png'
import SettingIcon from '@/assets/IconBar/SettingIcon.png'
import HomeIcon from '@/assets/IconBar/HomeIcon.png'
import TreeIcon from '@/assets/IconBar/TreeIcon.png'

const navbarStore = useNavbarStore()
const router = useRouter()
const route = useRoute()

const handleIconClick = (view) => {
  if (view === 'home') {
    router.push('/')
  } else {
    navbarStore.setSelectedNavItem(view)
  }
}

const mainIcons = computed(() => {
  const icons = [{ id: 'bookmark', src: HamburgerIcon, view: 'bookmark' }]

  if (route.path === '/paper') {
    icons.push(
      { id: 'summary', src: DocumentIcon, view: 'paper-summary' },
      { id: 'tree', src: TreeIcon, view: 'prior-paper-list' },
    )
  }

  return icons
})

const footerIcons = ref([
  { id: 1, src: DocumentIcon, view: 'footer1' },
  { id: 'home', src: HomeIcon, view: 'home' },
  { id: 3, src: SettingIcon, view: 'settings' },
])

const selectedNavItem = computed(() => navbarStore.selectedNavItem)
</script>

<template>
  <div class="icon-bar-container">
    <img :src="LogoIcon" alt="Logo" class="logo mb-3" @click="handleIconClick('home')" />
    <div class="icon-list">
      <!-- 메인 아이콘들 -->
      <div
        v-for="icon in mainIcons"
        :key="icon.id"
        class="icon"
        :class="{
          'logo-icon-bg': icon.id === 'bookmark',
          'selected-icon-bg': icon.view === selectedNavItem,
        }"
        @click="handleIconClick(icon.view)"
      >
        <img v-if="icon.src" :src="icon.src" alt="Icon" class="icon-image" />
        <span v-else>{{ icon.name }}</span>
      </div>

      <!-- 푸터 아이콘들 -->
      <div class="icon-list justify-content-end">
        <div
          v-for="icon in footerIcons"
          :key="icon.id"
          class="icon"
          :class="{ 'footer-icon-special': icon.id === 1 }"
          @click="handleIconClick(icon.view)"
        >
          <!-- 아이콘 이미지를 렌더링 -->
          <img :src="icon.src" alt="Footer Icon" class="icon-image" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.icon-bar-container {
  height: 100vh;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #a04747; /* 배경 색상을 #a04747로 설정 */
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
  padding: 8px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.logo-icon-bg {
  background-color: #a04747; /* LogoIcon의 배경 색상을 빨간색으로 설정 */
}

.selected-icon-bg {
  background-color: #ffffff; /* 선택된 아이콘의 배경 색상을 흰색으로 설정 */
}

.footer-icon-special {
  background-color: #ffffff; /* id가 1인 아이콘의 배경 색상 설정 */
  border-radius: 50%; /* id가 1인 아이콘을 동그랗게 설정 */
}

.icon-image {
  max-width: 100%;
  max-height: 100%;
}

.logo {
  cursor: pointer;
}

.mb-3 {
  margin-bottom: 1rem;
}
</style>
