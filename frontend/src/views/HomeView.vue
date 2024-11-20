<script setup>
import Header from '@/components/home/HomeHeader.vue'
import SearchSection from '@/components/home/SearchSection.vue'
import CardSection from '@/components/home/CardSection.vue'
import IntroSection from '@/components/home/IntroSection.vue'
import Footer from '@/components/home/HomeFooter.vue'
</script>

<template>
  <Header />
  <search-section />
  <div class="signup-link"><router-link to="/signup">회원가입</router-link></div>
  <card-section />
  <intro-section />
  <Footer />
</template>

<style scoped>
.HomeView {
  background-color: #a04747;
  color: white;
  width: 100%;
  margin: 0;
  padding: 0 15px;
  padding-bottom: 80px;
  box-sizing: border-box;
}

/* 커스텀 행 스타일 */
.custom-row {
  max-width: 900px; /* 최대 너비 설정 */
  margin-left: auto; /* 좌우 여백 설정 */
  margin-right: auto; /* 좌우 여백 설정 */
}

/* 반응형 스타일 */
@media (max-width: 900px) {
  .custom-row {
    max-width: 100%; /* 화면 크기가 작아질 때 최대 너비를 100%로 설정 */
  }
}

/* 이미지 크기 고정 */
.img-fluid {
  max-width: 100%;
  height: auto;
  max-height: 300px;
}
</style>
