<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.
import BookmarkIcon from '@/assets/SideComponent/BookmarkIcon.png'
import UnbookmarkIcon from '@/assets/bookmarksvg.svg'
import LoadingAnimation from '@/components/common/LoadingAnimation.vue'

const router = useRouter()
const LOGIN_URL = process.env.VUE_APP_LOGIN_URL
const showErrorModal = ref(false)
const inputPrompt = ref('')
const generatedResults = ref(null)
const loading = ref(false) // 로딩 상태 추가
const errorMessage = ref('') // 에러 메시지 상태 추가
const errorTitle = ref('')
const showIntroAndSteps = ref(true)


const isBookmarkModalVisible = ref(false) // 모달창 표시 여부
const selectedBookmark = ref(null) // 선택된 북마크 정보
const selectedKeyword = ref(null) // 선택된 북마크 정보
const steps = [
  { id: 1, text: '<br><span style="color: #902e2e; font-weight: bold;">키워드 변환</span>을 통해<br>내가 원하는 논문 검색에 필요한 <br>키워드를 추출하세요.' },
  { id: 2, text: '<br>원하는 키워드를 클릭해 <br><span style="color: #902e2e; font-weight: bold;">키워드 복사</span>를  수행하세요.' },
  { id: 3, text: '<br>검색된 논문들을 저장하고<br><span style="color: #902e2e; font-weight: bold;">추출된 논문 내용</span>을 통해 <br>원하는 논문을 선택하세요.' },
]



// 키워드 최적화 요청 (POST 요청)
const optimizeKeywords = async () => {
  errorMessage.value = ''
  
  loading.value = true // 로딩 시작
  generatedResults.value = null
  
  console.log("generatedResults1 : " ,generatedResults)
  
  try {
    console.log("generatedResults2 : " ,generatedResults)
    const response = await axios.post(
        '/papers/transformation/',
        {
          userPrompt: inputPrompt.value,
        }
      )

      generatedResults.value = response.data.result
      showIntroAndSteps.value = false
  } catch (error) {
    console.log("?")
    showIntroAndSteps.value = true
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



const copyKeyword = (keywordItem) => {
  // 선택된 키워드의 showCopyMessage를 true로 설정
  keywordItem.showCopyMessage = true;

  // 클립보드에 키워드 복사
  navigator.clipboard.writeText(keywordItem.generatedKeyword.split('[')[0])
    .then(() => {
      // 2초 후 해당 키워드의 showCopyMessage를 false로 설정
      setTimeout(() => {
        keywordItem.showCopyMessage = false;
      }, 2000);
    })
    .catch((error) => {
      console.error('키워드 복사 실패:', error);
    });
};


const updateBookmark = ref(null);

// 북마킹 함수 수정
const Bookmarking = async (userKeyword, paperDoi, bookMark) => {
  console.log("userKeyword : ", userKeyword)

  try {
    const inverseBookMark = !bookMark;
    const response = await axios.post('/users/bookmarks/', {
      userKeyword,
      paperDoi,
      bookMark: inverseBookMark,
    });

    if (response.data.resultCode === 201) {
      
      console.log("good")
      updateBookmark.value = inverseBookMark
    }
    
    isBookmarkModalVisible.value = false;
  } catch (error) {
    console.error('북마크 처리 중 오류 발생:', error);
  }
};

// 삭제 확인 모달 열기
const openBookmarkModal = (paper, keyword ) => {
  
  selectedBookmark.value = paper
  selectedKeyword.value = keyword
  console.log("selectedBookmark : " ,selectedKeyword)
  if (updateBookmark.value !== null){
    console.log("not null")
    console.log()
    selectedBookmark.value['bookmarked'] = updateBookmark
  }
  isBookmarkModalVisible.value = true
}

// 삭제 확인 모달 닫기
const closeBookmarkModal = () => {
  isBookmarkModalVisible.value = false
}









</script>





<template>

<div class="input-area d-flex p-2 mt-3">
        <input
          v-model="inputPrompt"
          type="text"
          class="form-control chat-input"
          placeholder="원하는 논문의 내용을 자신만의 언어로 표현해보세요."
          @keyup.enter="handleOptimization"
         
        />
        <button class="btn send-button" @click="handleOptimization" >></button>
  </div>
  
  
  <div class="main-container">

    <div class="test-content">

      <!-- 에러모달  -->


      <div v-if="loading" class="d-flex justify-content-center my-3"
      >
        <LoadingAnimation />
      </div>


      <div v-else>
        
        <div v-if="showErrorModal" class="modal-overlay">
        <div class="modal-content">
          <p class="error-message"
          >{{ errorMessage }}</p>
          <div class="modal-content-button "
          @click="closeErrorModal"
          > 닫기</div>
        </div>
      </div>

      <div v-if="showIntroAndSteps" class="intro-text text-center mb-4 ">
          <p class="text-muted">논문 검색이 어려우신가요? <br /></p>
          <p class="text-muted">
            DOCUMENTO와 함께 검색 키워드를 정의하고, <br />
            읽어야 할, 읽을 수 있는 논문을 탐색해보아요!
          </p>

          <div class="steps-container">
        <div class="d-flex justify-content-between mt-5">
          <div
            class="p-3 bg-light rounded  text-center m-2 "
            v-for="step in steps"
            :key="step.id"
            style="flex: 1;"
          >
            <h5>Step {{ step.id }}</h5>
            <p v-html="step.text"></p>
          </div>
        </div>
      </div>


        </div>




        <div v-if="generatedResults" >

          <div style="text-align: left; margin-bottom: 18px;">
            <strong style="color: #a04747;">{{ generatedResults.generatedPrompt }}</strong>
            에 대한 주요 키워드는 다음과 같이 설정 할 수 있습니다.
          </div>

          <div class="results-container">
            <div
            v-for="(keywordItem, index) in generatedResults.generatedKeywordList"
            :key="index"
            class="mb-4"
          >
          
          <div @click="copyKeyword(keywordItem)" style="cursor: pointer;">
  <h5 class="fw-bold text-start dynamic-padding mb-3">
    {{ index + 1 }}. {{ keywordItem.generatedKeyword.split('[')[1].split(']')[0] }} ( {{ keywordItem.generatedKeyword.split('[')[0] }} )
    <!-- 한국어 -->
  </h5>

</div>
<p v-if="keywordItem.showCopyMessage" class="copy-message">키워드가 복사되었습니다!</p>

<div
  class="d-flex mx-3 justify-content-start"
>
  <div
    v-for="(paper, paperIndex) in keywordItem.paperList"
    :key="paperIndex"
    class="card mb-3 shadow-sm me-3"
    style="width: 30%;"
  >
                <div class="card-body text-start">
                  <div class="d-flex justify-content-between" 
                    @click="openBookmarkModal(paper, keywordItem.generatedKeyword.split('[')[0])">
                    <p class="text-truncate-2 " >{{ paper.title }}</p>
                    
                    <img :src="paper.bookmarked ? BookmarkIcon : UnbookmarkIcon" 
                    
                    style="width: 25px; height: 30px;"/>
                    

                  </div>


                  <!-- <p
                  @click="requestPaperByDoi(paper.paperDoi)"
                style="cursor: pointer; font-size: 4px;"
                title="해당 논문 자세히 보기 ">
                    {{
                      paper.korAbstract.length > 250
                        ? paper.korAbstract.slice(0, 250) + '...'
                        : paper.korAbstract
                    }}
                  </p> -->
                  <p class="text-truncate-mul"
                  @click="requestPaperByDoi(paper.paperDoi)"
                style="cursor: pointer; font-size: 12px;"
                title="해당 논문 자세히 보기 ">
                    {{
                      paper.engAbstract
                    }}
                  </p>
<!-- 북마킹 확인 모달 -->
<div
      v-if="isBookmarkModalVisible"
      class="bookmark-overlay"
    >
      <div class="bookmark-content">
        <div v-if="selectedBookmark.bookmarked===true">
          
        <strong class="text-truncate-1"
        style="font-size: 15px;color: black;">{{ selectedBookmark.title }}</strong>
        <br><p style="font-size: 13px; color: black;">논문을 정말로 북마크에서 <span style="font-size: 18px;color:#a04747;font-weight:bold ">삭제</span>
          하시겠습니까?</p>
        

        </div>

        <div v-else>
          
          <strong class="text-truncate-1"
        style="font-size: 15px;color: black;">{{ selectedBookmark.title }}</strong>
        <br><p style="font-size: 13px;color: black;">논문을 정말로 북마크에 <span style="font-size: 18px;color:#a04747;font-weight:bold ">등록</span>
          하시겠습니까?</p>

        </div>
        



        <div class="bookmarkbutton-group">
          <div class="left-content" @click="closeBookmarkModal"
          >
      아니요
    </div>

    <div class="right-content" @click="Bookmarking(selectedKeyword, selectedBookmark.paperDoi, selectedBookmark.bookmarked)">
      네 
    </div>


        </div>
      </div>
    </div>



                </div>
              </div>
            </div>
          </div>

          </div>
          


        </div>



        


      </div>











    </div>
  </div>
</template>




<style scoped>
.main-container {

  display: flex;
  flex-grow: 1;
  align-items: center; /* 수직 가운데 정렬 */
  justify-content: center; /* 수평 가운데 정렬 */
  margin-top: -15px;
}

.test-content {
  flex-grow: 1;
  margin: auto;
  width: 100%; /* 좌우로 꽉 차게 설정 */
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



.bookmark-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .bookmark-content {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    width: 300px;
  }
  
.bookmarkbutton-group {
  display: flex;
  justify-content: center;
  margin-top: 15px;
  align-items: center;
  height: 100%;
  border-top: 1px solid #eba2a2;
  
}

.left-content, .right-content {
  flex: 1; /* 콘텐츠 영역 동등 배분 */
  text-align: center; /* 텍스트 가운데 정렬 */
  padding: 3px;
  color: #a04747;
  background-color: #f8f9fa;

}
.left-content:hover, .right-content:hover {

  color: #f8f9fa;
  background-color: #a04747;

}

.left-content {
  border-right: 0.5px solid #eba2a2;
}

.right-content {
  border-left: 0.5px solid #eba2a2;
}




.bookmarked-icon {
  width: 40px;
  transition: fill 0.3s ease; /* 부드러운 전환 효과 */
  fill: brightness(0) saturate(100%) invert(50%) sepia(100%) saturate(200%) hue-rotate(90deg) brightness(90%) contrast(100%);
}

.bookmarked-icon:hover {
  filter:none;
}

.bookmark-icon {
  width: 40px;
  transition: filter 0.3s ease; /* 부드러운 전환 효과 */
  filter: brightness(0) saturate(100%) invert(100%) sepia(0) saturate(0%) hue-rotate(0deg) brightness(100%) contrast(100%);
  border: 2px solid #ff5733 !important; /* 원하는 테두리 색상 설정 */
}

.bookmark-icon:hover {
  filter:brightness(0) saturate(100%) invert(50%) sepia(100%) saturate(200%) hue-rotate(90deg) brightness(90%) contrast(100%);

}


.main-container {

  display: flex;
  align-items: center; /* 수직 가운데 정렬 */
  justify-content: center; /* 수평 가운데 정렬 */
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

.card {
  display: flex;
  align-items: center; /* 카드 내부 내용의 세로 정렬 */
  justify-content: center; /* 카드 내부 내용의 가로 정렬 */

  border: 2px solid #a04747;
}
.results-container {
  max-height: 65vh; /* 최대 높이 설정 */
  overflow-y: auto; /* 수직 스크롤 추가 */
  display: flex;
  flex-direction: column; /* 세로 방향 */
  height: 100%; /* 부모 컨테이너가 높이를 갖도록 설정 */
}
.results-container::-webkit-scrollbar {
  width: 8px; /* 스크롤 바의 너비 */
}

.results-container::-webkit-scrollbar-thumb {
  background-color: #da7e7e; /* 스크롤 바의 색상 (부트스트랩 기본색) */
  border-radius: 4px; /* 스크롤 바의 모서리 둥글기 */
}

.results-container::-webkit-scrollbar-thumb:hover {
  background-color: #8a9cce; /* 스크롤 바 호버 시 색상 */
}

.results-container::-webkit-scrollbar-track {
  background-color: #f8f9fa; /* 스크롤 바 트랙의 배경색 */
}

.text-truncate-2 {
    display: -webkit-box; /* Flexbox 사용을 위해 설정 */
    -webkit-line-clamp: 2; /* 표시할 최대 줄 수 */
    -webkit-box-orient: vertical; /* 수직 방향으로 박스 정렬 */
    overflow: hidden; /* 넘치는 내용 숨기기 */
    text-overflow: ellipsis; /* 생략 표시(...) */
    font-weight: bold;
    max-width: 80%;
  }
  .text-truncate-1 {
    display: -webkit-box; /* Flexbox 사용을 위해 설정 */
    -webkit-line-clamp: 1; /* 표시할 최대 줄 수 */
    -webkit-box-orient: vertical; /* 수직 방향으로 박스 정렬 */
    overflow: hidden; /* 넘치는 내용 숨기기 */
    text-overflow: ellipsis; /* 생략 표시(...) */
    font-weight: bold;
    
  }
  .text-truncate-mul {
    display: -webkit-box; /* Flexbox 사용을 위해 설정 */
    -webkit-line-clamp: 10; /* 표시할 최대 줄 수 */
    -webkit-box-orient: vertical; /* 수직 방향으로 박스 정렬 */
    overflow: hidden; /* 넘치는 내용 숨기기 */
    text-overflow: ellipsis; /* 생략 표시(...) */
    font-weight: bold;
    
  }

.intro-text {
  margin-top: 20px;
  
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
  padding: 10px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 300px;
  height: 120px;
  display: flex;
  flex-direction: column; /* 수직 방향으로 정렬 */
  justify-content: space-between; /* 위-아래 간격 분배 */
  position: relative; /* 자식 요소의 위치 설정 */
  border: 5px solid #a04747;
}

.error-message {
  position: absolute;
  top: 8px; /* 상단 여백 */
  left: 8px; /* 좌측 여백 */
  margin: 0; /* 기본 여백 제거 */
}

.modal-content-button {
  position: absolute;
  bottom: 8px; /* 하단 여백 */
  right: 8px; /* 우측 여백 */
  background-color: white;
  color: #a04747;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  padding: 5px 10px;
}

.modal-content-button:hover {
  background-color: #a04747;
  color: white;
}
.error-message {
  white-space: pre-line; /* \n을 줄바꿈으로 인식 */
  text-align: left;
}
.copy-message {
  background-color: #a04747;
  font-size: 14px;
  margin: 20px;
  color: white;
}

.text-muted {
  color : #8A8A8A;
  font-size: 20px;
}



</style>
