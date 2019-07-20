import axios from 'axios/index'

export const authentication = {
    namespaced: false,
    state: {
        status: '',
        token: localStorage.getItem('token') || null,
    },
    getters : {
        authStatus: state => state.status,
        getToken (state){
            if (state.token) return (state.token);
            else return null;
        },
    },
    mutations: {
        auth_request(state){
            state.status = 'loading'
        },
        auth_reset(state){
            state.status = 'anonymous'
        },
        auth_success(state, data){
            state.status = 'success';
            state.token = data.token;
        },
        auth_error(state){
            state.status = 'error'
        },
        logout(state){
            state.status = 'anonymous';
            state.token = null;
        },
        update_token(state, new_token){
            state.token = new_token;
        }
    },
    actions: {
        signin({commit}, user) {
            return new Promise((resolve, reject) => {
                commit('auth_request');
                axios({url: 'http://localhost:8000/auth/request/signin/', data: user, method: 'POST'})
                    .then(resp => {
                        // console.log(resp.data);
                        if (resp.data.success) {
                            const token = resp.data.token;
                            const user = resp.data.user;
                            localStorage.setItem('token', token);
                            axios.defaults.headers.common['Authorization'] = token;
                            commit('auth_success', {token: token, user: user, username: user.username});

                        } else {
                            commit('auth_error');
                            localStorage.removeItem('token');
                        }
                        resolve(resp)

                    })
            })
        },
        reset(context, data) {
            return new Promise((resolve) => {
                delete axios.defaults.headers.common['Authorization'];
                axios({url: 'http://localhost:8000/auth/request/password_reset/', data: data, method: 'POST'})
                    .then(resp => {
                        resolve(resp)
                    })
            })
        },
        confirm_reset_pw(context, data) {
            return new Promise((resolve) => {
                axios({
                    url: 'http://localhost:8000/auth/reset-pw/', data: data,
                    method: 'POST'
                })
                    .then(resp => {
                        resolve(resp);
                    })
            })
        },
        social_signin({commit, dispatch}, jwt) {
            commit('auth_request');
            localStorage.setItem('token', jwt);
            axios.defaults.headers.common['Authorization'] = 'JWT ' + jwt;
            commit('auth_success', {token: jwt})

        },
        signup(context, user) {
            return new Promise((resolve) => {
                delete axios.defaults.headers.common['Authorization'];
                axios({url: 'http://localhost:8000/auth/request/signup/', data: user, method: 'POST'})
                    .then(resp => {
                        resolve(resp);
                    })
            })
        },
        logout({commit}) {
            return new Promise((resolve) => {
                window.onscroll = function(){};
                commit('logout');
                axios.defaults.headers.common['Authorization'] =  localStorage.getItem('token');
                axios({url: 'http://localhost:8000/auth/request/logout/', method: 'POST'});
                localStorage.removeItem('token');
                delete axios.defaults.headers.common['Authorization'];
                resolve()

            })
        },
        authenticate({commit}) {
            return new Promise((resolve) => {
                if (localStorage.getItem('token')) {
                    axios({
                        url: 'http://localhost:8000/auth/request/token-refresh/',
                        method: 'POST',
                        data: {'token': localStorage.getItem('token')}
                    })
                        .then(res => {
                            if (!res.data.success) {
                                commit('logout');
                                localStorage.removeItem('token');
                                delete axios.defaults.headers.common['Authorization'];
                            } else {
                                localStorage.setItem('token', res.data.token);
                                axios.defaults.headers.common['Authorization'] = 'JWT ' + res.data.token;
                                commit('update_token', res.data.token);
                            }
                            resolve(res.data.success)
                        })
                } else resolve(false)
            })
        }
    }

};





