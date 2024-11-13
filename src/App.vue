<template>
  <div id="app">
    <Header />
    <main>
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
</script>

<style scoped>
#app {
  font-family: Arial, sans-serif;
  text-align: center;
  padding: 0px;
}

html,
body {
  overflow-x: hidden; /* 좌우 스크롤 제거 */
  margin: 0;
  padding: 0;
  width: 100%;
  box-sizing: border-box; /* 박스 크기 조정 */
}
</style>
