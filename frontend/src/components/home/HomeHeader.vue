<script setup>
import { ref, onMounted } from 'vue'

// 환경 변수를 불러와 로그에 출력
console.log('VITE_APP_CLIENT_ID:', import.meta.env.VITE_APP_CLIENT_ID)
console.log('VITE_PROJECT_ROOT:', import.meta.env.VITE_PROJECT_ROOT)

const userToken = ref(null)

const loadGoogleSdk = () => {
  const script = document.createElement('script')
  script.src = 'https://accounts.google.com/gsi/client'
  script.async = true
  script.defer = true
  script.onload = initializeGoogleSignIn
  document.body.appendChild(script)
}

const initializeGoogleSignIn = () => {
  const google = window.google
  if (!google) {
    console.error('Google SDK 로드 실패')
    return
  }

  google.accounts.id.initialize({
    client_id: import.meta.env.VITE_APP_CLIENT_ID,
    callback: handleCredentialResponse,
  })

  google.accounts.id.renderButton(document.getElementById('googleSignInButton'), {
    theme: 'outline',
    size: 'large',
  })

  google.accounts.id.prompt()
}

const handleCredentialResponse = async (response) => {
  if (response.credential) {
    userToken.value = response.credential
    console.log('Google Token:', userToken.value)

    try {
      const res = await fetch('https://your-backend.com/api/verify-token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: userToken.value }),
      })

      const data = await res.json()
      if (res.ok) {
        console.log('토큰 검증 성공:', data)
        alert('토큰 검증에 성공했습니다!')
        // 추가적인 로그인 처리 로직
      } else {
        console.error('토큰 검증 실패:', data.message)
        alert(`토큰 검증 실패: ${data.message}`)
      }
    } catch (error) {
      console.error('서버 통신 오류:', error)
      alert('서버와의 통신 중 오류가 발생했습니다.')
    }
  } else {
    console.error('인증 응답에 토큰이 없습니다.')
    alert('인증에 실패했습니다. 다시 시도해주세요.')
  }
}

onMounted(() => {
  loadGoogleSdk()
})
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
      <<<<<<< HEAD
      <div id="googleSignInButton" class="login-btn">
        <button @click="handleLogin" class="styled-button">Login</button>
      </div>
      =======
      <div id="googleSignInButton" class="login-btn"></div>
      >>>>>>> a08fef817b7365195cddf428e8618dbb7745344e
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
<<<<<<< HEAD
  background: linear-gradient(45deg, #6ab7ff, #4fc3f7); /* 배경 그라데이션 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
=======
>>>>>>> a08fef817b7365195cddf428e8618dbb7745344e
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
<<<<<<< HEAD
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
  color: white;
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
=======
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
>>>>>>> a08fef817b7365195cddf428e8618dbb7745344e
  display: flex;
  align-items: center;
  justify-content: center;
}

<<<<<<< HEAD
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

=======
>>>>>>> a08fef817b7365195cddf428e8618dbb7745344e
.result {
  margin-top: 20px;
  text-align: left;
  display: inline-block;
}
</style>
