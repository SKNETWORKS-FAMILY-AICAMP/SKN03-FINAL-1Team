<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '@/axiosConfig' // axiosConfig 가져오기

import LeftSection from '@/components/Chatbot/LeftSection.vue'
import DropIcon from '@/assets/DropIcon.png'
import PdfViewer from '@/components/PdfViewer.vue'

const paper = ref(null)
const route = useRoute()
const showPdfViewer = ref(false) // PDF 뷰어 활성화 상태
const pdfUrl = ref('') // PDF 파일 URL
const paperS3Path = ref('') // paperS3Path 상태 추가

const togglePdfViewer = () => {
  showPdfViewer.value = !showPdfViewer.value // PDF 뷰어 활성화 상태 토글
}

onMounted(async () => {
  const paperId = route.params.id
  if (paperId) {
    try {
      const response = await axios.get(`/papers/${paperId}`)
      paper.value = response.data
      // PDF 파일 URL 설정
      pdfUrl.value = `/download/${paperId}`
      // paperS3Path 설정
      if (response.data.resultCode === 201) {
        paperS3Path.value = response.data.result.paperS3Path
      }
    } catch (error) {
      console.error('Error fetching paper details:', error)
    }
  } else {
    console.error('paperId가 유효하지 않습니다.')
  }
})
</script>

<template>
  <div class="container-fluid d-flex flex-row m-0 p-0">
    <div class="p-0">
      <LeftSection />
    </div>
    <div class="main d-flex align-items-center justify-content-center w-100">
      <div v-if="showPdfViewer">
        <PdfViewer :src="pdfUrl" />
      </div>
      <div v-else class="d-flex align-items-center dotted-box" @click="togglePdfViewer">
        <div>
          <img :src="DropIcon" class="flex-row align-items-center" />
          <p>S3 Path: {{ paperS3Path }}</p>
          <!-- paperS3Path 표시 -->
          <p class="d-flex align-items-center">
            좌측 리스트의 파일을 Drag&Drop하거나 업로드하세요.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.paper-detail {
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}

h2 {
  margin-top: 20px;
  font-size: 24px;
}

p {
  margin: 10px 0;
}

.dotted-box {
  width: 400px; /* 너비 설정 */
  height: 300px; /* 높이 설정 */
  border: 4px dotted #888888; /* 점선 테두리 설정 */
  margin-top: 20px; /* 상단 여백 설정 */
  cursor: pointer; /* 클릭 가능하도록 커서 변경 */
}
</style>
