<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.

const papers = ref([])
const route = useRoute()

const fetchPriorPapers = async () => {
  const paperDoi = route.query.paperDoi
  if (!paperDoi) {
    console.error('paperDoi가 쿼리에 존재하지 않습니다.')
    return
  }

  try {
    const response = await axios.get('/papers/priorpapers/', {
      params: {
        paperDoi: paperDoi,
      },
    })
    if (response.data.resultCode === 201 && response.data.result.paperList) {
      papers.value = response.data.result.paperList
    }
  } catch (error) {
    console.error('선행 논문을 가져오는 중 오류 발생:', error)
  }
}

onMounted(() => {
  fetchPriorPapers()
})
</script>

<template>
  <div class="container mt-4">
    <h2>선행 논문 목록</h2>
    <ul class="list-group">
      <li
        v-for="paper in papers"
        :key="paper.paperDoi"
        class="list-group-item d-flex justify-content-between align-items-center"
      >
        <strong>{{ paper.title }}</strong
        ><br />
        <span class="badge bg-secondary">{{ paper.similarity }}</span>
        <p>{{ paper.generatedKeyword }}</p>
      </li>
    </ul>
  </div>
</template>

<style scoped>
/* 추가적인 스타일을 여기에 작성할 수 있습니다 */
</style>
