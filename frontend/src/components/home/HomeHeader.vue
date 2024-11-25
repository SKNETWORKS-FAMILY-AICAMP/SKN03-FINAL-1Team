<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.

const userInfo = ref(null)

// 사용자 정보 가져오기
const fetchUserInfo = async () => {
  try {
    const response = await axios.get('/user_info')
    userInfo.value = response.data
    console.log('User Info:', userInfo.value)
  } catch (error) {
    console.error('Failed to fetch user info:', error)
  }
}

// 로그인 버튼 클릭 핸들러
const handleLogin = () => {
  window.location.href = 'http://localhost:8000/login'
}

// 로그아웃 핸들러
const handleLogout = async () => {
  try {
    const response = await axios.get('/logout')
    console.log(response.data.message) // 로그아웃 성공 메시지 확인
    // 쿠키 삭제 및 페이지 리로드
    document.cookie = 'session_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=localhost'

    // 페이지 새로고침
    window.location.href = 'http://localhost:5173'
  } catch (error) {
    console.error('Failed to logout:', error)
  }
}

onMounted(() => {
  fetchUserInfo()
})
</script>

<template>
  <header>
    <a href="#" class="logo"><img alt="logo" src="@/assets/home-logo.png" width="170" /></a>
    <div class="menu-container">
      <div class="menuWrap">
        <ul class="menu">
          <li><a href="javascript:;">Search</a></li>
          <li><a href="javascript:;">Review</a></li>
          <li><a href="javascript:;">Mypage</a></li>
        </ul>
      </div>
      <div id="userMenu" class="user-info">
        <template v-if="userInfo">
          <img :src="userInfo.picture" alt="User Picture" width="32" height="32" />
          <span>{{ userInfo.name }}</span>
          <button @click="handleLogout" class="styled-button">Logout</button>
        </template>
        <template v-else>
          <button @click="handleLogin" class="styled-button">Login</button>
        </template>
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

.menu-container {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  height: 100%; /* 메뉴 컨테이너 높이를 header와 동일하게 설정 */
}

.menuWrap {
  display: flex;
  align-items: center;
  margin-right: 20px; /* 사용자 정보와의 간격 추가 */
}

header ul.menu:after {
  display: block;
  clear: both;
  content: '';
}

header ul.menu {
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

.user-info {
  display: flex;
  align-items: center;
  gap: 10px; /* 간격 추가 */
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
