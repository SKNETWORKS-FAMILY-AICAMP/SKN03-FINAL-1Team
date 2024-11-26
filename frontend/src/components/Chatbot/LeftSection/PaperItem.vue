<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.
import DragHandleIcon from '@/assets/DragHandleIcon.png'
import BookMarkIcon from '@/assets/BookMarkIcon.png'

const userId = 31525125
const bookmarks = ref([])

// 사용자 북마크 데이터 가져오기
const fetchBookmarks = async () => {
  try {
    const response = await axios.get('/papers/bookmarks/', {
      headers: {
        userToken: userId,
      },
    })
    bookmarks.value = response.data.paperList
    console.log('Bookmarks:', bookmarks.value)
  } catch (error) {
    console.error('Failed to fetch bookmarks:', error)
  }
}

onMounted(() => {
  fetchBookmarks()
})
</script>

<template>
  <div>
    <div
      v-for="(bookmark, index) in bookmarks"
      :key="index"
      class="paper-item d-flex align-items-center my-2"
    >
      <div class="p-3">
        <img :src="DragHandleIcon" />
      </div>
      <div class="text-start flex-grow-1 d-flex flex-column">
        <p>{{ bookmark.title }}</p>
        <p>{{ bookmark.userKeyword }}</p>
      </div>
      <div class="ms-auto p-4">
        <img :src="BookMarkIcon" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.paper-item {
  background: white;
  color: black;
  border-radius: 10px;
  margin: 5px;
  padding: 0px;
  height: 75px;
}
.paper-item p {
  line-height: 0.7;
  margin-top: 5px;
  margin-bottom: 5px;
}
</style>
