import { createApp } from 'vue';
import { createHead } from '@vueuse/head';
import App from './App.vue';
import router from './router';
import i18n from './i18n';
import FloatingVue from 'floating-vue';
import 'floating-vue/dist/style.css';
import './index.css';

const app = createApp(App);
const head = createHead();

router.onError((error: Error) => {
    console.error('Global navigation error:', error);
});

app.use(router);
app.provide('router', router);
app.use(i18n);
app.use(FloatingVue);
app.use(head);
app.mount('#app');