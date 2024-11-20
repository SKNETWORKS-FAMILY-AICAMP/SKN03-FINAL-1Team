<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps(['isToggled']) // props 사용
const emit = defineEmits(['toggleChat'])

const toggleChat = () => {
  emit('toggleChat') // 부모 컴포넌트에 이벤트 전송
}
</script>

<template>
  <div class="toggle-switch" @click="toggleChat">
    <div :class="['toggle-knob', { toggled: props.isToggled }]"></div>
    <span :class="['left-label', { inactive: props.isToggled }]">기술상담</span>
    <span :class="['right-label', { inactive: !props.isToggled }]">논문탐색</span>
  </div>
</template>

<style scoped>
.toggle-switch {
  color: white;
  width: 320px; /* 토글 스위치의 너비를 2배로 증가 */
  height: 60px; /* 토글 스위치의 높이를 적절히 조정 */
  background-color: #eee; /* 토글 스위치의 배경 색상을 흰색으로 설정 */
  border-radius: 30px;
  position: relative;
  cursor: pointer;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  padding: 5px; /* 상하좌우에 5px의 패딩 추가 */
}

.toggle-knob {
  width: 130px; /* 토글 버튼의 너비를 조정 */
  height: 40px; /* 상하 간격을 위해 높이 조정 */
  background-color: #a04747;
  border-radius: 25px;
  position: absolute;
  top: 10px; /* 상하 간격 */
  left: 25px; /* 좌우 간격 */
  transition:
    left 0.2s ease-in-out,
    background-color 0.2s ease-in-out;
}

.toggled {
  left: 165px; /* 토글 상태일 때 우측으로 이동 */
  background-color: #a04747; /* 토글 버튼 색상 설정 */
}

.left-label,
.right-label {
  position: absolute;
  width: 140px; /* 텍스트 너비 조정 */
  text-align: center;
  user-select: none; /* 텍스트 드래그 방지 */
  transition: color 0.3s ease-in-out; /* 텍스트 색상 변경에 0.5초 소요 */
}

.left-label {
  left: 20px; /* 왼쪽 텍스트 위치 조정 */
  font-size: 14px; /* 폰트 크기 증가 */
}

.right-label {
  right: 20px; /* 오른쪽 텍스트 위치 조정 */
  font-size: 14px; /* 폰트 크기 증가 */
}

.inactive {
  color: #888888; /* 비활성화된 텍스트 색상 */
}
</style>
