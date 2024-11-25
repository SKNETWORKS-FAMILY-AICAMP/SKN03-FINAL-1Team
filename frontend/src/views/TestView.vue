<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const healthStatus = ref('')

const fetchHealthStatus = async () => {
  try {
    const response = await axios.get('https://api.documento.click/health')
    healthStatus.value = response.data
  } catch (error) {
    console.error('Failed to fetch health status:', error)
    healthStatus.value = 'Failed to fetch health status'
  }
}

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
