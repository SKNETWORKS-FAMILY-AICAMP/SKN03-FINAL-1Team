<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/axiosConfig'

const healthStatus = ref('')

// 서버 상태 가져오기
const fetchHealthStatus = async () => {
  try {
    const response = await axios.get('/health', { withCredentials: true })
    healthStatus.value = response.data
  } catch (error) {
    console.error('Failed to fetch health status:', error)
    healthStatus.value = 'Failed to fetch health status'
  }
}

// 컴포넌트가 마운트될 때 서버 상태 가져오기
onMounted(() => {
  fetchHealthStatus()
})
</script>

<template>
  <div>
    <h1>TestView</h1>
    <p>{{ healthStatus }}</p>
  </div>
</template>

<style scoped></style>
