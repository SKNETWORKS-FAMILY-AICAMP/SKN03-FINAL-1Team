<script setup>
import BookMarkIcon from '@/assets/BookMarkIcon.png'
</script>
<template>
  <div class="d-flex align-items-center">
    <div class="p-4">
      <img :src="BookMarkIcon" />
      <div>
        <h2>75%</h2>
      </div>
    </div>
    <div class="text-start">
      <h5>Hierarchical Text-ConditionalImage Generation with CLIP Latents</h5>
      <p class="my-1">대충 날짜 | 대충 저자</p>
      <p class="no-margin">키워드 : 어쩌구</p>
      <p class="no-margin">핵심 방법론 : 어쩌구저쩌구</p>
    </div>
  </div>
</template>
<style scoped>
.no-margin {
  margin: 0;
}
</style>
