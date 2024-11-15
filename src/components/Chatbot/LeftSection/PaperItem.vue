<script setup>
import DragHandleIcon from '@/assets/DragHandleIcon.png'
import BookMarkIcon from '@/assets/BookMarkIcon.png'
</script>

<template>
  <div class="paper-item d-flex align-items-center my-2">
    <div class="p-3">
      <img :src="DragHandleIcon" />
    </div>
    <div class="text-start flex-grow-1 d-flex flex-column">
      <p>논문명</p>
      <p>텍스트-이미지 생성</p>
    </div>
    <div class="ms-auto p-4">
      <img :src="BookMarkIcon" />
    </div>
  </div>
</template>

<style scoped>
.paper-item {
  background: white;
  color: black;
  border-radius: 10px;
  margin: 5px;
  padding: 0px;
  height: 75px;
}
.paper-item p {
  line-height: 0.7;
  margin-top: 5px;
  margin-bottom: 5px;
}
</style>
