<script setup></script>

<template>
  <div class="book-mark d-flex flex-column">
    <div class="bookmark-list mt-5 text-start">북마크 리스트</div>
    <div class="content my-2">10.18653/v1/2020.acl-demos.10</div>
    <div class="content my-2">뭔가 자연어 처리에 관한 서비스를 만들고 싶어!</div>
  </div>
</template>

<style scoped>
.book-mark {
  flex-grow: 1;
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
</style>
