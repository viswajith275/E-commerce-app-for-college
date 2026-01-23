import axios from 'axios'

const BASE_URL = 'http://localhost:8000' //API IP

const api =axios.create({
    baseURL: BASE_URL,
    withCredentials: true,
    headers: {
        'Content-type': 'application/json'
    }
})

export default api;