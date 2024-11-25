import axios from 'axios'

// axios 인스턴스를 생성
const instance = axios.create({
  baseURL: 'https://api.documento.click', // 백엔드 서버 주소
  withCredentials: true, // 인증 정보를 포함하는 요청 허용
  headers: {
    'Content-Type': 'application/json',
  },
})

export default instance
