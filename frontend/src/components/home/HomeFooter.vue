<script setup></script>

<template>
  <footer>
    <!-- 새로운 섹션 시작 -->
    <div class="container">
      <div class="count-box-container row mt-5 mx-3">
        <div class="count-box col-md-4 my-3">
          <div class="card">
            <div class="card-body">
              <h1 class="card-title">10547개</h1>
              <p class="card-text">총 논문 수</p>
            </div>
          </div>
        </div>
        <div class="count-box col-md-4 my-3">
          <div class="card">
            <div class="card-body">
              <h1 class="card-title">10547p</h1>
              <p class="card-text">총 페이지 수</p>
            </div>
          </div>
        </div>
        <div class="count-box col-md-4 my-3">
          <div class="card bg-white">
            <div class="card-body">
              <h1 class="card-title">10547개</h1>
              <p class="card-text">총 논문 수</p>
            </div>
          </div>
        </div>
      </div>
      <div class="footer-columns">
        <div class="footer-column">
          <h3>출처</h3>
          <p>(대충 깃허브 링크)</p>
          <p>(대충 논문 출처)</p>
        </div>
        <div class="footer-column">
          <h3>API</h3>
          <p>대충</p>
        </div>
        <div class="footer-column">
          <h3>개발자</h3>
          <p>SKN 3기 - 팀명뭐더라</p>
          <p>서민정 | git : 대충깃링크</p>
          <p>박규택 | git : 대충깃링크</p>
          <p>이준경 | git : 대충깃링크</p>
          <p>진윤화 | git : 대충깃링크</p>
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
</style>
