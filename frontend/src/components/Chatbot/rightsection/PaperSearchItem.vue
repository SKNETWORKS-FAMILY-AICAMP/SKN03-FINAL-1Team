<script setup>
defineProps({
  paper: Object,
})
</script>

<template>
  <div class="paper-item d-flex align-items-center my-2">
    <div class="p-3">
      <img :src="paper.DragHandleIcon" />
    </div>
    <div class="text-start flex-grow-1 d-flex flex-column">
      <p>{{ paper.title }}</p>
      <p>{{ paper.authors }}</p>
      <p>{{ paper.abstract }}</p>
      <p>{{ paper.citation }} citations</p>
    </div>
    <div class="ms-auto p-4">
      <img :src="paper.BookMarkIcon" />
    </div>
  </div>
</template>

<style scoped>
.paper-item {
  background: white;
  color: black;
  border-radius: 10px;
  margin: 5px;
  padding: 0px;
  height: auto; /* Height is adjusted to fit the content */
}
.paper-item p {
  line-height: 1.2;
  margin-top: 5px;
  margin-bottom: 5px;
}
</style>
