<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import axios from 'axios'

const messages = ref([]) // 대화 내용 저장
const inputText = ref('') // 입력값 저장

const sendMessage = async () => {
  const messageText = inputText.value.trim()
  if (messageText !== '') {
    messages.value.push({ text: messageText, type: 'user' }) // 사용자 메시지 추가
    inputText.value = '' // 입력 필드 내용 비우기
    scrollToBottom()

    try {
      const response = await axios.get(`/api/ask?ask_query=${encodeURIComponent(messageText)}`)
      messages.value.push({ text: response.data.answer.content, type: 'assistant' }) // API 응답 메시지 추가
    } catch (error) {
      console.error(error) // 오류를 콘솔에 출력
      messages.value.push({ text: '오류가 발생했습니다. 다시 시도해 주세요.', type: 'assistant' }) // 오류 처리
    }
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
  <div class="chat-container">
    <div class="chat-box flex-grow-1 w-100" ref="chatBoxRef">
      <div v-for="(message, index) in messages" :key="index" :class="['message', message.type]">
        {{ message.text }}
      </div>
    </div>
    <div class="input-area d-flex w-100 p-2 border-secondary-rounded">
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
.chat-container {
  width: 600px; /* 가로 길이를 600px로 고정 */
  height: 75vh; /* 높이를 75vh로 고정 */
  margin: 0 auto; /* 중앙 정렬 */
  display: flex;
  flex-direction: column;
}

.chat-box {
  overflow-y: auto; /* 세로 스크롤 활성화 */
  margin-bottom: 20px;
  flex-grow: 1; /* 남은 공간을 채우도록 설정 */
  width: 100%;
}

.input-area {
  border: 1px solid #a04747;
  border-radius: 50px;
  display: flex;
  gap: 10px;
  width: 100%; /* 좌우로 꽉 차게 설정 */
  margin-bottom: 5vh;
}

.chat-input {
  flex-grow: 1; /* 입력 필드가 남는 공간을 차지하도록 설정 */
  padding: 10px;
  border: none;
}

.chat-input:focus {
  border-color: none;
  box-shadow: none;
  outline: none; /* 포커스 시 기본 아웃라인 제거 */
}

.send-button {
  background-color: #a04747;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 50%;
  width: 50px;
  height: 50px;
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
