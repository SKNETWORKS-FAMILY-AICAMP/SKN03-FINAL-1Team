<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '@/axiosConfig'

const route = useRoute()
const paperDoi = route.query.paperDoi || ''
const summary = ref('')
const paperSummarys = ref([]) // 배열로 초기화

const mockResponse = {
  resultCode: 201,
  message: 'Summary retrieved successfully.',
  result: [
    {
      title: 'Hierarchical Text-Conditional Image Generation with CLIP Latents',
      userKeyword: '텍스트-이미지 생성',
      Author: 'test작가',
      publicationYear: 'publicationYear',
      publicationMonth: 'publicationMonth',
      generatedKeyword: '텍스트-이미지 생성 (Text to Image generation)',
      generatedCoreMethod:
        'DALL-E 2는 Diffusion Model과 CLIP의 조합으로 작동하여, 텍스트-이미지 생성에서 높은 수준의 성능을 보여줍니다. 텍스트 입력이 주어지면, CLIP은 이를 분석하여 관련된 이미지 특성을 파악하고, Diffusion Model은 이 정보에 따라 처음에는 노이즈 상태의 이미지에서 시작하여 점진적으로 텍스트에 맞는 이미지를 생성하게 됩니다.',
      generatedTechnologies:
        'Diffusion Model은 이미지를 점진적으로 변화시키는 과정에서 노이즈를 추가하고 제거하여 이미지를 생성하는 방식입니다. 처음에는 순수한 노이즈로부터 시작하여 단계적으로 노이즈를 제거함으로써 텍스트에서 묘사된 구체적인 형태의 이미지를 생성할 수 있습니다. 이러한 역방향 노이즈 제거 과정은 이미지를 점점 선명하고 세밀하게 만들어가며, 고해상도와 자연스러운 디테일을 확보하게 합니다.',
    },
  ],
}

const fetchPaperSummary = async () => {
  try {
    console.log('test입니다.')
    const summaryResponse = await axios.post('/papers/summary/', { paperDoi })
    if (summaryResponse.data.resultCode === 201) {
      paperSummarys.value = mockResponse.result
    } else {
      paperSummarys.value = 'Error: Invalid response code for summary'
    }
  } catch (error) {
    console.error('에러발생', error)
    paperSummarys.value = mockResponse.result
  }
}

onMounted(() => {
  // fetchPaperSummary()
})
</script>

<template>
  <div class="paper-summary-container">
    <div class="paper-summary mt-5 text-start">논문 핵심 요약</div>
    <div class="summary-detail-container flex-column mt-2 overflow-auto" style="max-height: 75vh">
      <div v-if="paperSummarys.length > 0" class="list-group">
        <ul class="list-group">
          <li v-for="paper in paperSummarys" :key="paper.title" class="list-group-item">
            <div class="text-start fw-bold fst-italic">{{ paper.title }} <br /></div>
            <strong>키워드:</strong> {{ paper.generatedKeyword }}<br />
            <strong>핵심 방법론:</strong> {{ paper.generatedCoreMethod }}<br />
            <strong>활용 기술:</strong> {{ paper.generatedTechnologies }}
          </li>
        </ul>
      </div>
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

.summary-detail-container {
  flex-grow: 1;
  color: black;
  background-color: white;
}

.summary-detail-container::-webkit-scrollbar {
  width: 8px; /* 스크롤 바의 너비 */
}

.summary-detail-container::-webkit-scrollbar-thumb {
  background-color: #da7e7e; /* 스크롤 바의 색상 (부트스트랩 기본색) */
  border-radius: 4px; /* 스크롤 바의 모서리 둥글기 */
}

.summary-detail-container::-webkit-scrollbar-thumb:hover {
  background-color: #8a9cce; /* 스크롤 바 호버 시 색상 */
}

.summary-detail-container::-webkit-scrollbar-track {
  background-color: #f8f9fa; /* 스크롤 바 트랙의 배경색 */
}
</style>
