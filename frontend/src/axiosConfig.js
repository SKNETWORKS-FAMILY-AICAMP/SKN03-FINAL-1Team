import axios from 'axios'

// Axios 인스턴스 생성
const instance = axios.create({
  baseURL: 'https://api.documento.click', // API 서버 주소
  withCredentials: true, // 인증 정보를 포함하는 요청 허용
  headers: {
    'Content-Type': 'application/json',
  },
})

export default instance
