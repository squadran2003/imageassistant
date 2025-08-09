import { createApp } from 'vue'
import './styles/css/tailwind.css' // Import Tailwind CSS
import App from './App.vue'
import router from './router.js'

createApp(App)
  .use(router)
  .mount('#app')
