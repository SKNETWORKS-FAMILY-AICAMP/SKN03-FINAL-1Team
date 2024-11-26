<script setup>
import { ref } from 'vue'
import axios from 'axios'

const paperDetails = ref('')
const paperDoi = ref('default')
const postData = ref('') // POST 요청에 사용할 데이터
const selectedUrl = ref('https://localhost:8000') // 기본 URL 설정
const selectedApi = ref('/papers/select') // 기본 API 엔드포인트 설정

// 논문 선택 함수 (GET 요청)
const fetchPaperDetails = async () => {
  try {
    const response = await axios.get(`${selectedUrl.value}${selectedApi.value}/`, {
      params: { paperDoi: paperDoi.value },
    })
    paperDetails.value = response.data
  } catch (error) {
    console.error('Failed to fetch paper details:', error)
    paperDetails.value = 'Failed to fetch paper details'
  }
}

// 논문 검색 함수 (POST 요청)
const searchPapers = async () => {
  try {
    const response = await axios.post(`${selectedUrl.value}${selectedApi.value}/`, {
      userKeyword: postData.value,
    })
    paperDetails.value = response.data
  } catch (error) {
    console.error('Failed to search papers:', error)
    paperDetails.value = 'Failed to search papers'
  }
}

// 버튼 클릭 시 함수 호출
const handleFetch = () => {
  if (selectedApi.value === '/papers/select' || selectedApi.value === '/health') {
    fetchPaperDetails()
  } else if (selectedApi.value === '/papers/search') {
    searchPapers()
  }
}
</script>

<template>
  <div>
    <h1>Paper Details</h1>
    <div>
      <label for="url-select">Select Server URL:</label>
      <select id="url-select" v-model="selectedUrl">
        <option value="http://localhost:8000">localhost:8000</option>
        <option value="https://api.documento.click">api.documento.click</option>
      </select>
    </div>
    <div>
      <label for="api-select">Select API Endpoint:</label>
      <select id="api-select" v-model="selectedApi">
        <option value="/papers/select">/papers/select</option>
        <option value="/papers/search">/papers/search</option>
        <option value="/health">/health</option>
      </select>
    </div>
    <input
      v-model="paperDoi"
      v-if="selectedApi === '/papers/select'"
      placeholder="Enter paper DOI"
    />
    <input
      v-model="postData"
      v-if="selectedApi === '/papers/search'"
      placeholder="Enter search keyword"
    />
    <input v-model="postData" v-if="selectedApi === '/health'" placeholder="Enter health check" />
    <button @click="handleFetch">Fetch Paper Details</button>
    <div>
      <h2>Paper Details:</h2>
      <pre>{{ paperDetails }}</pre>
    </div>
  </div>
</template>

<style scoped>
/* 스타일을 추가할 수 있습니다 */
</style>
