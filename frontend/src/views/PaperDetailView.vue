<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '@/axiosConfig'

import SideComponent from '@/components/common/SideComponent.vue'
import DropIcon from '@/assets/DropIcon.png'
import PdfViewer from '@/components/PdfViewer.vue'
import PaperDetail from '@/components/common/PaperDetail.vue'

const paper = ref(null)
const route = useRoute()
const showPdfViewer = ref(false)
const pdfUrl = ref('')
const paperS3Path = ref('')
const pdfFile = ref(null) // 추가
const priorPapers = ref(null) // 추가: priorPapers 데이터를 저장할 변수

const togglePdfViewer = () => {
  showPdfViewer.value = !showPdfViewer.value
}

onMounted(async () => {
  // 테스트를 위해 URL 고정
  pdfUrl.value =
    'https://documento-s3.s3.ap-northeast-2.amazonaws.com/papers/acl/2020/10.18653_v1_2020.acl-demos.1.pdf'
  fetchPdf(pdfUrl.value) // PDF 파일 가져오기 함수 호출

  const paperId = route.params.id
  const s3Path = route.query.paperS3Path
  if (s3Path) {
    paperS3Path.value = s3Path
  }

  if (paperId) {
    try {
      const response = await axios.get(`/papers/${paperId}`)
      paper.value = response.data
      if (!s3Path && response.data.resultCode === 201) {
        paperS3Path.value = response.data.result.paperS3Path
      }
    } catch (error) {
      console.error('Error fetching paper details:', error)
    }
  } else {
    console.error('paperId가 유효하지 않습니다.')
  }

  // paperDoi 쿼리 파라미터 읽기
  const paperDoi = route.query.paperDoi
  if (paperDoi) {
    try {
      const priorResponse = await axios.get('/papers/priorpapers/', {
        params: { paperDoi },
      })
      priorPapers.value = priorResponse.data
      console.log('Prior papers:', priorPapers.value)
    } catch (error) {
      console.error('Error fetching prior papers:', error)
    }
  } else {
    console.warn('paperDoi 쿼리 파라미터가 없습니다.')
  }
})

const fetchPdf = async (url) => {
  try {
    const response = await fetch(url)
    const blob = await response.blob()
    pdfFile.value = URL.createObjectURL(blob)
  } catch (error) {
    console.error('Error fetching PDF:', error)
  }
}
</script>

<template>
  <div class="container-fluid d-flex flex-row m-0 p-0">
    <div class="p-0">
      <SideComponent />
    </div>
    <div class="main d-flex align-items-center justify-content-center w-100">
      <div v-if="showPdfViewer">
        <PdfViewer :src="pdfFile" />
        <!-- src를 pdfFile로 변경 -->
      </div>
      <div v-else class="d-flex align-items-center dotted-box" @click="togglePdfViewer">
        <div>
          <img :src="DropIcon" class="flex-row align-items-center" />
          <p>S3 Path: {{ paperS3Path }}</p>
          <p class="d-flex align-items-center">
            좌측 리스트의 파일을 Drag&Drop하거나 업로드하세요.
          </p>
        </div>
      </div>
    </div>
    <div>
      <PaperDetail />
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
  width: 400px;
  height: 300px;
  border: 4px dotted #888888;
  margin-top: 20px;
  cursor: pointer;
}
</style>
