import Vue from 'vue';
import Vuex from 'vuex';
import { authentication } from './authentication.module';
import createMutationsSharer from "/app/node_modules/vuex-shared-mutations";
import VuexPersist from 'vuex-persist';

Vue.use(Vuex);

const vuexLocalStorage = new VuexPersist({
    key: 'vuex', // The key to store the state on in the storage provider.
    storage: window.localStorage, // or window.sessionStorage or localForage
    // Function that passes the state and returns the state with only the objects you want to store.
    // reducer: state => state,
    // Function that passes a mutation and lets you decide if it should update the state in localStorage.
    // filter: mutation => (true)
    reducer: state => ({
        authentication: state.authentication
    }),

})


const store = new Vuex.Store({
    plugins: [vuexLocalStorage.plugin, createMutationsSharer({ predicate: ["auth_success", "auth_request", "auth_error", "logout", "update_token", "auth_reset"] })],
    modules: {
        // alert,
        authentication
    }
});


export default store;

