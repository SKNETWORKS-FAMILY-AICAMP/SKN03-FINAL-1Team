<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axiosConfig from '@/axiosConfig' // axiosConfig 파일을 가져옵니다.
import SideComponent from '@/components/common/SideComponent.vue'

const paperS3Path = ref('')
const pdfFile = ref(null)
const route = useRoute()
const accessToken = 'temp' // 실제 토큰을 할당

onMounted(async () => {
  const paperDoi = route.query.paperDoi
  if (paperDoi) {
    try {
      const response = await axiosConfig.get('/papers/detail/', {
        params: { paperDoi },
        headers: {
          Authorization: `Bearer ${accessToken}`, // Authorization 헤더에 토큰 포함
        },
      })
      if (response.data.resultCode === 200 && response.data.result.paperS3Path) {
        paperS3Path.value = response.data.result.paperS3Path
        fetchPdf(paperS3Path.value) // PDF 파일 가져오기 함수 호출
        alert('PDF URL을 성공적으로 가져왔습니다!')
      } else {
        console.error('PDF URL을 가져오는데 실패했습니다.')
        alert('PDF URL을 가져오는데 실패했습니다.')
      }
    } catch (error) {
      console.error('Error fetching PDF URL:', error)
      alert('PDF URL을 가져오는데 실패했습니다.')
    }
  } else {
    console.warn('paperDoi 쿼리 파라미터가 없습니다.')
    alert('paperDoi 쿼리 파라미터가 없습니다.')
  }

  // 드래그 앤 드롭 이벤트 추가
  const dropBox = document.querySelector('.pdf-box')
  dropBox.addEventListener('dragover', (e) => {
    e.preventDefault()
    dropBox.classList.add('dragging-over')
  })

  dropBox.addEventListener('dragleave', () => {
    dropBox.classList.remove('dragging-over')
  })

  dropBox.addEventListener('drop', (e) => {
    e.preventDefault()
    dropBox.classList.remove('dragging-over')
    const draggable = document.querySelector('.dragging')
    if (draggable) {
      alert('PDF 박스에 드랍되었습니다!')
    }
  })
})

const fetchPdf = async (url) => {
  // try {
  //   const response = await fetch(url)
  //   const blob = await response.blob()
  //   pdfFile.value = URL.createObjectURL(blob)
  // } catch (error) {
  //   console.error('Error fetching PDF:', error)
  // }
}
</script>

<template>
  <div class="container-fluid d-flex flex-row m-0 p-0">
    <div class="p-0">
      <SideComponent />
    </div>
    <div class="right-section-wrapper d-flex justify-content-center align-items-center">
      <div v-if="paperS3Path" style="background-color: rgba(255, 0, 0, 0.3); height: 90%; width: 90%; border: 1px solid red;">
        <!-- <div v-if="showPdfViewer"> -->
        <!-- <PdfViewer :src="pdfFile" /> -->
      </div>
      <div v-else class="pdf-box d-flex align-items-center dotted-box">
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


<!-- <template>
  <div class="container-fluid d-flex flex-row m-0 p-0">
    <div class="main d-flex align-items-center justify-content-center w-100">
      <div v-if="showPdfViewer">
        <PdfViewer :src="pdfFile" />
      </div>
      <div v-else class="pdf-box d-flex align-items-center dotted-box">
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
</template> -->

<style scoped>
.container-fluid {
  width: 100%;
}
.right-section-wrapper {
  flex-grow: 1; /* 나머지 공간을 차지하도록 설정 */
  display: flex;
  justify-content: center; /* 수평 중앙 정렬 */
  align-items: center; /* 수직 중앙 정렬 */
  width: 1600px;
}



.dotted-box {
  width: 400px;
  height: 300px;
  border: 4px dotted #888888;
  margin-top: 20px;
  cursor: pointer;
}

.dragging-over {
  border-color: #555; /* 드래그 중일 때 테두리 색 변경 */
}
</style>
