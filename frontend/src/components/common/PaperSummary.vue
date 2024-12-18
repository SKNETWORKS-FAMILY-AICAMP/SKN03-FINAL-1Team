<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '@/axiosConfig'
import warningImage from '@/assets/warning.svg'
const route = useRoute()
const paperDoi = route.query.paperDoi || ''
const flag_code = ref(400)
const paperSummarys = ref([]) // 배열로 초기화

const fetchPaperSummary = async () => {
  try {
    
    console.log('test입니다.')
    const summaryResponse = await axios.get('/papers/summary/', {
  params: { paperDoi },
});
  console.log(summaryResponse.data.resultCode)
    if (summaryResponse.data.resultCode === 200) {
      paperSummarys.value = summaryResponse.data.result
      flag_code.value = 200
    } else {
      paperSummarys.value = 'Error: Invalid response code for summary'
    }
  } catch (error) {
  if (error.response && error.response.data) {
    const { resultCode, message} = error.response.data
    flag_code.value = resultCode
    console.log(message)
}
  }
}

onMounted(() => {
   fetchPaperSummary()
})
</script>

<template>
  <div class="paper-summary-container">

  <div class="paper-summary mt-5 text-start">논문 핵심 요약</div>

  <div v-if="flag_code === 200" class="summary-detail-container flex-column mt-2 overflow-auto" style="max-height: 75vh">
      <div class="list-group">
        <ul class="list-group">
          <li v-for="paper in paperSummarys" :key="paper.title" class="list-group-item">
            <div class="text-start fw-bold fst-italic">{{ paper.title }} <br /></div>
            <strong>논문 요약:</strong> {{ paper.Summary }}<br />
            <strong>요약 키워드:</strong> {{ paper.Keyword }}<br />
            <strong>핵심 방법론:</strong> {{ paper.coreMethod }}<br />
            <strong>핵심 활용 기술 및 설명:</strong> {{ paper.coreExplain }}<br />
            <strong>실험 결과:</strong> {{ paper.experimentResult }}<br />
            <strong>실험 내용:</strong> {{ paper.experimentContext }}
            
          </li>
        </ul>
      </div>

    
      
  </div>
    
  <div v-if="flag_code === 404" >
    <img
      :src="warningImage"
      alt="warning"
      width=80%
      class="warning-image"
    />

    <p>해당 논문 핵심 요약은 아직 준비되지 않았습니다</p>
    <p>이는 추후 없데이트 예정입니다</p> 
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
  margin: 20px;
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
.warning-image {
  filter: brightness(0) saturate(100%) invert(75%) sepia(70%) saturate(500%) hue-rotate(1deg) brightness(95%) contrast(90%);
}
</style>
