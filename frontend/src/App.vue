<script setup></script>

<template>
  <div id="app">
    <main>
      <router-view />
    </main>
  </div>
</template>

<style scoped>
/* @import '@/assets/font/Pretendard.css'; */

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
