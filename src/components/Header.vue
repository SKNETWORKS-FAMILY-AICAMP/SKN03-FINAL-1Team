<template>
  <header>
    <h1>
      <a href="#" class="logo"><img alt="Vue logo" src="@/assets/logo.png" width="200" /></a>
    </h1>
    <div class="menuWrap">
      <ul class="menu">
        <li><a href="javascript:;">Search</a></li>
        <li><a href="javascript:;">Review</a></li>
        <li><a href="javascript:;">Mypage</a></li>
      </ul>
      <button class="login-btn">로그인</button>
    </div>
  </header>
</template>

<script>
export default {}
</script>

<style scoped>
header {
  width: 100%;
  text-align: center;
  position: relative;
  height: 120px;
  box-sizing: border-box; /* 추가: 박스 크기 조정 */
  padding: 0 15px; /* 추가: 내부 여백 설정 */
  overflow-x: hidden; /* 추가: 좌우 스크롤 제거 */
}

header h1 {
  position: absolute;
  top: 0;
  left: 100px;
}

header ul.menu:after {
  display: block;
  clear: both;
  content: '';
}

header ul.menu {
  position: absolute;
  top: 20px;
  right: 150px;
}

header ul.menu li {
  float: left;
  padding: 10px 20px;
  list-style: none;
}

/* 로그인 버튼 스타일 */
button.login-btn {
  position: absolute;
  top: 20px;
  right: 50px;
  padding: 10px 20px;
  background-color: #000000;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button.login-btn:hover {
  background-color: #a04747;
}

a {
  text-decoration: none;
  color: #333;
}
</style>
