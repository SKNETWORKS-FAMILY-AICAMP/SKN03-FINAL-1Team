<script setup></script>

<template>
  <div class="container-fluid vh-100 d-flex flex-column">
    <div class="row flex-fill">
      <div class="col-12 col-md-3 d-flex flex-column justify-content-center bg-light p-3">
        <!-- 좌측 30% -->
        <div class="left-side-content d-flex flex-column align-items-start">
          <!-- 원하는 콘텐츠 추가 -->
          <p>왼쪽 콘텐츠 영역</p>
        </div>
      </div>
      <div class="col-12 col-md-9 d-flex flex-column justify-content-center bg-white p-3">
        <!-- 우측 70% -->
        <div class="right-side-content">오른쪽 콘텐츠 영역</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container-fluid {
  height: 100vh; /* 뷰포트 높이를 100%로 설정 */
}

.left-side-content {
  background-color: #a04747; /* 배경 색상 설정 */
  width: 100%;
  height: 100%;
  display: flex;
  align-items: stretch; /* 상하로 빈 공간 없이 채움 */
  padding: 0;
  margin: 0;
}

.right-side-content {
  background-color: #ffffff; /* 배경 색상 설정 */
  width: 100%;
  height: 100%;
}
</style>
