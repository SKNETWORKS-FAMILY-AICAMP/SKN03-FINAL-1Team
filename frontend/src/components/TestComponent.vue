<script setup>
import { ref, onMounted } from 'vue'

const pdfUrl =
  'https://documento-s3.s3.amazonaws.com/papers/emnlp/2023/10.18653_v1_2023.emnlp-main.516.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIASVLKB6UWYEEFQN7O%2F20241205%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20241205T082624Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=e0fc90d2912ab211ced540fa7f0373504b14511eabf2db6c5145d05c7462919e'

const pdfFile = ref(null)

const fetchAndOpenPdf = async (url) => {
  try {
    const response = await fetch(url)
    const blob = await response.blob()
    pdfFile.value = URL.createObjectURL(blob)
    window.open(pdfFile.value)
  } catch (error) {
    console.error('Error fetching PDF:', error)
  }
}

onMounted(() => {
  fetchAndOpenPdf(pdfUrl)
})
</script>

<template>
  <div>
    <p v-if="pdfFile">PDF 파일을 다운로드하고 있습니다...</p>
  </div>
</template>
