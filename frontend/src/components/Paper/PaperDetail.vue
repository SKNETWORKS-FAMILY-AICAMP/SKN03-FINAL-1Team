<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.

const route = useRoute()
const paperDoi = route.query.paperDoi || '' // 쿼리 파라미터에서 paperDoi 가져오기
const summary = ref('')
const priorPapers = ref([])

// 컴포넌트가 로드될 때 호출되는 함수
const fetchPaperDetails = async () => {
  try {
    // 논문 요약 정보 요청
    const summaryResponse = await axios.post('/papers/summary/', { paperDoi })
    if (summaryResponse.data.resultCode === 201) {
      const result = summaryResponse.data.result
      summary.value = `
        <div>
          <h1>${result.title}</h1>
          <p><strong>Keywords:</strong> ${result.userKeyword}</p>
          <p><strong>Authors:</strong> ${result.authors}</p>
          <p><strong>Publication Year:</strong> ${result.publicationYear}</p>
          <p><strong>Publication Month:</strong> ${result.publicationMonth}</p>
          <p><strong>Generated Keyword:</strong> ${result.generatedKeyword}</p>
          <p><strong>Core Method:</strong> ${result.generatedCoreMethod}</p>
          <p><strong>Technologies:</strong> ${result.generatedTechnologies}</p>
        </div>
      `
    } else {
      summary.value = 'Error: Invalid response code for summary'
    }

    // 선행 논문 정보 요청
    const priorPapersResponse = await axios.get('/papers/priorpapers/', {
      params: { paperDoi: paperDoi, default: '' },
    })
    if (priorPapersResponse.data.resultCode === 201) {
      priorPapers.value = priorPapersResponse.data.result.paperList
    } else {
      console.error('Error: Invalid response code for prior papers')
    }
  } catch (error) {
    console.error('Error fetching paper details:', error)
    summary.value = 'Error fetching paper details' // 오류 발생 시 메시지 설정
  }
}

// 컴포넌트가 로드되는 순간 POST 및 GET 요청 보내기
onMounted(() => {
  fetchPaperDetails()
})
</script>

<template>
  <div>
    <div v-html="summary"></div>
    <div v-if="priorPapers.length > 0">
      <h2>Prior Papers</h2>
      <ul>
        <li v-for="paper in priorPapers" :key="paper.paperDoi">
          <strong>Title:</strong> {{ paper.title }}<br />
          <strong>Generated Keyword:</strong> {{ paper.generatedKeyword }}<br />
          <strong>Similarity:</strong> {{ paper.similarity }}
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
/* 스타일 정의 */
</style>
