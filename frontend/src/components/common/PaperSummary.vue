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
  flag_code.value = 400
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
  <div class="bookmark-container">

  <div class="bookmark-list mt-5 mb-3 text-start">논문 핵심 요약</div>

  <div v-if="flag_code === 200" class="flex-column mt-2" >
    <div class="overflow-auto summary-detail-container " style="max-height: 75vh">
      <div class="summary-container">
  <p class="fw-bolder text-truncate-2">{{ paperSummarys.title }}</p>

  <p><span style="color: #a04747; font-weight: bold;">키워드:</span> {{ paperSummarys.Keyword }}</p>

  <p><span style="color: #a04747; font-weight: bold;">핵심 방법론:</span> <br>{{ paperSummarys.coreMethod }}</p>

  <p><span style="color: #a04747; font-weight: bold;">논문 요약:</span><br> {{ paperSummarys.Summary }}</p>

  
  <p><span style="color: #a04747; font-weight: bold;">핵심 활용 기술 및 설명:</span><br> {{ paperSummarys.coreExplain }}</p>
  <p><span style="color: #a04747; font-weight: bold;">실험 내용:</span><br> {{ paperSummarys.experimentContext }}</p>

  <p><span style="color: #a04747; font-weight: bold;">실험 결과:</span><br> {{ paperSummarys.experimentResult }}</p>

  
</div>


      </div>
            
  </div>
    
  <div v-if="flag_code === 404" class="d-flex flex-column align-items-center justify-content-center"
    style="flex-grow: 1;">
    <strong> Documento에서 지원하는 핵심 요약이 <br>존재하지 않는 논문입니다 <br></strong>

    <strong><br>키워드 최적화 및 논문 검색 과정을 통해 <br> 논문을 검색해보세요 :)</strong>
      </div>



  </div>
  


 


</template>

<style scoped>
.bookmark-container {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    padding: 20px 0px 20px 20px;
  }
  
  .bookmark-list {
    position: relative;
    margin-top: 20px;
    padding: 10px 10px;
    font-size: 20px;
    color: white;
  }
  
  .bookmark-list::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 1px;
    background-color: white;
  }
  
.summary-container{
  background-color: #f8f9fa;
  margin-right: 5px;
  border-radius: 20px;
  padding: 15px;
  text-align: left;
}

.custom-color {
  color: #a04747 !important; /* 원하는 색상 코드 입력 */
}

.text-truncate-2 {
    display: -webkit-box; /* Flexbox 사용을 위해 설정 */
    -webkit-line-clamp: 2; /* 표시할 최대 줄 수 */
    -webkit-box-orient: vertical; /* 수직 방향으로 박스 정렬 */
    overflow: hidden; /* 넘치는 내용 숨기기 */
    text-overflow: ellipsis; /* 생략 표시(...) */
  }

.summary-detail-container {
  
  color: black;
  
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
