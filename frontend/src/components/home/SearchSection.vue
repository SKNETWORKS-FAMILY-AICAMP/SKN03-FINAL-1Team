<script setup></script>

<template>
  <div class="HomeView py-5">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8 text-center">
          <h2 class="text-light mb-4">LLM 기반 논문 검색 시스템<br />DocuMento</h2>
          <input
            v-model="searchQuery"
            class="form-control form-control-lg"
            placeholder="원하는 키워드를 입력해보세요."
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
