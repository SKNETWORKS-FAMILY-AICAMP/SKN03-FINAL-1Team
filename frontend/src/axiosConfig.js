import axios from 'axios'

const instance = axios.create({
  baseURL: 'https://api.documento.click',
  headers: {
    'Content-Type': 'application/json',
  },
})

instance.interceptors.request.use(
  (config) => {
    // 요청 전에 실행할 작업 추가
    return config
  },
  (error) => {
    // 요청 오류가 있는 경우 작업
    return Promise.reject(error)
  },
)

instance.interceptors.response.use(
  (response) => {
    // 응답 데이터를 가공하거나 다른 작업 추가
    return response
  },
  (error) => {
    // 응답 오류가 있는 경우 작업
    return Promise.reject(error)
  },
)

export default instance
