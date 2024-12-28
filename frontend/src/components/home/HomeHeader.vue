<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/axiosConfig' // 설정한 axios 인스턴스를 가져옵니다.
import defaultImage from '@/assets/DEFAULT_USER.svg' // 기본 이미지 import
// // 환경 변수에서 API URL과 로그인 URL을 가져옵니다.
const API_URL = process.env.VUE_APP_API_URL
const LOGIN_URL = process.env.VUE_APP_LOGIN_URL
const HOME_REDIRECT_URL = process.env.VUE_APP_HOME_REDIRECT_URL


const userInfo = ref(null)

// 사용자 정보 가져오기
const fetchUserInfo = async () => {
  try {

    const response = await axios.get(`${API_URL}/user_info`)
    userInfo.value = response.data.result
    console.log('User Info:', userInfo.value['userImg'])
  } catch (error) {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_info')

    localStorage.removeItem('hide_modal_today')
  }
}

// 로그인 버튼 클릭 핸들러
const handleLogin = () => {
  window.location.href = LOGIN_URL
}
// 로그아웃 핸들러
const handleLogout = async () => {
  try {

    const response = await axios.post(`${API_URL}/logout`)
    // 로컬 스토리지에서 Access Token 삭제
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_info')
    window.location.href = HOME_REDIRECT_URL

    console.log(response.data.message) // 로그아웃 성공 메시지 확인
  } catch (error) {
    console.error('Failed to logout:', error)
  }
}

const menuItems = ref([
  { name: 'Keyword', link: '/main' },
  { name: 'Search', link: '/main' },
  { name: 'Preview', link: '/main' },
])

onMounted(() => {
  fetchUserInfo()
})
</script>

<template>
  <header>
    <a href="#" class="logo"><img alt="logo" src="@/assets/home-logo.png" width="170" /></a>
    <div class="menu-container">
      <div class="menuWrap">
        <ul class="menu align-center m-0">
          <li v-for="item in menuItems" :key="item.name">
            <a :href="item.link">{{ item.name }}</a>
          </li>
        </ul>
      </div>
      <div id="userMenu" class="user-info">
        <template v-if="userInfo">
          
          <!--img :src="userInfo.userImg" alt="User Picture" width="32" height="32" /!-->
          <!-- 사용자 이미지 -->
    <img
      v-if="userInfo.userImg"
      :src="userInfo.userImg"
      alt="User Picture"
      width="32"
      height="32"
    />

    <!-- 기본 이미지 -->
    <img
      v-else
      :src="defaultImage"
      alt="Default User"
      width="32"
      height="32"
      class="default-image"
    />



          <span>{{ userInfo.userName }}</span>
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
  background-color: black;
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
  background-color: #c65d5d; /* 호버 배경 색 */
}

.result {
  margin-top: 20px;
  text-align: left;
  display: inline-block;
}
.default-image {
  filter: brightness(0) saturate(100%) invert(38%) sepia(32%) saturate(1286%) hue-rotate(314deg) brightness(91%) contrast(90%);
}
</style>
