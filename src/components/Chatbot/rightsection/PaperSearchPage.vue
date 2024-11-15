<script setup>
const papers = ref([
  {
    title: 'Hierarchical Text-Conditional Image Generation with CLIP Latents',
    authors: 'By Aditya Ramesh, Prafulla Dhariwal, Alex Nichol, Casey Chu, Mark Chen',
    date: 'January, 2022',
    relevance: '75%',
    keywords: '텍스트-이미지 생성 (Text to Image generation)',
    methods:
      'Diffusion Model과 CLIP (Contrastive Language-Image Pre-training) 두 가지 기술을 결합하여 텍스트에서 이미지를 생성할 수 있다.',
  },
  // 다른 논문도 동일한 형식으로 추가할 수 있습니다.
])
</script>

<template>
  <div class="paper-search-page">
    <h2>논문 탐색</h2>
    <div class="search-bar">
      <input type="text" placeholder="검색 키워드를 입력해보세요." />
      <button>🔍</button>
    </div>
    <div v-for="(paper, index) in papers" :key="index" class="paper-entry">
      <div class="relevance-score">{{ paper.relevance }}</div>
      <div class="paper-details">
        <h3>{{ paper.title }}</h3>
        <p>{{ paper.date }} • {{ paper.authors }}</p>
        <p><strong>키워드:</strong> {{ paper.keywords }}</p>
        <p><strong>핵심 방법론:</strong> {{ paper.methods }}</p>
      </div>
    </div>
    <div class="pagination">
      <span>1</span> <span>*</span> <span>2</span> <span>*</span> <span>3</span> <span>&gt;</span>
    </div>
  </div>
</template>

<style scoped>
.paper-search-page {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.search-bar {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar input {
  padding: 10px;
  font-size: 16px;
  margin-right: 10px;
}

.search-bar button {
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
}

.paper-entry {
  width: 80%;
  border-bottom: 1px solid #ccc;
  padding: 20px 0;
  display: flex;
  align-items: flex-start;
}

.relevance-score {
  font-size: 24px;
  color: red;
  margin-right: 20px;
}

.paper-details {
  flex: 1;
}

.paper-details h3 {
  margin: 0;
  font-size: 18px;
}

.paper-details p {
  margin: 5px 0;
}

.pagination {
  margin-top: 20px;
}

.pagination span {
  margin: 0 5px;
  cursor: pointer;
}
</style>
