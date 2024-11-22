<script setup>
const handleLogin = () => {
  window.location.href = 'http://localhost:8000/login'
}
</script>

<template>
  <header>
    <a href="#" class="logo"><img alt="logo" src="@/assets/home-logo.png" width="170" /></a>
    <div class="menuWrap">
      <ul class="menu">
        <li><a href="javascript:;">Search</a></li>
        <li><a href="javascript:;">Review</a></li>
        <li><a href="javascript:;">Mypage</a></li>
      </ul>
      <div id="googleSignInButton" class="login-btn">
        <button @click="handleLogin" class="styled-button">Login</button>
      </div>
    </div>
  </header>
</template>

<style scoped>
header {
  width: 100%;
  text-align: center;
  position: relative;
  height: 120px;
  box-sizing: border-box;
  padding: 0 15px;
  overflow-x: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
}

.logo {
  position: absolute;
  top: 50%;
  left: 15px;
  transform: translateY(-50%);
}

header ul.menu:after {
  display: block;
  clear: both;
  content: '';
}

header ul.menu {
  position: absolute;
  top: 50%;
  right: 150px;
  transform: translateY(-50%);
  display: flex;
  gap: 20px;
}

header ul.menu li {
  list-style: none;
}

header ul.menu li a {
  text-decoration: none;
  color: black;
  font-weight: bold;
  transition: color 0.3s;
}

header ul.menu li a:hover {
  color: #ffc107; /* 호버 효과 */
}

.login-btn {
  position: absolute;
  top: 50%;
  right: 50px;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.styled-button {
  background-color: #ff7043;
  border: none;
  color: white;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  border-radius: 5px; /* 둥근 모서리 */
  cursor: pointer;
  transition: background-color 0.3s; /* 배경 색 전환 효과 */
}

.styled-button:hover {
  background-color: #ff5722; /* 호버 배경 색 */
}

.result {
  margin-top: 20px;
  text-align: left;
  display: inline-block;
}
</style>
