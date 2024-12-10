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
    const mockResponse = {
      resultCode: 201,
      message: 'Preceding papers retrieved successfully.',
      result: {
        paperList: [
          {
            paperDoi: 'test doi',
            parentPaperDoi: '10.18653/v1/2020.acl-demos.10',
            title: 'test title',
            generatedKeyword: '테스트 키워드',
            similarity: 92,
          },
          {
            paperDoi: 'test doi',
            parentPaperDoi: '10.18653/v1/2020.acl-demos.10',
            title: 'test title',
            generatedKeyword: '테스트 키워드',
            similarity: 75,
          },
        ],
      },
    }
    console.error('선행 논문을 가져오는 중 오류 발생:', error)
    // 에러가 발생했을 때 mockResponse를 사용하여 papers를 설정합니다.
    if (mockResponse.resultCode === 201 && mockResponse.result.paperList) {
      papers.value = mockResponse.result.paperList
    }
  }
}

onMounted(() => {
  // fetchPriorPapers()
})
</script>

<template>
  <div class="prior-paper-container flex-column">
    <div class="prior-paper-list mt-5 text-start">선행 논문 추천</div>
    <ul class="list-group">
      <li
        v-for="paper in papers"
        :key="paper.paperDoi"
        class="list-group-item text-start my-2 rounded-4"
      >
        <div class="row">
          <div class="col-auto mt-2">
            <div
              class="progress-circle"
              :style="{
                background: `conic-gradient(#a04747 0% ${paper.similarity}%, lightgray ${paper.similarity}% 100%)`,
              }"
            >
              <span>{{ paper.similarity }}%</span>
            </div>
          </div>
          <div class="col mt-2">
            <strong class="fst-italic">{{ paper.title }}</strong>
            <p>{{ paper.generatedKeyword }}</p>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.prior-paper-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.prior-paper-list {
  position: relative;
  margin-top: 20px;
  padding: 10px 0;
  font-size: 20px;
  color: white;
}

.prior-paper-list::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background-color: white;
}

.progress-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75em;
  color: #a04747;
}

.progress-circle::before {
  content: '';
  position: absolute;
  width: 85%;
  height: 85%;
  background-color: white;
  border-radius: 50%;
  z-index: 1;
}

.progress-circle span {
  z-index: 2;
}
</style>
