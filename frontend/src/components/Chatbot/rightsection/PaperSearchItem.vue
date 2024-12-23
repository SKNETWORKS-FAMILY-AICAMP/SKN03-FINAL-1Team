<script setup>
import BookMarkIcon from '@/assets/BookMarkIcon.png'
import { defineProps,ref, defineEmits } from 'vue'
import BookmarkList  from '@/components/common/BookmarkList.vue' // 정확한 경로로 수정
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.
const bookmarks = ref([])
const isBookmarkModalVisible = ref(false) // 모달창 표시 여부
const selectedBookmark = ref(null) // 선택된 북마크 정보

// props 정의
const props = defineProps({
  paper: {
    type: Object,
    required: true,
  },
  keyword: 
  {
    type: String,
    required: true,
  },
  /**
   * 
   */
  
})




// 북마킹 함수 수정
const Bookmarking = async (userKeyword, paperDoi, bookMark) => {
  try {
    const inverseBookMark = !bookMark;
    const response = await axios.post('/users/bookmarks/', {
      userKeyword,
      paperDoi,
      bookMark: inverseBookMark,
    });

    if (response.data.resultCode === 201) {
      console.log("goog")
    }
    isBookmarkModalVisible.value = false;
  } catch (error) {
    console.error('북마크 처리 중 오류 발생:', error);
  }
};

// 삭제 확인 모달 열기
const openBookmarkModal = (paper) => {
  selectedBookmark.value = paper
  console.log("props.paper : ", props.paper['bookmarked'])
  isBookmarkModalVisible.value = true
}

// 삭제 확인 모달 닫기
const closeBookmarkModal = () => {
  isBookmarkModalVisible.value = false
}


</script>

<template>
  <div class="d-flex align-items-center">
    
    <div class="p-4" @click="openBookmarkModal(paper)">
      <img :src="BookMarkIcon" 
      :class="{ 
    'bookmarked-icon': paper.bookmarked, 
    'bookmark-icon': !paper.bookmarked 
  }"/>
      <div>
        <h2>{{ paper.citation }} Citations</h2>
      </div>
    </div>




    <router-link
      :to="{ path: '/papers/detail/', query: { paperDoi: paper.paperDoi } }"
      class="text-start"
      style="text-decoration: none; color: inherit"
    >
      <div>
        <h5>{{ paper.title }}</h5>
        <p class="my-1 author">
          {{ paper.publication_month }} {{ paper.publication_year }} | {{ paper.authors }}
        </p>
        <p class="no-margin">DOI: {{ paper.paperDoi }}</p>
        <p class="no-margin abstract">Abstract: {{ paper.kor_abstract }}</p>
      </div>
    </router-link>

    <!-- 북마킹킹 확인 모달 -->
<div
      v-if="isBookmarkModalVisible"
      class="modal-overlay"
    >
      <div class="modal-content">
        <div v-if="selectedBookmark.bookmarked===true">
          <h3 class="modal-title">북마크 삭제 확인</h3>
        <p>
          "{{ selectedBookmark?.title }}"  논문을 북마크에서 정말로 삭제하시겠습니까?
        </p>

        </div>

        <div v-else>
          <h3 class="modal-title">북마크 등록 확인</h3>
        <p>
          "{{ selectedBookmark?.title }}" 논문을 북마크에 등록하시겠습니까?
        </p>

        </div>
        



        <div class="button-group">
          <button
            class="confirm-button"
            @click="Bookmarking(keyword, selectedBookmark.paperDoi, selectedBookmark.bookmarked)"
          >
            네
          </button>
          <button
            class="cancel-button"
            @click="closeBookmarkModal"
          >
            아니요
          </button>
        </div>
      </div>
    </div>


  </div>
</template>

<style scoped>
.bookmarked-icon {

  transition: filter 0.3s ease; /* 부드러운 전환 효과 */
  filter: brightness(0) saturate(100%) invert(50%) sepia(100%) saturate(200%) hue-rotate(90deg) brightness(90%) contrast(100%);
}

.bookmarked-icon:hover {
  filter:none;
}

.bookmark-icon {

  transition: filter 0.3s ease; /* 부드러운 전환 효과 */
  filter: none;
}

.bookmark-icon:hover {
  filter:brightness(0) saturate(100%) invert(50%) sepia(100%) saturate(200%) hue-rotate(90deg) brightness(90%) contrast(100%);

}


.no-margin {
  margin: 0;
}
.abstract {
  display: -webkit-box; /* Flexbox 기반 표시 */
  -webkit-line-clamp: 2; /* 표시할 최대 줄 수 (여기서는 3줄) */
  -webkit-box-orient: vertical; /* 세로 방향 정렬 */
  overflow: hidden; /* 넘치는 부분 감춤 */
  text-overflow: ellipsis; /* '...' 표시 */
}

.author {
  display: -webkit-box; /* Flexbox 기반 표시 */
  -webkit-line-clamp: 1; /* 표시할 최대 줄 수 (여기서는 3줄) */
  -webkit-box-orient: vertical; /* 세로 방향 정렬 */
  overflow: hidden; /* 넘치는 부분 감춤 */
  text-overflow: ellipsis; /* '...' 표시 */
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
