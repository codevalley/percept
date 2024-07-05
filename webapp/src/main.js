import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import i18n from './i18n'
import './index.css'

const app = createApp(App)
router.onError((error) => {
    console.error('Global navigation error:', error)
  })
app.use(router)
app.provide('router', router) // Add this line
app.use(i18n)
app.mount('#app')