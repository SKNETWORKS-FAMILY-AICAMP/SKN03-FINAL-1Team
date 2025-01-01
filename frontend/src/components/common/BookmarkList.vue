<script setup>
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { StarIcon } from '@heroicons/vue/24/solid'; // Heroicons의 북마크 아이콘 가져오기
import { ExclamationTriangleIcon } from '@heroicons/vue/24/solid';
import bookmarkheader from '@/assets/bookmarkheader.png'

import BookmarkIcon from '@/assets/SideComponent/BookmarkIcon.png'


const HOME_URL = process.env.VUE_APP_HOME_REDIRECT_URL

const bookmarks = ref([])

const isDeleteModalVisible = ref(false) // 모달창 표시 여부
const selectedBookmark = ref(null) // 선택된 북마크 정보
const router = useRouter()
const warnFlag = ref(false)



const showBookmarks = async () => {
  warnFlag.value = false
  console.log("showBookmarks")
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
  console.log("???")
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

  //window.location.href = `${HOME_URL}papers/detail/?paperDoi=${paperDoi}`;
  router.push({
        path: '/papers/detail/',
        query: { paperDoi },
      }).then(() => {
        window.location.reload();
      });
}


onMounted(() => {
  showBookmarks()
  console.log("on mount")
})
</script>

<template>
  <div class="bookmark-container flex-column">
    <div class="bookmark-list mt-5 mb-3 text-start">북마크 리스트</div>

    <div v-if="warnFlag" class="d-flex flex-column align-items-center justify-content-center"
    style="flex-grow: 1;">
    <strong> 현재 북마크된 논문이 존재하지 않습니다 <br></strong>

    <strong><br>키워드 최적화 및 논문 검색 과정을 통해 <br> 논문을 북마킹해보세요 :)</strong>
</div>

    <div v-else></div>
    <ul id="bookmark-list" class="list-group text-start overflow-auto summary-detail-container"
    style="margin-right: 5px;" >
      <li
        v-for="bookmark in bookmarks"
        :key="bookmark.bookmarkTitle"
        class="list-group-item text-start mb-3 rounded-4 p-2.5"
        
        >
        <div class="d-flex justify-content-between"
        >
        
      <div 
      class="d-flex align-items-center"
      >
        <img
    :src="bookmarkheader"
    style="width: 12px; height: 12px;"
    />

      </div>




        <div
  class="d-flex flex-column justify-content-center"
  style="max-width: 87%; cursor: pointer;"
  @click="requestPaperByDoi(bookmark.paperDoi)"
  title="해당 논문 자세히 보기"
>
            <strong style="font-weight: 900;" class="text-truncate-1">{{ bookmark.title }}</strong>

            <p class="text-truncate-1" style="font-size:13px">{{ bookmark.userKeyword }}</p>

          </div>


          <div class="d-flex align-items-center"
          @click="openDeleteModal(bookmark)"
          >
            
  <img
    :src="BookmarkIcon"
    style="width: 15px; height: 17px;"
  />
</div>


        </div>
        


        <!-- <h5>
              <strong class="text-truncate-2" >{{ bookmark.title }}</strong>
            </h5>
            <hr />
        <div class="d-flex align-items-center">
          
          <div 
          @click="requestPaperByDoi(bookmark.paperDoi)"
                style="cursor: pointer;"
                title="해당 논문 자세히 보기 "
          class="me-3">
          <p class="text-truncate-2">{{ bookmark.userKeyword }}</p>
            <div v-if="warnFlag">
              
            <p class="text-truncate-2">{{ bookmark.paperDoi }}</p>
            </div>

            <div v-else>

              <p class="text-truncate-1">{{ bookmark.paperDoi }}</p>
            </div>
            




          </div>


          <div v-if="warnFlag" >
            <ExclamationTriangleIcon 
  class="warn-icon"  
/>
          </div>
          <div v-else>
            <StarIcon 
  class="bookmark-icon" 
  @click="openDeleteModal(bookmark)" 
/>

          </div>
          
        </div> -->
      </li>



      
    </ul>

<!-- 삭제 확인 모달 -->
<div
      v-if="isDeleteModalVisible"
      class="bookmark-overlay"
    >
      <div class="bookmark-content">
        <strong class="text-truncate-1"
        style="font-size: 15px; color: black;">{{ selectedBookmark.title }}</strong>
        <br><p style="font-size: 13px; color: black;">논문을 정말로 북마크에서 <span style="font-size: 18px;color:#a04747;font-weight:bold ">삭제</span>
          하시겠습니까?</p>


        <div class="bookmarkbutton-group">
          <div class="left-content" @click="closeDeleteModal"
          >
      아니요
    </div>
    <div class="right-content" @click="delBookmarks(selectedBookmark.userKeyword, selectedBookmark.paperDoi, selectedBookmark.bookmarked)">
      네 
    </div>
        </div>
      </div>
    </div>

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
    padding: 10px 10px;
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
  
  .text-truncate-2 {
    display: -webkit-box; /* Flexbox 사용을 위해 설정 */
    -webkit-line-clamp: 2; /* 표시할 최대 줄 수 */
    -webkit-box-orient: vertical; /* 수직 방향으로 박스 정렬 */
    overflow: hidden; /* 넘치는 내용 숨기기 */
    text-overflow: ellipsis; /* 생략 표시(...) */
  }
  .text-truncate-1 {
    display: -webkit-box; /* Flexbox 사용을 위해 설정 */
    -webkit-line-clamp: 1; /* 표시할 최대 줄 수 */
    -webkit-box-orient: vertical; /* 수직 방향으로 박스 정렬 */
    overflow: hidden; /* 넘치는 내용 숨기기 */
    text-overflow: ellipsis; /* 생략 표시(...) */
    margin-top: 1px;
    margin-bottom: 1px;
  }


.bookmark-icon {
  width: 30px;
  transition: fill 0.3s ease; /* 부드러운 전환 효과 */
  fill: #ffca1a;
}

.bookmark-icon:hover {
fill: #ffd94d;
}

hr {
    border: 2px solid #a04747 !important;
    margin: 10px 0;
  }

  .warn-icon {
    width: 30px;
    transition: fill 0.3s ease; /* 부드러운 전환 효과 */
    fill: #a04747;
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
  
  border: 2px solid #902e2e !important;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 400px !important;
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


.summary-detail-container::-webkit-scrollbar {
  width: 8px; /* 스크롤 바의 너비 */
}

.summary-detail-container::-webkit-scrollbar-thumb {
  background-color: #da7e7e; /* 스크롤 바의 색상 (부트스트랩 기본색) */
  border-radius: 4px; /* 스크롤 바의 모서리 둥글기 */
}

.summary-detail-container::-webkit-scrollbar-thumb:hover {
  background-color: #8a9cce; /* 스크롤 바 호버 시 색상 */
}

.summary-detail-container::-webkit-scrollbar-track {
  background-color: #f8f9fa; /* 스크롤 바 트랙의 배경색 */
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

</style>