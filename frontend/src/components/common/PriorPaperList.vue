<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router' // Vue Router에서 useRoute를 가져옵니다.
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.
import warningImage from '@/assets/warning.svg'
const papers = ref([])
const route = useRoute() // 현재 라우트 정보를 가져옵니다.
const warnFlag = ref(false)

const fetchPriorPapers = async () => {
  warnFlag.value = false
  try {
    const paperDoi = route.query.paperDoi  // 기본 DOI 값을 사용합니다.
    const response = await axios.get('/papers/priorpapers/', {
      params: {
        paperDoi: paperDoi,
      },
    })
    if (response.data.resultCode === 200) {
      papers.value = response.data.result.paperList
      console.log("papers: ", papers)
    }
  } catch (error) {
    if (error.response && error.response.data) {
    const { resultCode, message} = error.response.data
    if (resultCode === 404) {
      warnFlag.value = true
    console.log(message)
    }
    
}
  }
}

onMounted(() => {
  fetchPriorPapers()
})
</script>

<template>
  <div class="prior-paper-container flex-column">
    <div class="prior-paper-list mt-5 text-start">선행 논문 추천</div>
    <ul v-if="papers"  class="list-group">
      <li
        v-for="paper in papers"
        :key="paper.paperDoi"
        class="list-group-item text-start my-2 rounded-4"
      >
        <div class="row">
          <div class="col-auto mt-2">
            <div
              class="progress-circle"
              :style="{
                background: `conic-gradient(#a04747 0% ${paper.similarity}%, lightgray ${paper.similarity}% 100%)`,
              }"
            >
              <span>{{ paper.similarity }}%</span>
            </div>
          </div>
          <div class="col mt-2">
            <strong class="fst-italic">{{ paper.title }}</strong>
            <p>{{ paper.generatedKeyword }}</p>
          </div>
        </div>
      </li>
    </ul>
    <div v-if="warnFlag" >
      <img
      :src="warningImage"
      alt="warning"
      width=80%
      class="warning-image"
    />

    <p>해당 논문의 선행 논문 추천은 준비중 입니다</p>
    <p>이는 추후 없데이트 예정입니다</p> 


    </div>


  </div>
</template>

<style scoped>
.prior-paper-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.prior-paper-list {
  position: relative;
  margin-top: 20px;
  padding: 10px 0;
  font-size: 20px;
  color: white;
}

.prior-paper-list::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background-color: white;
}

.progress-circle {
  width: 50px;
  height: 50px;
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
