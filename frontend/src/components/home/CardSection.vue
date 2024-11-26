<script setup></script>

<template>
  <div class="container">
    <div class="row custom-row mt-5 mx-3 d-flex text-start">
      <div class="col-md-4 d-flex">
        <div class="card bg-white flex-fill">
          <div class="card-body d-flex flex-column mx-2 mt-2">
            <h2 class="card-title fw-bold text-start">기술 상담</h2>
            <p class="card-text flex-grow-1">
              내 요구사항에 어떤 세부 기능을 넣어야 할지 알아보자고 챗봇과 함께 세부 기능을
              정의해보아요.
            </p>
            <a href="#" class="card-btn btn mt-auto">기술 상담 기능 ></a>
          </div>
        </div>
      </div>
      <div class="col-md-4 d-flex">
        <div class="card bg-white flex-fill">
          <div class="card-body d-flex flex-column mx-2 mt-2">
            <h2 class="card-title fw-bold text-start">논문 검색</h2>
            <p class="card-text flex-grow-1">
              키워드에 맞는, 내게 필요한 논문을 찾고 싶다면? 키워드 검색을 통해 내게 필요한 논문을
              빠르게 찾아보아요.
            </p>
            <a href="/main" class="card-btn btn mt-auto">논문 검색 기능 ></a>
          </div>
        </div>
      </div>
      <div class="col-md-4 d-flex">
        <div class="card bg-white flex-fill">
          <div class="card-body d-flex flex-column mx-2 mt-2">
            <h2 class="card-title fw-bold text-start">논문 파악</h2>
            <p class="card-text flex-grow-1">
              방법론을 활용하기 위해 내게 필요한 부분이 어딘지 알아보자고 챗봇과 함께 논문을
              이해하고, 내게 맞게 구현해보아요.
            </p>
            <a href="#" class="card-btn btn mt-auto">논문 파악 기능 ></a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card-btn {
  color: #a04747;
  font-weight: bold;
}
</style>
