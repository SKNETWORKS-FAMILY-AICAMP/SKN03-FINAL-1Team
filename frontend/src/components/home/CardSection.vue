<script setup></script>

<template>
  <div class="container">
    <div class="row custom-row  mx-3 d-flex text-start"
    style="margin-top: -50px;">
      <div v-for="(card, index) in cards" :key="index" class="col-md-4 d-flex p-2">
        <div class="card flex-fill card-detail">
          <div class="card-body d-flex flex-column align-items-start "
          style="gap: 5px;">
            <div class="circle"><img :src="card.imgElement" :alt="card.title" width="20px" height="auto"/></div>
            <h4 class="card-title fw-bold text-start">{{ card.title }}</h4>
            <p class="card-text flex-grow-1"
            >{{ card.text }}</p>
            <a :href="card.link" class="card-btn btn ">{{ card.buttonText }}</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import homeboomark from '@/assets/homebookmark.png'
import homesearch from '@/assets/homesearch.png'
import hometrans from '@/assets/hometrans.png'

const cards = [
  {
    title: '키워드 최적화',
    text: '어떻게 검색해야 할지 헷갈리시나요? 챗봇과 함께 나만의 언어를 논문 검색의 키워드로 변환해보아요.',
    link: '/main',
    buttonText: 'Keyword >',
    imgElement: hometrans,
  },
  {
    title: '논문 검색',
    text: '키워드에 맞는, 내게 필요한 논문을 찾고싶다면? 키워드 검색을 통해 내게 필요한 논문을 빠르게 찾아보아요.',
    link: '/main',
    buttonText: 'Search >',
    imgElement: homesearch,
  },
  {
    title: '북마크',
    text: '북마크된 논문들을 보며 과거 진행한 리뷰를 톺아보아요. 관련 요약을 제공받거나 선행 논문들을 추천받을 수 있어요.',
    link: '/main',
    buttonText: 'Preview >',
    imgElement: homeboomark,
  },
]
</script>

<style scoped>
.card-btn {
  color: #a04747;
  font-weight: bold;
  
  padding: 0;
}


.card-detail{
  background-color: #E6DEDD;

}

.circle {
  width: 40px; /* 원의 너비 */
  height: 40px; /* 원의 높이 */
  background-color: #a04747; /* 원의 색상 */
  border-radius: 50%; /* 둥근 모서리를 만들어 원형으로 */
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
