<script setup>
import { ref } from 'vue'
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.

const papers = ref([])

const fetchPriorPapers = async () => {
  try {
    const response = await axios.get('/papers/priorpapers/', {
      params: {
        paperDoi: '10.18653/v1/2020.acl-demos.10',
      },
    })
    if (response.data.resultCode === 201 && response.data.result.paperList) {
      papers.value = response.data.result.paperList
    }
  } catch (error) {
    console.error('선행 논문을 가져오는 중 오류 발생:', error)
  }
}
</script>

<template>
  <div class="container mt-4">
    <h2>선행 논문 목록</h2>
    <button class="btn btn-primary mb-3" @click="fetchPriorPapers">선행 논문 불러오기</button>
    <ul class="list-group">
      <li
        v-for="paper in papers"
        :key="paper.paperDoi"
        class="list-group-item d-flex justify-content-between align-items-center"
      >
        <strong>{{ paper.title }}</strong
        ><br />
        <span class="badge bg-secondary">{{ paper.similarity }}</span>
        <p>{{ paper.generatedKeyword }}</p>
      </li>
    </ul>
  </div>
</template>

<style scoped>
/* 추가적인 스타일을 여기에 작성할 수 있습니다 */
</style>
