<script setup>
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.
import { ref, onMounted } from 'vue'
import BookmarkIcon from '@/assets/SideComponent/BookmarkIcon.png'
import warningImage from '@/assets/warning.svg'
const bookmarks = ref([])
const warnFlag = ref(false)

const warnBookmark = [
      {
        title: '북마크가 존재하지 않습니다',
        userKeyword: 'DOCUMENTO의 다른 기능들에서 책갈피 표시를 눌러주세요',
        paperDoi: "이 카드는 북마크가 생성된 후 사라집니다!"
      },
      
    ]

const fetchBookmarks = async () => {
  warnFlag.value = false
  
  try {
    const response = await axios.get('/users/bookmarks/')
    if (response.data.resultCode === 200) {
      bookmarks.value = response.data.result.paperList
      console.log("papers: ", bookmarks)
    }
  } catch (error) {
    if (error.response && error.response.data) {
    const { resultCode, message} = error.response.data
    if (resultCode === 404) {
      warnFlag.value = true
      bookmarks.value = warnBookmark

    console.log(message)
    }
    
}
  }
}


onMounted(() => {
  fetchBookmarks()
})
</script>

<template>
  <div class="bookmark-container flex-column">
    <div class="bookmark-list mt-5 text-start">북마크 리스트</div>
    <ul id="bookmark-list" class="list-group text-start">
      <li
        v-for="bookmark in bookmarks"
        :key="bookmark.bookmarkTitle"
        class="list-group-item text-start my-2 rounded-4"
      >
        <div class="d-flex align-items-center">
          <div class="me-3">
            <h5>
              <strong class="fst-italic">{{ bookmark.title }}</strong>
            </h5>
            <p>{{ bookmark.userKeyword }}</p>
            <p>{{ bookmark.paperDoi }}</p>
          </div>

          <div v-if="warnFlag">
            <img :src="warningImage" 
            width=35
            class="warning-image" />
          </div>
          <div v-else>
            <img :src="BookmarkIcon" class="ms-auto" />
          </div>
          
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.bookmark-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 20px 0px 20px 20px;
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

.draggable {
  cursor: grab;
}

.dragging {
  opacity: 0.5;
}
.warning-image {
  filter: brightness(0) saturate(100%) invert(38%) sepia(32%) saturate(1286%) hue-rotate(314deg) brightness(91%) contrast(90%);
}
</style>
