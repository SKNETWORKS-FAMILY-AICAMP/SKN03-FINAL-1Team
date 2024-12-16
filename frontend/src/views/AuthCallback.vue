<script setup>
import { useRoute } from 'vue-router'
import {onMounted } from 'vue'

const route = useRoute()

const handleOAuthCallback = () => {
  const accessToken = route.query.access_token // URL에서 Access Token 추출

  if (!accessToken) {
    console.error('No access token found in URL!')
    return
  }

  try {
    // Access Token 저장
    localStorage.setItem('access_token', accessToken)

    console.log('Access Token saved successfully:', accessToken)

    const HOME_REDIRECT_URL = process.env.VUE_APP_HOME_REDIRECT_URL
    window.location.href = HOME_REDIRECT_URL
  } catch (error) {
    console.error('Error handling access token:', error)
  }
}

onMounted(() => {
  handleOAuthCallback()
})
</script>

<template>
  <div>
    <p>Authenticating... Redirecting...</p>
  </div>
</template>
