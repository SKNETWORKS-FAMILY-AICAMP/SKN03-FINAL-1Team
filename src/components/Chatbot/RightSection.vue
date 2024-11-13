<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'

const messages = ref([]) // 대화 내용 저장
const inputText = ref('') // 입력값 저장

const sendMessage = () => {
  if (inputText.value.trim() !== '') {
    messages.value.push({ text: inputText.value, type: 'user' }) // 사용자 메시지 추가
    inputText.value = ''
    scrollToBottom()
  }
}

const chatBoxRef = ref(null)

const scrollToBottom = async () => {
  await nextTick() // DOM 업데이트 완료 후 스크롤 이동
  const chatBox = chatBoxRef.value
  if (chatBox) {
    chatBox.scrollTop = chatBox.scrollHeight
  }
}

onMounted(() => {
  scrollToBottom()
})

watch(messages, () => {
  scrollToBottom()
})
</script>
<template>
  <div class="right-side-content d-flex flex-column justify-content-between align-items-center p-4">
    <div class="chat-box flex-grow-1 w-100" ref="chatBoxRef">
      <div v-for="(message, index) in messages" :key="index" :class="['message', message.type]">
        {{ message.text }}
      </div>
    </div>
    <div class="input-area d-flex w-100">
      <input
        v-model="inputText"
        type="text"
        class="form-control chat-input"
        placeholder="궁금한 점들을 물어보세요."
        @keyup.enter="sendMessage"
      />
      <button class="btn send-button" @click="sendMessage">></button>
    </div>
  </div>
</template>

<style scoped>
.right-side-content {
  background-color: #ffffff;
  width: 100%;
  height: 100%;
  padding: 40px; /* 내부 여백을 크게 추가 */
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 상단과 하단으로 공간 분배 */
  align-items: center; /* 수평 중앙 정렬 */
}

.chat-box {
  overflow-y: auto; /* 세로 스크롤 활성화 */
  margin-bottom: 20px;
  max-height: 80vh; /* 최대 높이 설정 */
  width: 100%;
}

.input-area {
  display: flex;
  gap: 10px;
  width: 100%; /* 좌우로 꽉 차게 설정 */
  margin-bottom: 5vh;
}

.chat-input {
  flex-grow: 1; /* 입력 필드가 남는 공간을 차지하도록 설정 */
  padding: 10px;
  border: 2px solid #f8d7d7; /* 클릭 시 테두리 색상 추가 */
}

.chat-input:focus {
  border-color: #f8d7d7; /* 포커스 시 테두리 색상 유지 */
  box-shadow: 0 0 0 0.25rem rgba(248, 215, 215, 0.5); /* 포커스 시 그림자 효과 */
  outline: none; /* 포커스 시 기본 아웃라인 제거 */
}

.send-button {
  background-color: #a04747;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

.send-button:hover {
  background-color: #7a3737; /* 어두운 빨간색으로 변경 */
}

.message {
  padding: 10px;
  margin: 5px 0;
  border-radius: 5px;
}

.user {
  background-color: #f8d7d7;
  align-self: flex-end;
}

.assistant {
  background-color: #f0f0f0;
  align-self: flex-start;
}
</style>
