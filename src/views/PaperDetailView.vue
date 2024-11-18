<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

import LeftSection from '@/components/Chatbot/LeftSection.vue'
import DropIcon from '@/assets/DropIcon.png'
import PdfViewer from '@/components/PdfViewer.vue'

const paper = ref(null)
const route = useRoute()
const showPdfViewer = ref(false) // PDF 뷰어 활성화 상태

const togglePdfViewer = () => {
  showPdfViewer.value = !showPdfViewer.value // PDF 뷰어 활성화 상태 토글
}

onMounted(async () => {
  const paperId = route.params.id
  try {
    const response = await axios.get(`https://api.example.com/papers/${paperId}`)
    paper.value = response.data
  } catch (error) {
    console.error('Error fetching paper details:', error)
  }
})
</script>

<template>
  <div class="container-fluid d-flex flex-row m-0 p-0">
    <div class="p-0">
      <left-section />
    </div>
    <div class="main d-flex align-items-center justify-content-center w-100">
      <div v-if="showPdfViewer">
        <PdfViewer />
      </div>
      <div v-else class="d-flex align-items-center dotted-box" @click="togglePdfViewer">
        <div>
          <img :src="DropIcon" class="flex-row align-items-center" />
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
