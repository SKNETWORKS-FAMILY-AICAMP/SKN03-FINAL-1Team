<template>
  <div class="book-mark d-flex flex-column">
    <div class="bookmark-list mt-5 text-start">북마크 리스트</div>
    <div class="content my-2"></div>
  </div>
</template>

<script setup>
// 필요에 따라 스크립트 로직을 추가하세요.
</script>

<style scoped>
.book-mark {
  flex-grow: 1; /* 남은 공간을 차지하도록 설정 */
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.bookmark-list {
  position: relative;
  margin-top: 20px;
  padding: 10px 0;
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

.content {
  /* 추가 스타일이 필요하면 여기에 작성하세요 */
}
</style>
