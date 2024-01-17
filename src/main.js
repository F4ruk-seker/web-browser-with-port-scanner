import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css'
import axios from "axios";
import router from './router'

// axios.defaults.baseURL = 'https://backdoor-api.farukseker.com.tr/'
axios.defaults.baseURL = 'http://127.0.0.1:8000/'

createApp(App)
    .use(router)
    .mount('#app')
