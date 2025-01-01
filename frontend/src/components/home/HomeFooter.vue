<script setup></script>

<template>
  <footer>
    <!-- 새로운 섹션 시작! -->
    <div class="container">
      <div class="count-box-container row mt-5 mx-3">
        <div class="count-box col-md-4 my-3">
          <div class="card">
            <div class="card-body">
              <h1 class="card-title">7550</h1>
              <p class="card-text">총 논문 수</p>
            </div>
          </div>
        </div>
        <div class="count-box col-md-4 my-3">
          <div class="card">
            <div class="card-body">
              <h1 class="card-title">113272</h1>
              <p class="card-text">총 페이지 수</p>
            </div>
          </div>
        </div>
        <div class="count-box col-md-4 my-3">
          <div class="card bg-white">
            <div class="card-body">
              <h1 class="card-title">234</h1>
              <p class="card-text">누적 방문자 수</p>
            </div>
          </div>
        </div>
      </div>
      <div class="footer-columns">
        <div class="footer-column">
          <h3>출처</h3>
          <a href="https://aclanthology.org/" target="_blank" rel="noopener noreferrer"  class="custom-link">ACL Anthology </a>
        </div>
        <div class="footer-column">
          <h3>깃허브</h3>
          <a href="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN03-FINAL-1Team" target="_blank" rel="noopener noreferrer"  class="custom-link">Documento github</a>
        </div>
        <div class="footer-column">
          <h3>개발자</h3>
          <p><a href="https://github.com/seom-j" target="_blank" rel="noopener noreferrer"  class="custom-link">서민정</a> | <a href="https://github.com/JinYunhwa" target="_blank" rel="noopener noreferrer"  class="custom-link">진윤화</a> | <a href="https://github.com/zelope" target="_blank" rel="noopener noreferrer"  class="custom-link">이준경</a> | <a href="https://github.com/WhiteNBlackTiger" target="_blank" rel="noopener noreferrer"  class="custom-link">박규택</a></p>
          
        </div>
      </div>
      <div class="footer-info d-flex justify-content-center align-items-center">
        <img src="@/assets/logo-white.png" alt="DocuMento logo" width="200" class="logo-image" />
        <p class="mb-0 ml-1">© 2024 DocuMento. <br />All Rights Reserved.</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
footer {
  background-color: #a04747;
  margin: 0;
  bottom: 0;
  width: 100%;
  color: white;
}
.container {
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

.footer-columns {
  display: flex;
  justify-content: space-around;
}

.footer-column {
  flex: 1;
  text-align: center;
}
.footer-info {
  margin-top: 10px;
  display: flex; /* Flexbox 사용하여 수평 정렬 */
  align-items: center; /* 요소들이 수직 중앙에 정렬되도록 설정 */
}

.footer-info img {
  display: block;
  margin-right: 20px;
}

.logo-image {
  margin: 0;
}
/* 카드부분 */
.count-box-container {
  padding-top: 20px;
  padding-bottom: 20px;
}
.card-body {
  background-color: #a04747;
  color: white;
  border: 1px solid white;
  border-radius: 5px;
}
/* 하이퍼링크 기본 스타일 제거 */
.custom-link {
  color: white; /* 글자 색 */
  text-decoration: none; /* 밑줄 제거 */

}

/* 마우스를 올릴 때 효과 */
.custom-link:hover {
  color: blue; /* 마우스 오버 시 글자 색 변경 */
  text-decoration: underline; /* 밑줄 추가 */
}
</style>
