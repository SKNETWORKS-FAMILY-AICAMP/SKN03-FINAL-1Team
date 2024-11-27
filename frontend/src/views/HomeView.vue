<script setup>
import Header from '@/components/Home/HomeHeader.vue'
import SearchSection from '@/components/Home/SearchSection.vue'
import CardSection from '@/components/Home/CardSection.vue'
import IntroSection from '@/components/Home/IntroSection.vue'
import Footer from '@/components/Home/HomeFooter.vue'
</script>

<template>
  <div>
    <Header />
    <search-section />
    <div class="card-intro-wrapper">
      <card-section />
      <intro-section />
    </div>
    <Footer />
  </div>
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

.card-intro-wrapper {
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}
</style>
