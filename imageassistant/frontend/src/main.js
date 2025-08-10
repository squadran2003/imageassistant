import { createApp } from 'vue'
import './styles/css/tailwind.css' // Import Tailwind CSS
import App from './App.vue'
import router from './router.js'

const app = createApp(App)

// Configure warning handler to prevent sensitive data exposure
app.config.warnHandler = (msg) => {
  if (process.env.NODE_ENV === 'production') {
    // Suppress all warnings in production
    return
  }
  
  // In development, filter out sensitive data from warnings
  if (msg && typeof msg === 'string') {
    // Remove token data from warning messages
    const filteredMsg = msg.replace(/token:\s*"[^"]*"/g, 'token: "[FILTERED]"')
                          .replace(/Bearer\s+[a-zA-Z0-9._-]+/g, 'Bearer [FILTERED]')
    console.warn(`[Vue warn]: ${filteredMsg}`)
  }
}

app.use(router).mount('#app')
