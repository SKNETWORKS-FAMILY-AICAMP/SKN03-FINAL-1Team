<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router'; // Vue Router에서 useRoute를 가져옵니다.
import axios from '@/axiosConfig'; // 설정한 axios 인스턴스를 가져옵니다.
import closeIcon from '@/assets/upbtn.png';
import openIcon from '@/assets/downbtn.png';

const papers = ref([]);
const route = useRoute(); // 현재 라우트 정보를 가져옵니다.
const warnFlag = ref(false);

const router = useRouter()

const requestPaperByDoi = async (paperDoi) => {

//window.location.href = `${HOME_URL}papers/detail/?paperDoi=${paperDoi}`;
router.push({
      path: '/papers/detail/',
      query: { paperDoi },
    }).then(() => {
      window.location.reload();
    });
}

// 데이터 가져오기
const fetchPriorPapers = async () => {
  warnFlag.value = false;
  try {
    const paperDoi = route.query.paperDoi; // 기본 DOI 값을 사용합니다.
    const response = await axios.get('/papers/priorpapers/', {
      params: {
        paperDoi: paperDoi,
      },
    });
    if (response.data.resultCode === 200) {
      // 각 항목에 `isOpen` 상태 추가
      papers.value = response.data.result.paperList.map((paper) => ({
        ...paper,
        isOpen: false, // 초기 상태는 닫힘
      }));
      console.log('papers: ', papers);
    }
  } catch (error) {
    if (error.response && error.response.data) {
      const { resultCode, message } = error.response.data;
      if (resultCode === 404) {
        warnFlag.value = true;
        console.log(message);
      }
    }
  }
};

const toggleOpen = (paper) => {
  paper.isOpen = !paper.isOpen; // 해당 항목의 상태만 변경
};

onMounted(() => {
  fetchPriorPapers();
});
</script>


<template>
  <div class="bookmark-container flex-column">
    <div class="bookmark-list mt-5 mb-3 text-start">선행 논문 추천</div>
    <ul
      v-if="papers"
      class="list-group text-start overflow-auto summary-detail-container"
    >
      <li
        v-for="paper in papers"
        :key="paper.paperDoi"
        class="list-group-item text-start my-2 rounded-4 p-3"
        style="margin-right: 5px;"
      >
        <div class="d-flex justify-content-between align-items-center">
          <!-- Progress Circle -->
          <div
            class="progress-circle"
            :style="{
              background: `conic-gradient(#a04747 0% ${paper.similarity}%, lightgray ${paper.similarity}% 100%)`,
            }"
          >
            <span>{{ paper.similarity }}%</span>
          </div>

          <!-- Title -->
          <strong
            class="text-truncate-1 my-2"
            
            >{{ paper.title }}</strong
          >

          <!-- Toggle Button -->
          <div 
          >
            <img
            :src="paper.isOpen ? closeIcon : openIcon"
            @click="toggleOpen(paper)"
            class="toggle-img"
            
          />

          </div>
        </div>

        <!-- Toggle Content -->
        <div v-if="paper.isOpen" class="toggle-content mt-3">
          <div 
          @click="requestPaperByDoi(paper.paperDoi)"
          >
            <p><span style="color: #a04747; font-weight: bold;">키워드:</span><br> {{ paper.Keyword }}</p>
          <p><span style="color: #a04747; font-weight: bold;">핵심 방법론:</span> <br>{{ paper.coreMethod }}</p>
          <p><span style="color: #a04747; font-weight: bold;">유사 부분 요약:</span> <br>{{ paper.Summary }}</p>

          </div>
        </div>
      </li>
    </ul>

    <div
      v-if="warnFlag"
      class="d-flex flex-column align-items-center justify-content-center"
      style="flex-grow: 1;"
    >
      <strong>
        Documento에서 지원하는 선행논문이 <br />
        존재하지 않는 논문입니다 <br />
      </strong>

      <strong>
        <br />키워드 최적화 및 논문 검색 과정을 통해 <br />논문을 검색해보세요 :)
      </strong>
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


.toggle-container {
  border: 1px solid #ccc;
  padding: 10px;
  max-width: 500px;
  margin: 20px auto;
  text-align: center;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.toggle-img {
  width: 10px; /* 아이콘 크기 조정 */
  height: 10px;
  cursor: pointer;
  transition: transform 0.3s ease; /* 클릭 시 애니메이션 */
}

.toggle-img:hover {
  transform: scale(1.1); /* 호버 시 확대 효과 */
}

.toggle-content {
  margin-top: 20px;
  text-align: left;
}

.text-truncate-1 {
    display: -webkit-box; /* Flexbox 사용을 위해 설정 */
    -webkit-line-clamp: 1; /* 표시할 최대 줄 수 */
    -webkit-box-orient: vertical; /* 수직 방향으로 박스 정렬 */
    overflow: hidden; /* 넘치는 내용 숨기기 */
    text-overflow: ellipsis; /* 생략 표시(...) */
    max-width: 75%;
    
  }

.progress-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75em;
  color: #a04747;
}

.progress-circle::before {
  content: '';
  position: absolute;
  width: 85%;
  height: 85%;
  background-color: white;
  border-radius: 50%;
  z-index: 1;
}

.progress-circle span {
  z-index: 2;
}

.warning-image {
  filter: brightness(0) saturate(100%) invert(75%) sepia(70%) saturate(500%) hue-rotate(1deg) brightness(95%) contrast(90%);
}

</style>
