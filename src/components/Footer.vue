<script setup></script>

<template>
  <footer>
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
  </footer>
</template>

<style scoped>
footer {
  background-color: #a04747;
  padding: 10px;
  position: fixed;
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
</style>
