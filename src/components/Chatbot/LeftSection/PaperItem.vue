<script setup>
import DragHandleIcon from '@/assets/DragHandleIcon.png'
import BookMarkIcon from '@/assets/BookMarkIcon.png'
</script>

<template>
  <div class="paper-item d-flex align-items-center my-2">
    <div>
      <img :src="DragHandleIcon" />
    </div>
    <div class="text-start">
      <p>논문명</p>
      <p>텍스트-이미지 생성</p>
    </div>
    <div>
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
}
.paper-item p {
  line-height: 0.7;
}
</style>
