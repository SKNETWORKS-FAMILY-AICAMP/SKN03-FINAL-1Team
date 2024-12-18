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
    <router-link
      :to="{ path: '/papers/detail/', query: { paperDoi: paper.paperDoi } }"
      class="text-start"
      style="text-decoration: none; color: inherit"
    >
      <div>
        <h5>{{ paper.title }}</h5>
        <p class="my-1 author">
          {{ paper.publication_month }} {{ paper.publication_year }} | {{ paper.authors }}
        </p>
        <p class="no-margin">DOI: {{ paper.paperDoi }}</p>
        <p class="no-margin abstract">Abstract: {{ paper.kor_abstract }}</p>
      </div>
    </router-link>
  </div>
</template>

<style scoped>
.no-margin {
  margin: 0;
}
.abstract {
  display: -webkit-box; /* Flexbox 기반 표시 */
  -webkit-line-clamp: 2; /* 표시할 최대 줄 수 (여기서는 3줄) */
  -webkit-box-orient: vertical; /* 세로 방향 정렬 */
  overflow: hidden; /* 넘치는 부분 감춤 */
  text-overflow: ellipsis; /* '...' 표시 */
}

.author {
  display: -webkit-box; /* Flexbox 기반 표시 */
  -webkit-line-clamp: 1; /* 표시할 최대 줄 수 (여기서는 3줄) */
  -webkit-box-orient: vertical; /* 세로 방향 정렬 */
  overflow: hidden; /* 넘치는 부분 감춤 */
  text-overflow: ellipsis; /* '...' 표시 */
}
</style>
