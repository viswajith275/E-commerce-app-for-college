import axios from 'axios'

const BASE_URL = 'http://localhost:8000' //API IP

const api =axios.create({
    baseURL: BASE_URL,
    withCredentials: true,
    headers: {
        'Content-type': 'application/json'
    }
})

//Refresh Token accepting,I think?
api.interceptors.response.use(
    (response) => response,
    async (error)=>{
        const originalRequest = error.config;
        if(error.response.status === 401 && !originalRequest._retry){
            originalRequest._retry=true;
        
            try{
                api.post("/refresh")
    
                return api(originalRequest);
            }
            catch(refreshError){
                console.log("Session Expired");
                return Promise.reject(refreshError);
            }
        }
        return Promise.reject(error);
    }
    
);


export default api;