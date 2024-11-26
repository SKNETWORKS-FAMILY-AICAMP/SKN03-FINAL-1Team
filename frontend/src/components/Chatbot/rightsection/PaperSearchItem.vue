<template>
  <div class="paper-item">
    <h3>{{ paper.title }}</h3>
    <p><strong>DOI:</strong> {{ paper.paperDoi }}</p>
    <p><strong>Authors:</strong> {{ paper.authors }}</p>
    <p><strong>Publication Year:</strong> {{ paper.publicationYear }}</p>
    <p><strong>Publication Month:</strong> {{ paper.publicationMonth }}</p>
    <p><strong>Abstract:</strong> {{ paper.abstract }}</p>
    <p><strong>Citations:</strong> {{ paper.citation }}</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  paper: {
    type: Object,
    required: true,
  },
})
</script>

<style scoped>
.paper-item {
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 10px;
}
</style>
