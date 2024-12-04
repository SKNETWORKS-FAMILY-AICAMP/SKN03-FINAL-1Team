<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '@/axiosConfig'

const bookmarks = ref([])
const route = useRoute()

const mockResponse = {
  resultCode: 201,
  message: 'Bookmarks retrieved successfully.',
  result: {
    test: 'test입니다.',
    bookmarkList: [
      {
        title: '북마크 타이틀입니다.',
        parentPaperDoi: '10.18653/v1/2020.acl-demos.10',
        generatedKeyword: '테스트 키워드',
        similarity: 92,
      },
      {
        title: '북마크 타이틀입니다.',
        bookmarkTitle: 'test doi',
        parentPaperDoi: '10.18653/v1/2020.acl-demos.10',
        generatedKeyword: '테스트 키워드',
        similarity: 75,
      },
    ],
  },
}

const fetchBookmarks = async () => {
  try {
    console.log('테스트입니다.')
    bookmarks.value = mockResponse.result.bookmarkList
    console.log(bookmarks)
  } catch (error) {
    console.error('선행 논문을 가져오는 중 오류 발생:', error)

    if (mockResponse.resultCode === 201 && mockResponse.result.paperList) {
      bookmarks.value = mockResponse.result.paperList
    }
  }
}

onMounted(() => {
  fetchBookmarks()
})
</script>

<template>
  <div class="bookmark-container flex-column">
    <div class="bookmark-list mt-5 text-start">북마크 리스트</div>
    <ul class="list-group text-start">
      <li
        v-for="bookmark in bookmarks"
        :key="bookmark.bookmarkList"
        class="list-group-item text-start my-2 rounded-4"
      >
        <h5>
          <strong class="fst-italic">{{ bookmark.title }}</strong>
        </h5>
        <p>{{ bookmark.generatedKeyword }}</p>
      </li>
    </ul>
    <div class="temp-test">
      <div class="content my-2">10.18653/v1/2020.acl-demos.10</div>
      <div class="content my-2">뭔가 자연어 처리에 관한 서비스를 만들고 싶어!</div>
    </div>
  </div>
</template>

<style scoped>
.bookmark-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.bookmark-btn {
  border: none;
  background-color: transparent;
  color: red;
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

.list-group {
  color: black;
}
</style>
