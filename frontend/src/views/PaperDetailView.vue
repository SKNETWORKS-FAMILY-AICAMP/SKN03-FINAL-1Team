<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axiosConfig from '@/axiosConfig' // axiosConfig 파일을 가져옵니다.
import SideComponent from '@/components/common/SideComponent.vue'
const LOGIN_URL = process.env.VUE_APP_LOGIN_URL

const paperS3Path = ref('')
const route = useRoute()
const errorMessage = ref('') // 에러 메시지 저장
const errorTitle = ref('') // 에러 메시지 저장
const showErrorModal = ref(false) // 모달 상태
const errorFlag = ref(300)
onMounted(async () => {
  
  
    try {
      errorFlag.value = 300
      const paperDoi = route.query.paperDoi

      const response = await axiosConfig.get('/papers/detail/', {
        params: { paperDoi },
      })
      errorFlag.value = 200

      paperS3Path.value = `${response.data.result.paperS3Path}#toolbar=1&navpanes=0&view=FitH&page=1` 
      
    } catch (error) {
      if (error.response && error.response.data) {
        const { resultCode, message, errorCode } = error.response.data
        errorMessage.value = message
        errorTitle.value = errorCode
        if (resultCode === 400 || resultCode === 404) {
            errorFlag.value = 400
            showErrorModal.value = true // 모달 창 띄우기
          } else if (resultCode === 403) {
            // 인증 실패: 로그인 페이지로 리다이렉트
            showErrorModal.value = true

            // 3초 후 백엔드 로그인 페이지로 이동
            setTimeout(() => {
              window.location.href = LOGIN_URL
            }, 2500)
          }
      }
      else {
      console.log("알수없는 에러: ", error)
    }
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

const closeErrorModal = () => {
  showErrorModal.value = false
  errorMessage.value = ''
}




</script>

<template>
  
  <div class="container-fluid d-flex flex-row m-0 p-0">
    
    <div class="p-0">
      <SideComponent />
    </div>
    <div class="right-section-wrapper d-flex justify-content-center align-items-center">
      <div v-if="showErrorModal" class="modal-overlay">
        <div class="modal-content">
          <h4>{{ errorTitle }}</h4>
          <p class="error-message">{{ errorMessage }}</p>
          <button @click="closeErrorModal">닫기</button>
        </div>
      </div>


      <div v-if="errorFlag===200" style="height: 95%; width: 100%;" class="pdf-border ">
        <object
      :data="paperS3Path"
      type="application/pdf"
      width="100%"
      height="100%"
    >
      
    </object>
      </div>

      <div v-if="errorFlag===400" > 

        <div class="pdf-box d-flex align-items-center dotted-box">
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
  </div>
</template>


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
  padding: 10px; /* 내부 여백 */
}
/* 기본 예시 */
.pdf-border {
  border: 4px solid #a04747; /* 2px 굵기의 검은색 실선 */
  border-radius: 2px; /* 둥근 모서리 */
  padding: 4px; /* 내부 여백 */
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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-content button {
  background-color: #a04747;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.modal-content button:hover {
  background-color: #7a3737;
}
.error-message {
  white-space: pre-line; /* \n을 줄바꿈으로 인식 */
}
</style>
