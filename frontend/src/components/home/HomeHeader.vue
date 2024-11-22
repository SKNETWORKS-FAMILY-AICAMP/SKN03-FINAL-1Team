<script setup>
const handleLogin = () => {
  window.location.href = '/login'
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
        <button @click="handleLogin">Login</button>
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
  top: 20px;
  right: 150px;
}

header ul.menu li {
  float: left;
  padding: 10px 20px;
  list-style: none;
}

.login-btn {
  position: absolute;
  top: 20px;
  right: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.result {
  margin-top: 20px;
  text-align: left;
  display: inline-block;
}
</style>
