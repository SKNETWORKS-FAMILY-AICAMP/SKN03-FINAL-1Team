<script setup>
import { ref, onMounted } from 'vue'
import BookmarkIcon from '@/assets/SideComponent/BookmarkIcon.png'

const bookmarks = ref([])

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
        generatedKeyword: '10.18653/v1/2020.acl-demos.10',
        similarity: 75,
      },
      {
        title: '북마크 타이틀입니다.',
        bookmarkTitle: 'test doi',
        parentPaperDoi: '10.18653/v1/2020.acl-demos.10',
        generatedKeyword: '뭔가 자연어 처리에 관한 서비스를 만들고 싶어!',
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
  }
}

const initDragAndDrop = () => {
  const draggables = document.querySelectorAll('.draggable')
  const container = document.getElementById('bookmark-list')

  draggables.forEach((draggable) => {
    draggable.addEventListener('dragstart', () => {
      draggable.classList.add('dragging')
    })

    draggable.addEventListener('dragend', () => {
      draggable.classList.remove('dragging')
    })
  })

  container.addEventListener('dragover', (e) => {
    e.preventDefault()
    const afterElement = getDragAfterElement(container, e.clientY)
    const draggable = document.querySelector('.dragging')
    if (afterElement == null) {
      container.appendChild(draggable)
    } else {
      container.insertBefore(draggable, afterElement)
    }
  })
}

const getDragAfterElement = (container, y) => {
  const draggableElements = [...container.querySelectorAll('.draggable:not(.dragging)')]

  return draggableElements.reduce(
    (closest, child) => {
      const box = child.getBoundingClientRect()
      const offset = y - box.top - box.height / 2
      if (offset < 0 && offset > closest.offset) {
        return { offset: offset, element: child }
      } else {
        return closest
      }
    },
    { offset: Number.NEGATIVE_INFINITY },
  ).element
}

onMounted(() => {
  fetchBookmarks()
  initDragAndDrop()
})
</script>

<template>
  <div class="bookmark-container flex-column">
    <div class="bookmark-list mt-5 text-start">북마크 리스트</div>
    <ul id="bookmark-list" class="list-group text-start">
      <li
        v-for="bookmark in bookmarks"
        :key="bookmark.bookmarkTitle"
        class="list-group-item text-start my-2 rounded-4 draggable"
        draggable="true"
      >
        <div class="d-flex align-items-center">
          <div class="me-3">
            <h5>
              <strong class="fst-italic">{{ bookmark.title }}</strong>
            </h5>
            <p>{{ bookmark.generatedKeyword }}</p>
          </div>
          <img :src="BookmarkIcon" class="ms-auto" />
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.bookmark-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 20px 0px 20px 20px;
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

.draggable {
  cursor: grab;
}

.dragging {
  opacity: 0.5;
}
</style>
