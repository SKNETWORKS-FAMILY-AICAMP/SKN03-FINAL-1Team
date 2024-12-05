<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '@/axiosConfig'

// const paper = ref(null)
// const route = useRoute()
// const showPdfViewer = ref(false)
// const pdfUrl = ref('')
// const paperS3Path = ref('')
// const pdfFile = ref(null) // 추가
// const priorPapers = ref(null) // 추가: priorPapers 데이터를 저장할 변수
// const accessToken = 'temp' // 실제 토큰을 할당

// const fetchPaperDetails = async (paperDoi) => {
//   try {
//     const response = await axios.get(`/papers/select/`, {
//       params: { paperDoi },
//       headers: {
//         Authorization: `Bearer ${accessToken}`, // Authorization 헤더에 토큰 포함
//       },
//     })
//     if (response.data && response.data.resultCode === 200) {
//       paperS3Path.value = response.data.result.paperS3Path
//     } else {
//       console.error('Failed to fetch paper details')
//     }
//   } catch (error) {
//     console.error('Error fetching paper details:', error)
//   }
// }

// const fetchPdf = async (url) => {
//   try {
//     const response = await fetch(url)
//     const blob = await response.blob()
//     pdfFile.value = URL.createObjectURL(blob)
//     showPdfViewer.value = true
//   } catch (error) {
//     console.error('Error fetching PDF:', error)
//   }
// }

// onMounted(async () => {
//   const paperDoi = route.query.paperDoi
//   if (paperDoi) {
//     await fetchPaperDetails(paperDoi)
//     // await fetchPriorPapers(paperDoi)
//   } else {
//     console.warn('paperDoi 쿼리 파라미터가 없습니다.')
//   }
// })

// // paperS3Path가 변경될 때마다 fetchPdf를 호출
// watch(paperS3Path, async (newPath) => {
//   if (newPath) {
//     await fetchPdf(newPath)
//   }
// })
</script>

<template>
  <div class="container-fluid d-flex flex-row m-0 p-0">
    <div class="p-0">
      <SideComponent />
    </div>
    <div class="main d-flex align-items-center justify-content-center w-100">
      <div v-if="showPdfViewer">
        <PdfViewer :src="pdfFile" />
      </div>
      <div v-else class="d-flex align-items-center dotted-box">
        <div>
          <img :src="DropIcon" class="flex-row align-items-center" />
          <p>S3 Path: {{ paperS3Path }}</p>
          <p class="d-flex align-items-center">
            좌측 리스트의 파일을 Drag&Drop하거나 업로드하세요.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
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
