<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router' // Vue Router에서 useRoute를 가져옵니다.
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.

const DEFAULT_DOI = '기본 DOI 값' // 기본 DOI 값을 정의합니다.

const papers = ref([])
const route = useRoute() // 현재 라우트 정보를 가져옵니다.

const fetchPriorPapers = async () => {
  try {
    const paperDoi = route.query.paperDoi || DEFAULT_DOI // 기본 DOI 값을 사용합니다.
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
    <button class="btn btn-primary mb-3" @click="fetchPriorPapers">선행 논문 불러오기</button>
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
