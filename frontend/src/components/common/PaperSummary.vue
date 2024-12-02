<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.

const route = useRoute()
const paperDoi = route.query.paperDoi || '' // 쿼리 파라미터에서 paperDoi 가져오기
const summary = ref('')
const priorPapers = ref([])

// 논문 요약 정보를 HTML 형식으로 생성하는 함수
const createSummaryHTML = (result) => {
  return `
    <h1>${result.title}</h1>
    <p><strong>Keywords:</strong> ${result.userKeyword}</p>
    <p><strong>Authors:</strong> ${result.authors}</p>
    <p><strong>Publication Year:</strong> ${result.publicationYear}</p>
    <p><strong>Publication Month:</strong> ${result.publicationMonth}</p>
    <p><strong>Generated Keyword:</strong> ${result.generatedKeyword}</p>
    <p><strong>Core Method:</strong> ${result.generatedCoreMethod}</p>
    <p><strong>Technologies:</strong> ${result.generatedTechnologies}</p>
  `
}

// 테스트 데이터 설정 함수
const setTestData = () => {
  summary.value = `
    <h1>테스트 논문 제목</h1>
    <p><strong>Keywords:</strong> 테스트 키워드</p>
    <p><strong>Authors:</strong> 테스트 저자</p>
    <p><strong>Publication Year:</strong> 2023</p>
    <p><strong>Publication Month:</strong> 10</p>
    <p><strong>Generated Keyword:</strong> 테스트 생성 키워드</p>
    <p><strong>Core Method:</strong> 테스트 핵심 방법</p>
    <p><strong>Technologies:</strong> 테스트 기술</p>
  `
  priorPapers.value = [
    { title: '테스트 논문 1', generatedKeyword: '테스트 키워드 1', similarity: 0.9 },
  ]
}

// 논문 세부 정보를 가져오는 함수
const fetchPaperDetails = async () => {
  try {
    const summaryResponse = await axios.post('/papers/summary/', { paperDoi })
    if (summaryResponse.data.resultCode === 201) {
      summary.value = createSummaryHTML(summaryResponse.data.result)
    } else {
      summary.value = 'Error: Invalid response code for summary'
    }

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
    setTestData() // 테스트 데이터 설정
  }
}

// 컴포넌트가 로드되는 순간 POST 및 GET 요청 보내기
onMounted(() => {
  fetchPaperDetails()
})
</script>

<template>
  <div class="paper-summary-container flex-column">
    <div class="paper-summary mt-5 text-start">논문 핵심 요약</div>
    <div v-text="summary"></div>
    <!-- v-html 대신 v-text 사용 -->
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
.paper-summary-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.paper-summary {
  position: relative;
  margin-top: 20px;
  padding: 10px 0;
  font-size: 20px;
  color: white;
}

.paper-summary::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background-color: white;
}
</style>
