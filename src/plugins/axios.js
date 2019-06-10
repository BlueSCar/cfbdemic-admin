import Vue from 'vue';
import axios from 'axios';

const config = {
    timeout: 60 * 1000
};

if (process.env.NODE_ENV === 'development') {
    config.baseURL = `http://${process.env.WEB_HOST}`;
}

const _axios = axios.create(config); // eslint-disable-line

_axios.interceptors.request.use(
    config => config, // eslint-disable-line
    error => Promise.reject(error)
);

// Add a response interceptor
_axios.interceptors.response.use(
    response => response,
    error => Promise.reject(error)
);

Plugin.install = (Vue, options) => { // eslint-disable-line
    Vue.axios = _axios; // eslint-disable-line
    window.axios = _axios;
    Object.defineProperties(Vue.prototype, {
        axios: {
            get() {
                return _axios;
            }
        },
        $axios: {
            get() {
                return _axios;
            }
        }
    });
};

Vue.use(Plugin);

export default Plugin;
