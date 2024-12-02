<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const papers = ref([])

const fetchPriorPapers = async () => {
  try {
    const response = await axios.get('/papers/priorpapers/', {
      params: {
        paperDoi: '10.18653/v1/2020.acl-demos.10',
      },
    })
    if (response.data.result && response.data.result.paperList) {
      papers.value = response.data.result.paperList
    }
  } catch (error) {
    console.error('선행 논문을 가져오는 중 오류 발생:', error)
  }
}

onMounted(fetchPriorPapers)
</script>

<template>
  <div>
    <h2>선행 논문 목록</h2>
    <ul>
      <li v-for="paper in papers" :key="paper.paperDoi">
        {{ paper.title }} (유사도: {{ paper.similarity }})
      </li>
    </ul>
  </div>
</template>

<style scoped>
/* 스타일을 여기에 추가할 수 있습니다 */
</style>
