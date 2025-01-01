<script setup>
import BookmarkIcon from '@/assets/SideComponent/BookmarkIcon.png'
import UnbookmarkIcon from '@/assets/bookmarksvg.svg'
import { defineProps,ref } from 'vue'
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.

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

})
const updateBookmark = ref(null);

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
      
      console.log("good")
      updateBookmark.value = inverseBookMark
    }
    
    isBookmarkModalVisible.value = false;
  } catch (error) {
    console.error('북마크 처리 중 오류 발생:', error);
  }
};

// 삭제 확인 모달 열기
const openBookmarkModal = (paper) => {
  selectedBookmark.value = paper
  console.log("selectedBookmark : ", selectedBookmark.value)
  if (updateBookmark.value !== null){
    console.log("not null")
    console.log()
    selectedBookmark.value['bookmarked'] = updateBookmark
  }
  isBookmarkModalVisible.value = true
}

// 삭제 확인 모달 닫기
const closeBookmarkModal = () => {
  isBookmarkModalVisible.value = false
}


</script>

<template>
  <div class="d-flex align-items-center justify-content-start">



  <div class="p-4 d-flex flex-column align-items-center" @click="openBookmarkModal(paper)"
    style="width: 100px;">

  
      <img v-if="updateBookmark !== null" :src="updateBookmark ? BookmarkIcon : UnbookmarkIcon" 
                    
                    style="width: 20px; height: 24px; margin-bottom: 10px;"/>
      <img v-else :src="paper.bookmarked ? BookmarkIcon : UnbookmarkIcon" 
                    
      style="width: 20px; height: 24px; margin-bottom: 10px;"/>
      <div 
      >
        <h2 style="color: #a04747;">{{ paper.similarity }}%</h2>
      </div>
    </div>




    <router-link
      :to="{ path: '/papers/detail/', query: { paperDoi: paper.paperDoi } }"
      class="text-start"
      style="text-decoration: none; color: inherit"
    >
      <div>
        <h5 class="text-truncate-1">{{ paper.title }}</h5>
        <p class="my-1 author">
          {{ paper.publication_month }} {{ paper.publication_year }} | {{ paper.authors }}
        </p>
        <p class="no-margin"><span style="color: #902e2e; font-weight: bold;">키워드:</span> {{ paper.Keyword }}</p>
        <p class="no-margin abstract"><span style="color: #902e2e; font-weight: bold;">핵심 방법론:</span> {{ paper.coreMethod }}</p>
      </div>
    </router-link>



<!-- 북마킹 확인 모달 -->
<div
      v-if="isBookmarkModalVisible"
      class="bookmark-overlay"
    >
      <div class="bookmark-content">
        <div v-if="selectedBookmark.bookmarked===true">
          
        <strong class="text-truncate-1"
        style="font-size: 15px;color: black;">{{ selectedBookmark.title }}</strong>
        <br><p style="font-size: 13px; color: black;">논문을 정말로 북마크에서 <span style="font-size: 18px;color:#a04747;font-weight:bold ">삭제</span>
          하시겠습니까?</p>
        

        </div>

        <div v-else>
          
          <strong class="text-truncate-1"
        style="font-size: 15px;color: black;">{{ selectedBookmark.title }}</strong>
        <br><p style="font-size: 13px;color: black;">논문을 정말로 북마크에 <span style="font-size: 18px;color:#a04747;font-weight:bold ">등록</span>
          하시겠습니까?</p>

        </div>
        



        <div class="bookmarkbutton-group">
          <div class="left-content" @click="closeBookmarkModal"
          >
      아니요
    </div>

    <div class="right-content" @click="Bookmarking(keyword, selectedBookmark.paperDoi, selectedBookmark.bookmarked)">
      네
    </div>


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
  -webkit-line-clamp: 1; /* 표시할 최대 줄 수 (여기서는 3줄) */
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

.bookmark-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .bookmark-content {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    width: 300px;
  }
  
.bookmarkbutton-group {
  display: flex;
  justify-content: center;
  margin-top: 15px;
  align-items: center;
  height: 100%;
  border-top: 1px solid #eba2a2;
  
}

.left-content, .right-content {
  flex: 1; /* 콘텐츠 영역 동등 배분 */
  text-align: center; /* 텍스트 가운데 정렬 */
  padding: 3px;
  color: #a04747;
  background-color: #f8f9fa;

}
.left-content:hover, .right-content:hover {

  color: #f8f9fa;
  background-color: #a04747;

}

.left-content {
  border-right: 0.5px solid #eba2a2;
}

.right-content {
  border-left: 0.5px solid #eba2a2;
}

.text-truncate-1 {
    display: -webkit-box; /* Flexbox 사용을 위해 설정 */
    -webkit-line-clamp: 1; /* 표시할 최대 줄 수 */
    -webkit-box-orient: vertical; /* 수직 방향으로 박스 정렬 */
    overflow: hidden; /* 넘치는 내용 숨기기 */
    text-overflow: ellipsis; /* 생략 표시(...) */
    font-weight: bold;
    
  }
</style>
