<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.

const router = useRouter()

const inputPrompt = ref('')
const generatedResults = ref(null)
const loading = ref(false) // 로딩 상태 추가
const errorMessage = ref('') // 에러 메시지 상태 추가

const showIntroAndSteps = ref(true)

const steps = [
  { id: 1, text: '키워드 변환을 통해 내가 원하는 논문 검색에 필요한 키워드를 추출하세요.' },
  { id: 2, text: '해당 키워드를 기반으로 논문을 검색하세요.' },
  { id: 3, text: '검색된 논문들을 저장하고 논문 파악을 통해 논문의 난이도를 파악하세요.' },
]

// 키워드 최적화 요청 (POST 요청)
const optimizeKeywords = async () => {
  showIntroAndSteps.value = false
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
        path: '/paper/select',
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
  <div class="main-container">
    <div class="test-content">
      <div class="input-area d-flex w-100 p-2">
        <input
          v-model="inputPrompt"
          type="text"
          class="form-control chat-input"
          placeholder="원하는 논문의 내용을 자신만의 언어로 표현해보세요."
          @keyup.enter="handleOptimization"
          :disabled="loading"
        />
        <button class="btn send-button" @click="handleOptimization" :disabled="loading">></button>
      </div>

      <div v-if="loading" class="d-flex justify-content-center my-3">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">로딩 중...</span>
        </div>
      </div>

      <div v-else>
        <div v-if="errorMessage" class="alert alert-danger text-center">
          {{ errorMessage }}
        </div>

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

        <div v-if="showIntroAndSteps" class="intro-text text-center mb-4">
          <p class="text-muted">논문 검색이 어려우신가요? <br /></p>
          <p class="text-muted">
            도큐멘토와 함께 검색 키워드를 정의하고, <br />
            읽어야 할, 읽을 수 있는 논문을 탐색해보아요!
          </p>
        </div>
      </div>
      <div v-if="showIntroAndSteps" class="steps-container">
        <div class="d-flex justify-content-between mt-5">
          <div
            class="p-3 bg-light rounded shadow text-center m-2"
            v-for="step in steps"
            :key="step.id"
            style="flex: 1"
          >
            <h5>Step {{ step.id }}</h5>
            <p>{{ step.text }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.main-container {
  /* 필요한 스타일을 여기에 추가하세요 */
}

.input-area {
  border: 1px solid #a04747;
  border-radius: 50px;
  display: flex;
  gap: 10px;
  width: 100%; /* 좌우로 꽉 차게 설정 */
  margin-bottom: 5vh;
}

.chat-input {
  flex-grow: 1; /* 입력 필드가 남는 공간을 차지하도록 설정 */
  padding: 10px;
  border: none;
}

.chat-input:focus {
  border-color: none;
  box-shadow: none;
  outline: none; /* 포커스 시 기본 아웃라인 제거 */
}

.send-button {
  background-color: #a04747;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 50%;
  width: 50px;
  height: 50px;
}

.send-button:hover {
  background-color: #7a3737; /* 어두운 빨간색으로 변경 */
}

.results-area .card {
  max-width: 600px;
  margin: 0 auto;
}

.intro-text {
  margin-top: 20px;
}

/* steps 관련 스타일 */
.steps-container {
  margin-top: 50px;
}

.bg-light {
  background-color: #f8f9fa !important;
}

.shadow {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}
</style>
