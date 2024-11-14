<script setup>
import { useRouter } from 'vue-router'
import logo from '@/assets/home-logo.png'
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
          <img :src="logo" alt="Logo" class="logo mb-3" @click="goToHomePage" />
          <div class="bookmark-list">북마크 리스트</div>
        </div>
        <div class="footer mt-auto">
          <button class="btn view-button">논문내용보기-></button>
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

.bookmark-list::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 50%;
  height: 1px;
  background-color: white; /* 상단 테두리 색상 */
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

.logo {
  max-width: 90%;
  object-fit: contain;
  margin: 0;
  padding: 0;
  cursor: pointer; /* 클릭 가능한 커서 추가 */
}

.footer {
  width: 100%;
  display: flex;
  justify-content: center;
}

.view-button {
  color: #ffffff;
  border: 1px solid white;
  width: 88%;
  margin-bottom: 100px; /* 하단 여백 추가 */
}
</style>
