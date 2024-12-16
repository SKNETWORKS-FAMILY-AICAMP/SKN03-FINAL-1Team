<script setup></script>

<template>
  <div class="container">
    <div class="row custom-row mt-5 mx-3 d-flex text-start">
      <div v-for="(card, index) in cards" :key="index" class="col-md-4 d-flex p-2">
        <div class="card bg-white flex-fill">
          <div class="card-body d-flex flex-column mx-2 mt-2">
            <h4 class="card-title fw-bold text-start">{{ card.title }}</h4>
            <p class="card-text flex-grow-1">{{ card.text }}</p>
            <a :href="card.link" class="card-btn btn mt-auto">{{ card.buttonText }}</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const cards = [
  {
    title: '키워드 최적화',
    text: '논문 검색에 어려움이 있으신가요? 찾고 있는 논문을 편하게 입력해주세요!',
    link: '/main',
    buttonText: 'Keyword >',
  },
  {
    title: '논문 검색',
    text: '키워드에 맞는, 내게 필요한 논문을 찾고 싶다면? 키워드 검색을 통해 내게 필요한 논문을 빠르게 찾아보아요.',
    link: '/main',
    buttonText: 'Search >',
  },
  {
    title: '북마크',
    text: '북마크된 논문들을 보며 과거 진행한 리뷰를 톺아보아요. 관련 요약을 제공받거나 선행 논문들을 추천받을 수 있어요.',
    link: '/main',
    buttonText: 'Preview >',
  },
]
</script>

<style scoped>
.card-btn {
  color: #a04747;
  font-weight: bold;
}
</style>
