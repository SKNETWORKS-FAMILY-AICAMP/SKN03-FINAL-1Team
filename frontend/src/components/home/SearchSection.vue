<script setup></script>

<template>
  <div class="HomeView py-5">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8 text-center">
          <h2 class="text-light mb-4"
          style="text-align: left;">AI 기반 빠르고 쉬운 논문 검색 시스템<br />DocuMento</h2>
          <div class="input-area d-flex p-2 mt-3">
        <input
          v-model="inputPrompt"
          type="text"
          class="form-control chat-input"
          placeholder="원하는 논문의 영어 키워드를 입력해보세요"
          
         
        />
        <button class="btn send-button" >></button>
  </div>
        </div>
      </div>
    </div>
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
  background-color: white;
 
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



</style>
