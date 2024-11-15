<script setup>
import { useRouter } from 'vue-router'
import IconBar from '@/components/Chatbot/IconBar/IconBarMain.vue'
const router = useRouter()

const goToHomePage = () => {
  router.push('/') // 홈페이지 경로로 이동
}
</script>

<template>
  <div class="container m-0 p-0 h-100">
    <div class="left-side-content d-flex flex-row">
      <icon-bar />
      <div class="book-mark d-flex flex-column">
        <div class="content mx-3 my-3">
          <div class="bookmark-list mt-5">북마크 리스트</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  height: 100vh;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: row;
}

.left-side-content {
  display: flex;
  flex-direction: row; /* 가로 정렬 */
  background-color: #a04747;
  width: 100%;
  height: 100%;
  color: #ffffff;
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
  box-shadow: 2px 0px 10px 4px #515151; /* 섀도우 속성 추가 */
  margin-right: 20px;
}

.icon-bar {
  width: 80px;
  height: 100vh;
  border-top-right-radius: 20px;
  border-bottom-right-radius: 20px;
}

.book-mark {
  flex-grow: 1; /* 남은 공간을 차지하도록 설정 */
  display: flex;
  flex-direction: column;
}

.bookmark-list {
  position: relative;
  margin-top: 20px;
  padding: 10px 0;
}

.bookmark-list::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background-color: white; /* 하단 테두리 색상 */
}
</style>
