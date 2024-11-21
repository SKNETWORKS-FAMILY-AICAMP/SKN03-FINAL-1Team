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
      <div id="googleSignInButton" class="login-btn"></div>
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
