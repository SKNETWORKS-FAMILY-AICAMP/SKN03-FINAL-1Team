<script setup></script>
<template>
  <div class="test-content">
    <div class="input-area d-flex w-100 p-2">
      <input
        v-model="inputText"
        type="text"
        class="form-control chat-input"
        placeholder="탐색 키워드를 입력해보아요."
        @keyup.enter="sendMessage"
      />
      <button class="btn send-button" @click="sendMessage">></button>
    </div>
    <div><p>test</p></div>
    <div><p>test</p></div>
    <div><p>test</p></div>
  </div>
</template>
<style scoped>
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

.test-content {
  height: 80vh;
}
</style>
