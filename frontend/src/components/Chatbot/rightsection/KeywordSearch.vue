<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.
import BookmarkIcon from '@/assets/SideComponent/BookmarkIcon.png'

const router = useRouter()
const LOGIN_URL = process.env.VUE_APP_LOGIN_URL
const showErrorModal = ref(false)
const inputPrompt = ref('')
const generatedResults = ref(null)
const loading = ref(false) // 로딩 상태 추가
const errorMessage = ref('') // 에러 메시지 상태 추가
const errorTitle = ref('')
const showIntroAndSteps = ref(true)

const steps = [
  { id: 1, text: '키워드 변환을 통해 내가 원하는 논문 검색에 필요한 키워드를 추출하세요.' },
  { id: 2, text: '해당 키워드를 기반으로 논문을 검색하세요.' },
  { id: 3, text: '검색된 논문들을 저장하고 논문 파악을 통해 논문의 난이도를 파악하세요.' },
]



// 키워드 최적화 요청 (POST 요청)
const optimizeKeywords = async () => {
  errorMessage.value = ''
  showIntroAndSteps.value = false
  loading.value = true // 로딩 시작
  generatedResults.value = ref(null)
  try {
    const response = await axios.post(
        '/papers/transformation/',
        {
          userPrompt: inputPrompt.value,
        },

      )
      generatedResults.value = response.data.result
      
  } catch (error) {
    if (error.response && error.response.status) {
      const { resultCode, message, errorCode } = error.response.data
      errorMessage.value = message
      errorTitle.value = errorCode
      showErrorModal.value = true
      if (resultCode === 403) {
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


  } finally {
    loading.value = false // 로딩 종료
  }
}

// 메시지 전송 핸들러
const handleOptimization = () => {
  if (inputPrompt.value.trim() !== '') {
    optimizeKeywords()
  } else {
    console.warn('최적화할 프롬프트를 입력해보세요.')
  }
}
const requestPaperByDoi = async (paperDoi) => {
  router.push({
        path: '/papers/detail/',
        query: { paperDoi },
      })
}
const closeErrorModal = () => {
  showErrorModal.value = false; // 모달 숨기기
  inputPrompt.value = ''
  errorMessage.value = ''; // 에러 메시지 초기화
  errorTitle.value = ''; // 에러 제목 초기화
  showIntroAndSteps.value = true; // steps를 다시 보여주기
};

const showCopyMessage = ref(false);

const copyKeyword = (keyword) => {
  // 키워드를 클립보드에 복사
  navigator.clipboard.writeText(keyword).then(() => {
    // 성공적으로 복사되었을 때 알림 표시
    showCopyMessage.value = true;

    // 2초 후 알림 숨기기
    setTimeout(() => {
      showCopyMessage.value = false;
    }, 2000);
  }).catch((error) => {
    console.error('키워드 복사 실패:', error);
  });
};


</script>
<template>
  <div class="main-container">

    <div class="test-content">
      <div class="input-area d-flex p-2">
        <input
          v-model="inputPrompt"
          type="text"
          class="form-control chat-input"
          placeholder="원하는 논문의 내용을 자신만의 언어로 표현해보세요."
          @keyup.enter="handleOptimization"
          :disabled="loading"
        />
        <button class="btn send-button" @click="handleOptimization" :disabled="loading">></button>
      </div>
      <div v-if="showErrorModal" class="modal-overlay">
        <div class="modal-content">
          <h4>{{ errorTitle }}</h4>
          <p class="error-message">{{ errorMessage }}</p>
          <button @click="closeErrorModal">닫기</button>
        </div>
      </div>
      <div v-if="loading" class="d-flex justify-content-center my-3">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">로딩 중...</span>
        </div>
      </div>

      <div v-else>
        

        <div v-if="generatedResults" class="results-area mt-5">
          <div class="mb-4">
            <p class="text-start dynamic-padding">{{ generatedResults.generatedPrompt }}</p>
            <!-- ~~의 키워드 검색 결과입니다. -->
          </div>


          <div
            v-for="(keywordItem, index) in generatedResults.generatedKeywordList"
            :key="index"
            class="mb-4"
          >
          
          <div @click="copyKeyword(keywordItem.generatedKeyword.split('[')[0])" style="cursor: pointer;">
  <h5 class="fw-bold text-start dynamic-padding">
    {{ index + 1 }}. {{ keywordItem.generatedKeyword.split('[')[1].split(']')[0] }}
    <!-- 한국어 -->
  </h5>
  <h5 class="fw-bold text-start dynamic-padding pb-1">
    {{ keywordItem.generatedKeyword.split('[')[0] }}
    <!-- 영어 -->
  </h5>
</div>
<p v-if="showCopyMessage" class="copy-message">키워드가 복사되었습니다!</p>


         


            <div class="d-flex flex-wrap">
              <div
                v-for="(paper, paperIndex) in keywordItem.paperList"
                :key="paperIndex"
                class="card mb-3 shadow-sm me-3"
                @click="requestPaperByDoi(paper.paperDoi)"
                style="cursor: pointer; width: 30%"
                title="해당 논문 자세히 보기 "
              >
                <div class="card-body text-start">
                  <div class="d-flex align-items-center">
                    <p class="fw-bold">{{ paper.title }}</p>
                    <img :src="BookmarkIcon" class="px-1" />
                  </div>
                  <p>
                    {{
                      paper.engAbstract.length > 250
                        ? paper.engAbstract.slice(0, 250) + '...'
                        : paper.engAbstract
                    }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="showIntroAndSteps" class="intro-text text-center mb-4">
          <p class="text-muted">논문 검색이 어려우신가요? <br /></p>
          <p class="text-muted">
            도큐멘토와 함께 검색 키워드를 정의하고, <br />
            읽어야 할, 읽을 수 있는 논문을 탐색해보아요!
          </p>
        </div>
      </div>








      <div v-if="showIntroAndSteps" class="steps-container">
        <div class="d-flex justify-content-between mt-5">
          <div
            class="p-3 bg-light rounded shadow text-center m-2"
            v-for="step in steps"
            :key="step.id"
            style="flex: 1"
          >
            <h5>Step {{ step.id }}</h5>
            <p>{{ step.text }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.main-container {
  max-height: 80vh; /* 최대 높이 설정 */
  overflow-y: auto; /* 수직 스크롤 추가 */
  display: flex;
  align-items: center; /* 수직 가운데 정렬 */
  justify-content: center; /* 수평 가운데 정렬 */
}

.main-container::-webkit-scrollbar {
  width: 8px; /* 스크롤 바의 너비 */
}

.main-container::-webkit-scrollbar-thumb {
  background-color: #da7e7e; /* 스크롤 바의 색상 (부트스트랩 기본색) */
  border-radius: 4px; /* 스크롤 바의 모서리 둥글기 */
}

.main-container::-webkit-scrollbar-thumb:hover {
  background-color: #8a9cce; /* 스크롤 바 호버 시 색상 */
}

.main-container::-webkit-scrollbar-track {
  background-color: #f8f9fa; /* 스크롤 바 트랙의 배경색 */
}

.test-content {
  margin: auto;
  max-width: 1000px;
}

.input-area {
  border: 1px solid #a04747;
  border-radius: 50px;
  display: flex;
  gap: 10px;
  width: 100%; /* 좌우로 꽉 차게 설정 */
  margin-bottom: 5vh;
}

.chat-input {
  flex-grow: 1; /* 입력 필드가 남는 공간을 차지하도록 설정 */
  padding: 10px;
  border: none;
}

.chat-input:focus {
  border-color: none;
  box-shadow: none;
  outline: none; /* 포커스 시 기본 아웃라인 제거 */
}

.send-button {
  background-color: #a04747;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 50%;
  width: 50px;
  height: 50px;
}

.send-button:hover {
  background-color: #7a3737; /* 어두운 빨간색으로 변경 */
}

.results-area .card {
  max-width: 600px;
  margin: 0 auto;
  border: 1px solid #a04747;
}

.intro-text {
  margin-top: 20px;
}

/* steps 관련 스타일 */
.steps-container {
  margin-top: 50px;
}

.bg-light {
  background-color: #f8f9fa !important;
}

.shadow {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}
@media (max-width: 999px) {
  .dynamic-padding {
    padding-left: 0 !important;
  }
}

@media (min-width: 1000px) {
  .dynamic-padding {
    padding-left: 1rem !important;
  }
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
.copy-message {
  color: green;
  font-size: 14px;
  margin-top: 10px;
}
</style>
