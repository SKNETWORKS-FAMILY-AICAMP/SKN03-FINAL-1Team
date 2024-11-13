<script setup>
import LeftSection from '@/components/Chatbot/LeftSection.vue'
import RightSection from '@/components/Chatbot/RightSection.vue'
</script>

<template>
  <div class="container-fluid d-flex">
    <div class="row flex-fill w-100">
      <div class="col-md-3 p-0">
        <LeftSection />
      </div>
      <div class="col-md-9 p-0">
        <RightSection />
      </div>
    </div>
  </div>
</template>

<style scoped>
.container-fluid {
  height: 100vh;
  margin: 0;
  padding: 0;
}

.row {
  margin: 0;
  width: 100%;
}

.col-md-4,
.col-md-8 {
  padding: 0;
}
</style>
