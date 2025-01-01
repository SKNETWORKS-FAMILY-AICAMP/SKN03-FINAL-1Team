<template>
    <div class="loading-container">
      <!-- 고정된 이미지 -->
      <div class="fixed-image">
        <img :src="imageSrc" alt="Main Image" />
      </div>
  
      <!-- 텍스트 애니메이션 -->
      <div class="animated-text">
        <span v-for="(char, index) in text" :key="index" :class="{'highlight': index === currentIndex}">
          {{ char }}
        </span>
      </div>
  
      <!-- 고정된 로딩 중 텍스트 -->
      <div class="loading-text">로딩 중...</div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import imageSrc from "@/assets/logox4.png"; // 고정된 이미지 경로
  
  // DOCUMENTO 텍스트
  const text = "DOCUMENTO".split(""); // 글자를 배열로 나눔
  const currentIndex = ref(0); // 현재 강조할 글자 인덱스
  
  // 애니메이션 시작
  const startAnimation = () => {
    setInterval(() => {
      currentIndex.value = (currentIndex.value + 1) % text.length; // 다음 글자로 순회
    }, 500); // 0.5초 간격
  };
  
  onMounted(() => {
    startAnimation();
  });
  </script>
  
  <style>
  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    margin: 50px auto;
  }
  
  .fixed-image img {
    width: 100px; /* 이미지 크기 */
    height: auto;
    margin-bottom: 10px; /* 이미지와 텍스트 간 간격 */
  }
  
  .animated-text {
    display: flex;
    gap: 5px; /* 글자 간 간격 */
    font-size: 24px;
    font-weight: bold;
    color: #8A8A8A; /* 기본 글자 색상 */
  }
  
  .highlight {
    color: #a04747; /* 강조 색상 */
  }
  
  .loading-text {
    margin-top: 20px;
    font-size: 16px;
    color: #a04747;
  }
  </style>
  