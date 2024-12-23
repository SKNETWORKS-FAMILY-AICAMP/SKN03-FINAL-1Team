<script setup>
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BookmarkIcon from '@/assets/SideComponent/BookmarkIcon.png'
import warningImage from '@/assets/warning.svg'
const bookmarks = ref([])

const isDeleteModalVisible = ref(false) // 모달창 표시 여부
const selectedBookmark = ref(null) // 선택된 북마크 정보
const router = useRouter()
const warnFlag = ref(false)

const warnBookmark = [
      {
        title: '북마크가 존재하지 않습니다',
        userKeyword: 'DOCUMENTO의 다른 기능들에서 책갈피 표시를 눌러주세요',
        paperDoi: "이 카드는 북마크가 생성된 후 사라집니다!"
      },
      
    ]

const showBookmarks = async () => {
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

const delBookmarks = async (userKeyword, paperDoi) => {
  try {
    const response = await axios.post('/users/bookmarks/',{
      userKeyword,
      paperDoi,
      bookMark: false // 삭제할 북마크 정보를 본문에 포함
    })
    if (response.data.resultCode === 201) {
      bookmarks.value = response.data.result.paperList
      showBookmarks()
    }
    isDeleteModalVisible.value = false
  } catch (error) {
    console.error('북마크 삭제 중 오류 발생:', error)
  }
  
}

// 삭제 확인 모달 열기
const openDeleteModal = (bookmark) => {
  selectedBookmark.value = bookmark
  isDeleteModalVisible.value = true
}

// 삭제 확인 모달 닫기
const closeDeleteModal = () => {
  isDeleteModalVisible.value = false
}


const requestPaperByDoi = async (paperDoi) => {
  router.replace({
        path: '/papers/detail/',
        query: { paperDoi },
      })
}


onMounted(() => {
  showBookmarks()
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
          <div 
          @click="requestPaperByDoi(bookmark.paperDoi)"
                style="cursor: pointer;"
                title="해당 논문 자세히 보기 "
          class="me-3">
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
            <img :src="BookmarkIcon" 
            class="bookmark-icon" 
            @click="openDeleteModal(bookmark)" 
            />
          </div>
          
        </div>
      </li>
    </ul>

<!-- 삭제 확인 모달 -->
<div
      v-if="isDeleteModalVisible"
      class="modal-overlay"
    >
      <div class="modal-content">
        <h3 class="modal-title">삭제 확인</h3>
        <p>
          "{{ selectedBookmark?.title }}" 북마크를 정말로 삭제하시겠습니까?
        </p>
        <div class="button-group">
          <button
            class="confirm-button"
            @click="delBookmarks(selectedBookmark.userKeyword, selectedBookmark.paperDoi)"
          >
            네
          </button>
          <button
            class="cancel-button"
            @click="closeDeleteModal"
          >
            아니요
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>

.bookmark-icon {
  width: 40px;
  transition: filter 0.3s ease; /* 부드러운 전환 효과 */
  filter: brightness(0) saturate(100%) invert(50%) sepia(100%) saturate(200%) hue-rotate(90deg) brightness(90%) contrast(100%);
}

.bookmark-icon:hover {
  filter:none
}



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


.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #a04747;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 400px;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.confirm-button,
.cancel-button {
  background: #902e2e;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.confirm-button:hover,
.cancel-button:hover {
  background: #28a745;
}

</style>
