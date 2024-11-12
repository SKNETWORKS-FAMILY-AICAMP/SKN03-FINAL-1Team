<script setup>
import { ref } from 'vue'

const searchQuery = ref('')
</script>

<template>
  <div class="HomeView">
    <h2>어쩌구 저쩌구 어렵지 않으신가요?<br />키워드를 검색해보아요!!!</h2>
    <input v-model="searchQuery" class="search-input" placeholder="원하는 키워드를 입력해보세요." />
  </div>
</template>

<style scoped>
.HomeView {
  background-color: #a04747;
  text-align: left;
  color: white;
}
</style>
