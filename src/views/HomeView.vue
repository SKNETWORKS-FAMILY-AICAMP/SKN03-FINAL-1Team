<script setup>
import { ref } from 'vue'

const searchQuery = ref('')
</script>

<template>
  <div class="HomeView py-5">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8 text-center">
          <h2 class="text-light mb-4">
            어쩌구 저쩌구 어렵지 않으신가요?<br />키워드를 검색해보아요!!!
          </h2>
          <input
            v-model="searchQuery"
            class="form-control form-control-lg"
            placeholder="원하는 키워드를 입력해보세요."
          />
        </div>
      </div>
    </div>
  </div>

  <!-- 새로운 섹션 시작 -->
  <div class="row mt-5 mx-3">
    <div class="col-md-4">
      <div class="card bg-white">
        <div class="card-body">
          <h5 class="card-title">기술 상담</h5>
          <p class="card-text">
            내 요구사항에 어떤 세부 기능을 넣어야 할지 알아보자고 챗봇과 함께 세부 기능을
            정의해보아요.
          </p>
          <a href="#" class="btn btn-primary">기술 상담 기능 ></a>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card bg-white">
        <div class="card-body">
          <h5 class="card-title">논문 검색</h5>
          <p class="card-text">
            키워드에 맞는, 내게 필요한 논문을 찾고 싶다면? 키워드 검색을 통해 내게 필요한 논문을
            빠르게 찾아보아요.
          </p>
          <a href="#" class="btn btn-primary">논문 검색 기능 ></a>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card bg-white">
        <div class="card-body">
          <h5 class="card-title">논문 파악</h5>
          <p class="card-text">
            방법론을 활용하기 위해 내게 필요한 부분이 어딘지 알아보자고 챗봇과 함께 논문을 이해하고,
            내게 맞게 구현해보아요.
          </p>
          <a href="#" class="btn btn-primary">논문 파악 기능 ></a>
        </div>
      </div>
    </div>
  </div>
  <!-- 새로운 섹션 끝 -->
  <div class="container mt-3 mx-3">
    <div class="row">
      <div class="col-md-6">
        <div class="card bg-white">
          <div class="card-body">
            <p>
              인공지능은 빠르게 발전하는 분야이기 때문에 최신 연구와 기술을 파악하는 것이
              필수적입니다. 이때, 논문에서는 AI의 새로운 알고리즘, 데이터 처리 방법, 응용 분야 등이
              검증된 형식으로 소개됩니다. 그렇지만 인공지능 논문, 다가가기 어렵지 않으셨나요?
              인공지능 분야의 논문의 경우 전문 용어의 사용이 많고, 고도의 전문 지식을 요구하며, 밀도
              높은 정보와 복잡한 구조를 가지고 있기에 초기 접근의 벽이 높습니다. 저희 Documento는
              새내기 연구자를 위하여 접근의 벽을 허물고 간단한 인공지능 논문의 접근을 편리하게
              하고자 합니다.
            </p>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <img src="@/assets/home_image1.png" class="img-fluid" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.HomeView {
  background-color: #a04747;
  color: white;
  width: 100%;
  margin: 0;
  padding: 0 15px;
  padding-bottom: 80px;
  box-sizing: border-box;
}
</style>
