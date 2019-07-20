import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store/index'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// vee-validate
import VeeValidate from 'vee-validate';
Vue.use(VeeValidate);

VeeValidate.Validator.extend('verify_password', {
    getMessage: field => `The `+ field + ` must be between 8 and 20 characters long and must contain at least 1 uppercase, 1 lowercase, 1 number and one special character in the list !@#$%^&*`,
    validate: value => {
        var strongRegex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[!@#$%^&*])[A-Za-z\\d!@#$%^&*]{8,20}$");
        return strongRegex.test(value);
    }
});

VeeValidate.Validator.extend('verify_name', {
    getMessage: field => `Please enter a valid ` + field,
    validate: value => {
        var strongRegex = /^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$/u;
        return strongRegex.test(value);
    }
});


// font awesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { faUserSecret } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faUserSecret)

Vue.component('font-awesome-icon', FontAwesomeIcon)

import axios from 'axios';
import VueAxios from 'vue-axios'
var VueCookie = require('vue-cookie');
Vue.use(VueCookie);

Vue.use(VueAxios, axios);

Vue.use(BootstrapVue);

Vue.config.productionTip = false;

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app');
