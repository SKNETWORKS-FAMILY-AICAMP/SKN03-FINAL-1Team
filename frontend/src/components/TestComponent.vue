<template>
  <div>
    <h2>Google OAuth Test</h2>
    <button @click="testGoogleOauth">Test Google OAuth</button>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'

// 'GAuth' 주입
const GAuth = inject('GAuth')

// 주입된 'GAuth'가 올바르게 주입되었는지 확인
if (!GAuth) {
  console.error('GAuth is not injected properly')
} else {
  console.log('Injected GAuth: ', GAuth)
}

const user = ref({})

// 테스트용 구글 OAuth 함수
const testGoogleOauth = async () => {
  try {
    await GAuth.signIn()
    if (GAuth.isAuthenticated.value) {
      const userInfo = GAuth.getUser()
      user.value = userInfo.profileObj
      console.log('User Info:', user.value)
    }
  } catch (error) {
    console.error('Google Sign-In Error:', error)
  }
}
</script>

<style scoped>
div {
  text-align: center;
  margin-top: 50px;
}

button {
  width: 200px;
  padding: 10px;
  background-color: #4285f4;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #357ae8;
}
</style>
