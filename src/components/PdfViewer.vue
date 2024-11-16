<template>
  <div>
    <embed :src="pdfUrl" width="600" height="400" type="application/pdf" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import dummyPdf from '@/assets/dummy.pdf'

const pdfUrl = computed(() => dummyPdf)
</script>
