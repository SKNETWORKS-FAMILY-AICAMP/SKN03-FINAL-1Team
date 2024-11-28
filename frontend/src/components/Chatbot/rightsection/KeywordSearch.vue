<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.

const inputPrompt = ref('')
const generatedResults = ref(null)
const loading = ref(false) // 로딩 상태 추가
const errorMessage = ref('') // 에러 메시지 상태 추가
const router = useRouter()

// 키워드 최적화 요청 (POST 요청)
const optimizeKeywords = async () => {
  loading.value = true // 로딩 시작
  errorMessage.value = '' // 기존 에러 메시지 초기화
  try {
    const response = await axios.post('/papers/transformation/', {
      userPrompt: inputPrompt.value,
    })
    generatedResults.value = response.data.result
    console.log('Optimized Results:', generatedResults.value)
  } catch (error) {
    if (error.response && error.response.status === 404) {
      errorMessage.value = '그런건 없어요'
    } else if (error.message && error.message.includes('CORS')) {
      errorMessage.value = 'CORS 오류가 발생했습니다. 서버 설정을 확인해주세요.'
    } else {
      console.error('키워드 최적화에 실패했습니다:', error)
      errorMessage.value = '키워드 최적화에 실패했습니다. 다시 시도해주세요.'
    }
  } finally {
    loading.value = false // 로딩 종료
  }
}

// 메시지 전송 핸들러
const handleOptimization = () => {
  if (inputPrompt.value.trim() !== '') {
    optimizeKeywords()
  } else {
    console.warn('최적화할 프롬프트를 입력해보세요.')
  }
}

// DOI 요청 핸들러 및 페이지 이동
const requestPaperByDoi = async (doi) => {
  try {
    const response = await axios.get(`/papers/select/?paperDoi=${doi}`)
    if (response.data.resultCode === 201) {
      const paperS3Path = response.data.result.paperS3Path
      router.push({
        path: '/paper',
        query: { paperS3Path },
      })
    }
  } catch (error) {
    console.error('논문 세부 정보를 가져오는데 실패했습니다:', error)
    errorMessage.value = '논문 정보를 불러오는 데 실패했습니다. 다시 시도해주세요.'
  }
}
</script>

<template>
  <div class="container mt-5">
    <div class="text-center mb-4">
      <h2 class="fw-bold">논문 키워드 최적화</h2>
      <p class="text-muted">
        원하는 논문의 키워드를 자신만의 언어로 입력하고 최적화된 키워드를 찾아보세요!
      </p>
    </div>

    <!-- Step 1: 키워드 입력 -->
    <div class="input-group mb-4">
      <input
        v-model="inputPrompt"
        type="text"
        class="form-control"
        placeholder="논문 프롬프트를 입력하세요."
        @keyup.enter="handleOptimization"
        :disabled="loading"
      />
      <button class="btn btn-primary" @click="handleOptimization" :disabled="loading">
        최적화
      </button>
    </div>

    <!-- 로딩 스피너 -->
    <div v-if="loading" class="text-center mb-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">로딩 중...</span>
      </div>
    </div>

    <!-- 에러 메시지 표시 -->
    <div v-if="errorMessage" class="alert alert-danger text-center">
      {{ errorMessage }}
    </div>

    <!-- Step 2: 최적화된 키워드 및 논문 표시 -->
    <div v-if="generatedResults" class="results-area mt-5">
      <h3 class="mb-4">최적화된 키워드 및 논문:</h3>
      <div class="mb-4">
        <h4>생성된 프롬프트: {{ generatedResults.generatedPrompt }}</h4>
      </div>
      <div
        v-for="(keywordItem, index) in generatedResults.generatedKeywordList"
        :key="index"
        class="mb-4"
      >
        <h5 class="fw-bold">키워드: {{ keywordItem.generatedKeyword }}</h5>
        <div
          v-for="(paper, paperIndex) in keywordItem.paperList"
          :key="paperIndex"
          class="card mb-3 shadow-sm"
          @click="requestPaperByDoi(paper.paperDoi)"
          style="cursor: pointer"
        >
          <div class="card-body">
            <h6>{{ paper.title }}</h6>
            <p><strong>DOI:</strong> {{ paper.paperDoi }}</p>
            <p><strong>초록:</strong> {{ paper.korAbstract }}</p>
            <p><strong>인용 수:</strong> {{ paper.citation }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.input-group {
  max-width: 600px;
  margin: 0 auto;
}
.results-area .card {
  max-width: 600px;
  margin: 0 auto;
}
</style>
