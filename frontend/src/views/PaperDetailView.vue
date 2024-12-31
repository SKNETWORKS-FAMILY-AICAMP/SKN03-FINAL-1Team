<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axiosConfig from '@/axiosConfig' // axiosConfig 파일을 가져옵니다.
import SideComponent from '@/components/common/SideComponent.vue'
import homeboomark from '@/assets/homebookmark.png'
import homesearch from '@/assets/homesearch.png'
import hometrans from '@/assets/hometrans.png'



const LOGIN_URL = process.env.VUE_APP_LOGIN_URL

const paperS3Path = ref('')
const route = useRoute()
const errorMessage = ref(`왼쪽의 사이드 바를 눌러 북마크하신 논문을 확인하거나\n돋보기 아이콘을 통해 논문탐색을 시작해 주세요`) // 에러 메시지 저장
const errorTitle = ref('') // 에러 메시지 저장
const showErrorModal = ref(false) // 모달 상태
const errorFlag = ref(300)
// 모달창 표시 여부 관리
const isModalVisible = ref(false)

// "오늘 하루 보지 않기" 체크박스 상태
const doNotShowToday = ref(false)

// 로컬 스토리지 키
const LOCAL_STORAGE_KEY = 'hide_modal_today'
const showIntroAndSteps = ref(true)

const steps = [
  { id: 1, text: '<br>좌측의 <span style="color: #902e2e; font-weight: bold;">사이드바</span>를 열어서<br><span style="color: #902e2e; font-weight: bold;">저장</span>했던 논문을 확인하고<br><span style="color: #902e2e; font-weight: bold;">상세정보</span>를 탐색하세요',
  imgElement: homeboomark,
  },
  { id: 2, text: '<br>좌측 하단 <span style="color: #902e2e; font-weight: bold;">돋보기 아이콘</span>을 선택해 <br><span style="color: #902e2e; font-weight: bold;">메인 서비스</span> 화면으로 이동 후 <br><span style="color: #902e2e; font-weight: bold;">키워드 추출</span> 서비스를 이용하세요.' ,
  imgElement: hometrans,
  },
  { id: 3, text: '<br>좌측 하단 <span style="color: #902e2e; font-weight: bold;">돋보기 아이콘</span>을 선택해 <br><span style="color: #902e2e; font-weight: bold;">메인 서비스</span> 화면으로 이동 후 <br><span style="color: #902e2e; font-weight: bold;">논문 탐색</span> 서비스를 이용하세요.' ,
  imgElement: homesearch,
  },
]


onMounted(async () => {
    
  
    try {
      errorFlag.value = 300
      const paperDoi = route.query.paperDoi
      console.log("papaerDoi: ", paperDoi)
      const response = await axiosConfig.get('/papers/detail/', {
        params: { paperDoi },
      })
      if (response.data.resultCode === 200){
        showIntroAndSteps.value = false

        errorFlag.value = 200
        paperS3Path.value = `${response.data.result.paperS3Path}#toolbar=1&navpanes=0&view=FitH&page=1` 
      } 
      
    } catch (error) {
      if (error.response && error.response.data) {
        isModalVisible.value = false
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
  

})

const closeModal = () => {
  showErrorModal.value = false
  isModalVisible.value = false
  errorMessage.value = ''
  if (doNotShowToday.value) {
    // 체크박스가 활성화된 경우 로컬 스토리지에 값 저장
    localStorage.setItem(LOCAL_STORAGE_KEY, 'true')
  }
}

const closError = () => {
  showErrorModal.value = false
  showIntroAndSteps.value = true
}

// 컴포넌트가 마운트되면 라우트와 로컬 스토리지 값 확인
onMounted(() => {
  const storedValue = localStorage.getItem(LOCAL_STORAGE_KEY)
  console.log("isin")
  if (!storedValue) {
    // 로컬 스토리지 값이 없고, 현재 페이지가 대상 페이지일 때 모달 표시
    
    isModalVisible.value = true
  }
})



</script>

<template>
      


  <div class="container-fluid d-flex flex-row m-0 p-0">
    <div class="p-0">
      <SideComponent />
    </div>


    <div v-if="isModalVisible" class="modal-overlay">
    <div class="modal-content">
      <h4>WELCOME TO DOCUMENTO!</h4>
      <p class="error-message">{{ errorMessage }}</p>     

      <div class="d-flex justify-content-around">  
        <div class="checkbox-container">
        <input 
          type="checkbox" 
          id="doNotShowToday" 
          v-model="doNotShowToday" 
        />
        <label for="doNotShowToday">오늘 하루 보지 않기</label>
      </div>
      <button class="close-button" @click="closeModal">닫기</button>
      </div>
      




    </div>
  </div>
    








    <div class="right-section-wrapper d-flex justify-content-center align-items-center">
      <div v-if="showErrorModal" class="modal-overlay">
        <div class="modal-content">
          
          <p class="error-message">{{ errorMessage }}</p>
          <button @click="closError">닫기</button>
        </div>
      </div>

      <div v-if="showIntroAndSteps" class="intro-text text-center mb-4 ">
          <p class="text-muted">논문상세 제공을 위한 논문 정보가 입력되지 않았어요 <br /></p>
          <p class="text-muted">
            아래의 서비스들 중에<br />
            하나를 선택해서 DOCUMENTO와 함께 논문 탐색을 진행해 주세요
          </p>

          <div class="steps-container">
        <div class="d-flex justify-content-between mt-5">
          <div
            class="p-3 bg-light rounded  text-center m-2 "
            v-for="step in steps"
            :key="step.id"
            style="flex: 1;"
          >
          <div class="d-flex align-items-center justify-content-between">
            
            <div class="circle"><img :src="step.imgElement"  
              width="15px" height="15px"/></div>
              <h5 style="margin-top: 6px;">Service {{ step.id }}</h5>
              <div class="dummy-circle"><img :src="step.imgElement"  
                width="15px" height="auto"/></div>
          </div>

            
            <p v-html="step.text"></p>
          </div>
        </div>
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
.checkbox-container {
  margin: 1rem 0;
  text-align: left;
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
  width: 400px;
  height: 250px;
  display: flex;
  justify-content: space-between;
  border: 5px solid #a04747;

}

.modal-content button {
  background-color: white;
  color: #a04747;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.modal-content button:hover {
  background-color: #a04747;
  color: white;
}
.error-message {
  white-space: pre-line; /* \n을 줄바꿈으로 인식 */
  text-align: left;
}

.intro-text {
  margin-top: 20px;

  width: 80%;
  
}

.text-muted {
  color : #8A8A8A;
  font-size: 20px;
}

/* steps 관련 스타일 */
.steps-container {
  margin-top: 40px;
  margin: 10px;


}

.bg-light {
  background-color: #f8f9fa ;
  border: 2px solid #a04747;
  border-radius: 20px !important;

}

.circle {
  width: 30px; /* 원의 너비 */
  height: 30px; /* 원의 높이 */
  background-color: #a04747; /* 원의 색상 */
  border-radius: 50%; /* 둥근 모서리를 만들어 원형으로 */
  display: flex;
  align-items: center;
  justify-content: center;
}
.dummy-circle {
  width: 25x; /* 원의 너비 */
  height: 25px; /* 원의 높이 */
  background-color: white; /* 원의 색상 */
  border-radius: 50%; /* 둥근 모서리를 만들어 원형으로 */
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
