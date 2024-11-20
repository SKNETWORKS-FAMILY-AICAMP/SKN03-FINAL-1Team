<script setup>
import Header from '@/components/home/HomeHeader.vue'
import Footer from '@/components/home/HomeFooter.vue'
import TestComponent from '@/components/TestComponent.vue'
</script>

<template>
  <div class="signup-container">
    <Header />
    <div class="form-container">
      <h2>회원가입</h2>
      <button @click="googleSignIn">Google로 회원가입</button>
    </div>
    <test-component />
    <Footer />
  </div>
</template>

<style scoped>
.signup-container {
  color: white;
  width: 100%;
  margin: 0;
  padding: 0 15px;
  box-sizing: border-box;
}

.form-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background-color: white;
  color: black;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h2 {
  margin-bottom: 20px;
}

button {
  width: 100%;
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
