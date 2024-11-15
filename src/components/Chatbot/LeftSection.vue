<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import IconBar from '@/components/Chatbot/IconBar/IconBarMain.vue'
import PaperItem from './LeftSection/PaperItem.vue'

const papers = ref([]) // 논문 리스트
const currentPage = ref(1) // 현재 페이지 번호
const itemsPerPage = 3 // 페이지 당 항목 수
</script>

<template>
  <div class="container m-0 p-0 h-100">
    <div class="left-side-content d-flex flex-row">
      <icon-bar />
      <div class="book-mark d-flex flex-column">
        <div class="bookmark-list mt-5 text-start">북마크 리스트</div>
        <div class="content my-2">
          <PaperItem />
          <PaperItem />
          <PaperItem />
          <PaperItem />
          <PaperItem />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  height: 100vh;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: row;
}

.left-side-content {
  display: flex;
  flex-direction: row; /* 가로 정렬 */
  background-color: #a04747;
  width: 100%;
  height: 100%;
  color: #ffffff;
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
  box-shadow: 2px 0px 10px 4px #515151; /* 섀도우 속성 추가 */
  margin-right: 20px;
}

.icon-bar {
  width: 80px;
  height: 100vh;
  border-top-right-radius: 20px;
  border-bottom-right-radius: 20px;
}

.book-mark {
  flex-grow: 1; /* 남은 공간을 차지하도록 설정 */
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.bookmark-list {
  position: relative;
  margin-top: 20px;
  padding: 10px 0;
  font-size: 20px;
  color: white;
}

.bookmark-list::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background-color: white;
}

.paper-entry {
  margin-top: 10px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.pagination button {
  background-color: #fff;
  border: 1px solid #ccc;
  color: #333;
  padding: 10px 15px;
  margin: 0 5px;
  cursor: pointer;
}

.pagination button.active {
  background-color: #a04747;
  color: white;
}
</style>
