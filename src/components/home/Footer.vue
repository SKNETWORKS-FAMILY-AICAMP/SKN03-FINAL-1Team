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
      <div class="footer-info">
        <p>© 2024 DocuMento. All Rights Reserved.</p>
        <img src="@/assets/logo.png" alt="DocuMento logo" width="200" />
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
}

.footer-info img {
  display: block;
  margin: 0 auto;
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
