<script setup>
import LeftSection from '@/components/Chatbot/LeftSection.vue'

import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const paper = ref(null)
const route = useRoute()

onMounted(async () => {
  const paperId = route.params.id
  try {
    const response = await axios.get(`https://api.example.com/papers/${paperId}`)
    paper.value = response.data
  } catch (error) {
    console.error('Error fetching paper details:', error)
  }
})
</script>

<template>
  <div class="paper-detail">
    <left-section />
    <h1>논문 상세 정보</h1>
    <div>
      <p>논문 정보를 불러오는 중...</p>
    </div>
  </div>
</template>

<style scoped>
.paper-detail {
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}

h2 {
  margin-top: 20px;
  font-size: 24px;
}

p {
  margin: 10px 0;
}
</style>
