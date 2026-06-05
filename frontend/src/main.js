import { createApp } from 'vue';
import App from './App.vue';
import routes from './routes/routes.js';
import './assets/styles.css';
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
	history: createWebHistory(),
	routes: routes,
});

const app = createApp(App);
app.use(router);
app.mount('#app');
