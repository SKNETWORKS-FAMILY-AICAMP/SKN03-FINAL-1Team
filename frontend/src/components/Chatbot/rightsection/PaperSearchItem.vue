<script setup>
import BookMarkIcon from '@/assets/BookMarkIcon.png'
import { defineProps } from 'vue'

// props 정의
const props = defineProps({
  paper: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <div class="d-flex align-items-center">
    <div class="p-4">
      <img :src="BookMarkIcon" />
      <div>
        <h2>{{ paper.citation }} Citations</h2>
      </div>
    </div>
    <div class="text-start">
      <h5>{{ paper.title }}</h5>
      <p class="my-1">
        {{ paper.publicationMonth }} {{ paper.publicationYear }} | {{ paper.authors }}
      </p>
      <p class="no-margin">DOI: {{ paper.paperDoi }}</p>
      <p class="no-margin">Abstract: {{ paper.abstract }}</p>
    </div>
  </div>
</template>

<style scoped>
.no-margin {
  margin: 0;
}
</style>
