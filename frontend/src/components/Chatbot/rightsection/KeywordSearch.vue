<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.

const inputPrompt = ref('')
const generatedResults = ref(null)
const router = useRouter()

// 키워드 최적화 요청 (POST 요청)
const optimizeKeywords = async () => {
  try {
    const response = await axios.post('/papers/transformation/', {
      userPrompt: inputPrompt.value,
    })
    generatedResults.value = response.data.result
    console.log('Optimized Results:', generatedResults.value)
  } catch (error) {
    console.error('Failed to optimize keywords:', error)
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
    console.error('Failed to fetch paper details:', error)
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
      />
      <button class="btn btn-primary" @click="handleOptimization">최적화</button>
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
