<script setup>
const props = defineProps({
  src: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div class="pdf-container">
    <embed :src="src" class="pdf-viewer" type="application/pdf" />
  </div>
</template>

<style scoped>
.pdf-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 70vw;
  height: 100vh;
  overflow: hidden;
}

.pdf-viewer {
  width: 100%;
  height: 100%;
}
</style>
