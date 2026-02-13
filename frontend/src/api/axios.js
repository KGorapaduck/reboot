import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api', // Should be in env, but hardcoded for now matching other files
    timeout: 10000,
});

// Request interceptor to add Auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('auth_token');
        if (token) {
            config.headers.Authorization = `Token ${token}`; // DRF Token Auth uses 'Token <key>'
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default api;
