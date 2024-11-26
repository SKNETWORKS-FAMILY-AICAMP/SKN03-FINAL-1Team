<script setup>
import { ref } from 'vue'
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.
import PaperSearchItem from '@/components/Chatbot/rightsection/PaperSearchItem.vue' // 정확한 경로로 수정

const inputText = ref('')
const papers = ref([])

// 논문 데이터 가져오기 (POST 요청)
const fetchPapers = async () => {
  try {
    const response = await axios.post('/papers/search', {
      userKeyword: inputText.value,
    })
    papers.value = response.data.result.paperList
    console.log('Papers:', papers.value)
  } catch (error) {
    console.error('Failed to fetch papers:', error)
  }
}

// 메시지 전송 핸들러
const sendMessage = () => {
  if (inputText.value.trim() !== '') {
    fetchPapers()
  } else {
    console.warn('탐색 키워드를 입력해보아요.')
  }
}
</script>

<template>
  <div class="test-content">
    <div class="input-area d-flex w-100 p-2">
      <input
        v-model="inputText"
        type="text"
        class="form-control chat-input"
        placeholder="탐색 키워드를 입력해보아요."
        @keyup.enter="sendMessage"
      />
      <button class="btn send-button" @click="sendMessage">></button>
    </div>
    <div v-for="(paper, index) in papers" :key="index">
      <PaperSearchItem :paper="paper" class="search-item" />
    </div>
  </div>
</template>

<style scoped>
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
</style>
