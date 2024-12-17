<script setup>
import { ref,onMounted } from 'vue'
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.
import PaperSearchItem from '@/components/Chatbot/rightsection/PaperSearchItem.vue' // 정확한 경로로 수정

const currentPage = ref(1) // 현재 페이지
const totalPages = ref(0) // 전체 페이지 수
const inputText = ref('')
const papers = ref([])
const loading = ref(false) // 로딩 상태 추가

// 논문 데이터 가져오기 (POST 요청)
const fetchPapers = async (page = currentPage) => {
  loading.value = true // 로딩 시작
  try {
    const response = await axios.post(
      '/papers/search/',
      {
        userKeyword: inputText.value,
      },
    )
    const { paperLists, totalPages: total } = response.data.result.paperTotals
    papers.value = paperLists[page-1]?.paperInfos || [] // 현재 페이지 데이터
    totalPages.value = total
    currentPage.value = page
  } catch (error) {
    console.error('Failed to fetch papers:', error)
  } finally {
    loading.value = false // 로딩 종료
  }
}


/* 페이지 변경 함수 */
const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    fetchPapers(page)
  }
}

/* 컴포넌트 마운트 시 첫 페이지 데이터 가져오기 */
// onMounted(() => {
//   fetchPapers(currentPage.value)
// })
</script>

<template>
  <div class="main-container">
    <div class="test-content">
      <div class="input-area d-flex p-2">
        <input
          v-model="inputText"
          type="text"
          class="form-control chat-input"
          placeholder="탐색 키워드를 입력해보아요."
          @keyup.enter="fetchPapers(1)"
        />
        <button class="btn send-button" @click="fetchPapers(1)" :disabled="loading">></button>
      </div>
      <div v-if="loading" class="d-flex justify-content-center my-3">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">로딩 중...</span>
        </div>
      </div>
      <div v-else>
        <div v-for="(paper, index) in papers" :key="index">
          <PaperSearchItem :paper="paper" class="search-item" />
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
</template>

<style scoped>
.main-container {
  max-height: 80vh; /* 최대 높이 설정 */
  overflow-y: auto; /* 수직 스크롤 추가 */
  display: flex;
  flex-grow: 1;
  align-items: center; /* 수직 가운데 정렬 */
  justify-content: center; /* 수평 가운데 정렬 */
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

.test-content {
  height: 80vh;
}

.search-item:not(:last-child) {
  border-bottom: 1px solid #ccc; /* 구분선 추가 */
  padding-bottom: 10px; /* 구분선과 요소 간의 간격 추가 */
  margin-bottom: 10px; /* 구분선과 요소 간의 간격 추가 */
}
.pagination-controls {
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
</style>
