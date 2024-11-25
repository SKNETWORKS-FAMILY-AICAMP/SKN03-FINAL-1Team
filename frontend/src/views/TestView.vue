<script setup>
import { ref } from 'vue'
import axios from 'axios'

const paperDetails = ref('')
const paperDoi = ref('default')
const selectedUrl = ref('http://localhost:8000') // 기본 URL 설정

// 논문 선택 함수
const fetchPaperDetails = async () => {
  try {
    const response = await axios.get(`${selectedUrl.value}/papers/select/`, {
      params: { paperDoi: paperDoi.value },
    })
    paperDetails.value = response.data
  } catch (error) {
    console.error('Failed to fetch paper details:', error)
    paperDetails.value = 'Failed to fetch paper details'
  }
}

// 버튼 클릭 시 논문 선택 함수 호출
const handleFetch = () => {
  fetchPaperDetails()
}
</script>

<template>
  <div>
    <h1>Paper Details</h1>
    <select v-model="selectedUrl">
      <option value="http://localhost:8000">localhost:8000</option>
      <option value="https://api.documento.click">api.documento.click</option>
    </select>
    <input v-model="paperDoi" placeholder="Enter paper DOI" />
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
