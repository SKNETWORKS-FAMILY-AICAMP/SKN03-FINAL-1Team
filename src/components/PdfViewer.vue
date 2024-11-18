<template>
  <div class="pdf-container">
    <embed :src="pdfUrl" class="pdf-viewer" type="application/pdf" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import dummyPdf from '@/assets/dummy.pdf'

const pdfUrl = computed(() => dummyPdf)
</script>

<style scoped>
.pdf-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 70vw; /* Viewport 너비 */
  height: 100vh; /* Viewport 높이 */
  overflow: hidden; /* 필요 시 스크롤 숨김 */
}

.pdf-viewer {
  width: 100%;
  height: 100%;
}
</style>
