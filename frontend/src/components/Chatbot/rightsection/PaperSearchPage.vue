<script setup>
import { ref } from 'vue'

import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.
import PaperSearchItem from '@/components/Chatbot/rightsection/PaperSearchItem.vue' // 정확한 경로로 수정
import LoadingAnimation from '@/components/common/LoadingAnimation.vue'


const LOGIN_URL = process.env.VUE_APP_LOGIN_URL
const currentPage = ref(1) // 현재 페이지
const totalPages = ref(0) // 전체 페이지 수
const inputText = ref('')
const papers = ref([])
const loading = ref(false) // 로딩 상태 추가
const totalPapers = ref([]) // 전체데이터저장
const errorMessage = ref('') // 에러 메시지 저장
const errorTitle = ref('') // 에러 메시지 저장
const showErrorModal = ref(false) // 모달 상태
const showIntroAndSteps = ref(true)
const steps = [
  { id: 1, text: '<br>키워드 변환을 통해<br><span style="color: #902e2e; font-weight: bold;">추출한 키워드</span> 또는 <span style="color: #902e2e; font-weight: bold;">알고 있는 키워드</span>를<br>준비해 주세요.' },
  { id: 2, text: '<br>해당 키워드를 기반으로 <br><span style="color: #902e2e; font-weight: bold;">논문 검색</span>을 수행하세요.' },
  { id: 3, text: '<br>검색된 논문들을 저장하고<br><span style="color: #902e2e; font-weight: bold;">DOCUEMENTO Score</span>를 통해 <br>검색된 키워드와 유사한 논문을 파악하세요.' },
]







// 논문 데이터 가져오기 (POST 요청 - 최초 1회만)
const fetchPapers = async () => {
papers.value = []
loading.value = true // 로딩 시작
showIntroAndSteps.value = false
try {
  const response = await axios.get('/papers/search/', {
  params: {
    userKeyword: inputText.value, // 쿼리 파라미터로 전달
  },
});

  
  const { paperLists: list, totalPages:total, totalSizes:size } = response.data.result.paperTotals
  totalPapers.value = list // 전체 데이터 저장
  totalPages.value = total
  console.log("totalSize: ", size)
  // 첫 페이지 데이터 표시
  goToPage(1)
} catch (error) {
  if (error.response && error.response.data) {
    const { resultCode, message, errorCode } = error.response.data
    errorMessage.value = message
    errorTitle.value = errorCode
    if (resultCode === 400 || resultCode === 404) {
        showErrorModal.value = true // 모달 창 띄우기
      } else if (resultCode === 403) {
        // 인증 실패: 로그인 페이지로 리다이렉트
        showErrorModal.value = true

        // 3초 후 백엔드 로그인 페이지로 이동
        setTimeout(() => {
          window.location.href = LOGIN_URL
        }, 2500)
      }
    else {
      errorMessage.value = '알 수 없는 에러가 발생했습니다.'
      showErrorModal.value = true
    }
  }
} finally {
  loading.value = false // 로딩 종료
}
}

/* 페이지 변경 함수 */
const goToPage = (page) => {

if (page >= 1 && page <= totalPages.value) {
  currentPage.value = page
  papers.value = totalPapers.value[page-1]?.paperInfos || [] // 현재 페이지 데이터
  console.log(papers)
}
}


const closeErrorModal = () => {
  showErrorModal.value = false
  errorMessage.value = ''
  showIntroAndSteps.value = false
  showIntroAndSteps.value = true
}


</script>

<template>


<div class="input-area d-flex p-2 mt-3">
        <input
          v-model="inputText"
          type="text"
          class="form-control chat-input"
          placeholder="탐색 키워드를 입력해보아요."
          @keyup.enter="fetchPapers()"
        />
        <button class="btn send-button" @click="fetchPapers()" >></button>
      </div>


  <div class="main-container">
    <div class="test-content">
      

      <div v-if="showIntroAndSteps" class="intro-text text-center mb-4 ">
          <p class="text-muted">논문 검색이 어려우신가요? <br /></p>
          <p class="text-muted">
            DCOUMENTO와 함께 검색 키워드를 정의하고, <br />
            읽어야 할, 읽을 수 있는 논문을 탐색해보아요!
          </p>

          <div class="steps-container">
        <div class="d-flex justify-content-between mt-5">
          <div
            class="p-3 bg-light rounded  text-center m-2 "
            v-for="step in steps"
            :key="step.id"
            style="flex: 1;"
          >
            <h5>Step {{ step.id }}</h5>
            <p v-html="step.text"></p>
          </div>
        </div>
      </div>


        </div>


      <div v-else>
              <!-- 에러모달  -->
      <div v-if="showErrorModal" class="modal-overlay">
        <div class="modal-content">
          <p class="error-message"
          >{{ errorMessage }}</p>
          <div class="modal-content-button "
          @click="closeErrorModal"
          > 닫기</div>
        </div>
      </div>


      <!-- 로딩  -->
      <div v-if="loading" class="d-flex justify-content-center my-3">
        <LoadingAnimation />
      </div>


      <div v-else>
        <div v-for="(paper, index) in papers" :key="index">
          <PaperSearchItem :paper="paper" :keyword="inputText" class="search-item my-3 py-3" />
        </div>
      
    </div>
    <!-- 페이지네이션 컨트롤 -->
    <div v-if="papers.length > 0" class="pagination-controls">
      <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">
        이전
      </button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">
        다음
      </button>
    </div>


        
</div>



  </div>
  </div>
</template>



<style scoped>
.main-container {
  max-height: 80vh; /* 최대 높이 설정 */
  
  display: flex;
  flex-grow: 1;
  align-items: center; /* 수직 가운데 정렬 */
  justify-content: center; /* 수평 가운데 정렬 */
  margin-top: -15px;
}

.test-content {
  flex-grow: 1;
  margin: auto;
  width: 100%; /* 좌우로 꽉 차게 설정 */
  max-width: 1000px;
}

.input-area {
  border: 1px solid #a04747;
  border-radius: 50px;
  display: flex;
  gap: 10px;
  width: 100%; /* 좌우로 꽉 차게 설정 */
  margin-bottom: 5vh;
}
.chat-input {
  flex-grow: 1; /* 입력 필드가 남는 공간을 차지하도록 설정 */
  padding: 10px;
  border: none;
}

.chat-input:focus {
  border-color: none;
  box-shadow: none;
  outline: none; /* 포커스 시 기본 아웃라인 제거 */
}

.send-button {
  background-color: #a04747;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 50%;
  width: 50px;
  height: 50px;
}

.send-button:hover {
  background-color: #7a3737; /* 어두운 빨간색으로 변경 */
}


.search-item  {
  border-bottom: 1px solid #a04747; /* 구분선 추가 */

  height: 130px !important;
}
.pagination-controls {
  margin-top: 30px;
  display: flex;
  align-items: center;
  gap: 1rem;
  justify-content: center;
}

button {
  background-color: #a04747;
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #7a3737;
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
  background: white;
  padding: 10px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 300px;
  height: 120px;
  display: flex;
  flex-direction: column; /* 수직 방향으로 정렬 */
  justify-content: space-between; /* 위-아래 간격 분배 */
  position: relative; /* 자식 요소의 위치 설정 */
  border: 5px solid #a04747;
}

.error-message {
  position: absolute;
  top: 8px; /* 상단 여백 */
  left: 8px; /* 좌측 여백 */
  margin: 0; /* 기본 여백 제거 */
}

.modal-content-button {
  position: absolute;
  bottom: 8px; /* 하단 여백 */
  right: 8px; /* 우측 여백 */
  background-color: white;
  color: #a04747;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  padding: 5px 10px;
}

.modal-content-button:hover {
  background-color: #a04747;
  color: white;
}
.error-message {
  white-space: pre-line; /* \n을 줄바꿈으로 인식 */
  text-align: left;
}

.intro-text {
  margin-top: 20px;
  
}

.text-muted {
  color : #8A8A8A;
  font-size: 20px;
}

/* steps 관련 스타일 */
.steps-container {
  margin-top: 40px;
  margin: 10px;
}

.bg-light {
  background-color: #f8f9fa ;
  border: 2px solid #a04747;
  border-radius: 20px !important;

}


</style>

