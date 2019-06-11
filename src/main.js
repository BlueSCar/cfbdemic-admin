import Vue from 'vue';
import App from './App.vue';
import router from './router';
import './plugins/bootstrap-vue';
import './plugins/fontawesome';
import './plugins/axios';
import './plugins/vue-spinners';

Vue.config.productionTip = false;
Vue.config.devtools = process.env.DEV_TOOLS === 'development';

new Vue({
    router,
    render: h => h(App)
}).$mount('#app');
