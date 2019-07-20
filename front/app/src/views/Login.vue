<template>
    <div class="container">

        <Alert v-if="loading==='error'" msg="Login error" is_error  class="mainbox col-md-10 col-md-offset-3 col-sm-10 col-sm-offset-2" />
        <Alert v-if="account_confirmed_ornot==='True'" :msg="account_confirmed"  is_success class="mainbox col-md-10 col-md-offset-3 col-sm-10 col-sm-offset-2" />
        <Alert v-if="account_confirmed_ornot==='False'" :msg="account_confirmed"  is_error class="mainbox col-md-10 col-md-offset-3 col-sm-10 col-sm-offset-2" />
        <Alert v-if="confirm_alert" :msg="confirm_alert" is_success  class="mainbox col-md-10 col-md-offset-3 col-sm-10 col-sm-offset-2" />
        <div  v-if="error_alert_obj">
            <Alert v-for="(item, index) in error_alert_obj" :msg="item[0]" :key="index" is_error class="mainbox col-md-10 col-md-offset-3 col-sm-10 col-sm-offset-2"/>

        </div>
        <Alert v-if="error_alert" :msg="error_alert" is_error class="mainbox col-md-10 col-md-offset-3 col-sm-10 col-sm-offset-2"/>

        <div class="text-center mainbox col-md-10 col-md-offset-3 col-sm-8 col-sm-offset-2" v-if="loading==='loading'">

            <div class="spinner-grow" style="width: 3rem; height: 3rem;" role="status">
                <span class="sr-only">Loading...</span>
            </div>
        </div>


        <!--LOGIN-->
        <div id="loginbox" style="margin-top:50px;" class="mainbox col-md-10 col-md-offset-2 col-sm-10 col-sm-offset-2" v-show="loginbox" v-if="loading !== 'success' && loading !== 'loading'">
            <div class="panel panel-info" >
                <div class="panel-heading">
                    <div class="panel-title">Sign In</div>
                    <div style="float:right; font-size: 80%; position: relative; top:-10px; padding-top:15px;">
                        <a href="#" @click="show_resetbox">Forgot password?</a>
                    </div>
                </div>
                <div style="padding-top:30px" class="panel-body" >

                    <div style="display:none" id="login-alert" class="alert alert-danger col-sm-12">
                    </div>

                    <form id="loginform" class="form-horizontal" role="form">
                        <div style="margin-bottom: 25px" class="input-group">
                            <span class="input-group-addon">
                                <i class="glyphicon glyphicon-user"></i>
                            </span>
                            <input v-validate="'required|alpha_num|min:6|max:12'" id="login-username" type="text"  class="form-control" name="username" value="" placeholder="username" v-model="username" >
                        </div>
                        <p class="text-danger font-weight-light align-text-bottom">{{ errors.first('username') }}</p>
                        <div style="margin-bottom: 25px" class="input-group">
                            <span class="input-group-addon">
                                <i class="glyphicon glyphicon-lock"></i>
                            </span>
                            <input v-validate="'required|verify_password'" id="login-password" type="password" class="form-control" name="password" placeholder="password" v-model="password" >
                        </div>
                        <p class="text-danger font-weight-light align-text-bottom" v-show="errors.has('password')" >{{ errors.first('password') }}</p>

                        <div style="margin-top:10px" class="form-group">
                            <!-- Button -->
                            <div class="col-sm-12 controls">
                                <button id="btn-login" type="button" class="btn btn-success" @click="signin" :class="{ disabled: loading === 'loading' }" >Login  </button>
                            </div>
                        </div>
                        <div  class="form-group">
                            <a @click="make_request"  class="btn btn-info" href="http://localhost:8000/accounts/google/login/?process=login" :class="{ disabled: loading === 'loading' }" ><i class="fab fa-google"></i></a>
                            <a @click="make_request"  class="btn btn-info"  href="http://localhost:8000/accounts/github/login/?process=login" :class="{ disabled: loading === 'loading' }"><i class="fab fa-github"></i></a>
                            <a style="padding: 0" class="btn btn-info" v-bind:href=" 'https://api.intra.42.fr/oauth/authorize?client_id='+ this.client_id + '&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Flogin&response_type=code&state=' + this.state "
                               :class="{ disabled: loading === 'loading' }">
                                <i class="fab icon-42"></i> </a>
                        </div>
                        <div class="form-group">
                            <div class="col-md-12 control">
                                <div style="border-top: 1px solid#888; padding-top:15px; font-size:85%" >
                                    Don't have an account!
                                    <a href="#" @click="show_register">Sign Up Here</a>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        <!--END LOGIN-->

        <!--RESET PASS-->
        <div id="resetbox" style="margin-top:50px;display: none" class="mainbox col-md-10 col-md-offset-3 col-sm-10 col-sm-offset-2" v-show="resetbox">
            <div class="panel panel-info" >
                <div style="padding-top:30px" class="panel-body" >
                    <form class="form-horizontal" role="form">

                        <div style="margin-bottom: 25px" class="input-group">
                            <span class="input-group-addon">
                                <i class="glyphicon glyphicon-user"></i>
                            </span>
                            <input v-validate="'required|email'" id="reset-email" type="email" class="form-control" name="email_reset" placeholder="email" v-model="email" data-vv-as="email">

                        </div>
                        <p class="text-danger font-weight-light align-text-bottom" v-show="errors.has('email_reset')" >{{ errors.first('email_reset') }}</p>

                        <div style="margin-top:10px" class="form-group">
                            <div class="col-sm-12 controls">
                                <a id="btn-reset" href="#" class="btn btn-success" @click="reset">Send email </a>
                            </div>
                        </div>

                        <div class="form-group">
                            <div class="col-md-12 control">
                                <div style="border-top: 1px solid#888; padding-top:15px; font-size:85%" >
                                    Don't have an account!
                                    <a href="#" @click="show_register">Sign Up Here</a>
                                    <br>
                                    Back to <a href="#" @click="show_login">Login</a>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        <!--END RESET PASS-->

        <!--   CONFIRM RESET PW-->

        <div id="resetconfirmbox" style="margin-top:50px;" class="mainbox col-md-10 col-md-offset-3 col-sm-10 col-sm-offset-2"  v-show="resetconfirmbox">
            <p>Reset password</p>
            <div class="panel panel-info" >
                <div style="padding-top:30px" class="panel-body" >

                    <form class="form-horizontal" role="form" >
                        <div style="margin-bottom: 25px" class="input-group">
                            <span class="input-group-addon">
                                <i class="glyphicon glyphicon-user"></i>
                            </span>
                            <!--<input v-validate="'required|min:8|max:20|verify_password'" type="password" class="form-control" name="password"  placeholder="pw" v-model="reset_pw_1"  >-->
                            <input v-validate="'required|verify_password'" type="password" class="form-control" name="password_reset"  placeholder="pw" v-model="reset_pw_1" ref="password_reset" data-vv-as="password" >
                        </div>
                        <p class="text-danger font-weight-light align-text-bottom" v-show="errors.has('password_reset')">{{ errors.first('password_reset')}}</p>

                        <div style="margin-bottom: 25px" class="input-group">
                            <span class="input-group-addon">
                                <i class="glyphicon glyphicon-user"></i>
                            </span>
                            <input  v-validate="'required|verify_password|confirmed:password_reset'"  type="password" class="form-control" name="password_reset_confirm" placeholder="pw" v-model="reset_pw_2" data-vv-as="confirm password">
                        </div>
                        <p class="text-danger font-weight-light align-text-bottom" v-show="errors.has('password_reset_confirm')" > {{ errors.first('password_reset_confirm')}}</p>
                        <div style="margin-top:10px" class="form-group">
                            <div class="col-sm-12 controls">
                                <a id="btn-confirm" href="#" class="btn btn-success" @click="reset_password">Confirm </a>
                            </div>
                        </div>

                        <div class="form-group">
                            <div class="col-md-12 control">
                                <div style="border-top: 1px solid#888; padding-top:15px; font-size:85%" >
                                    Don't have an account!
                                    <a href="#" @click="show_register">Sign Up Here</a>

                                    <br>
                                    Back to
                                    <a href="#" @click="show_login">Login</a>

                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <!--   END CONFIRM RESET PW-->


        <!--SIGN UP-->
        <div id="signupbox" style="display:none; margin-top:50px" class="mainbox col-md-10 col-md-offset-4 col-sm-10 col-sm-offset-2" v-show="signupbox">
            <div class="panel panel-info">
                <div class="panel-heading">
                    <div class="panel-title">Sign Up</div>
                    <br>
                </div>
                <div class="panel-body" >
                    <form id="signupform" class="form-horizontal" role="form" enctype="multipart/form-data">

                        <div id="signupalert" style="display:none" class="alert alert-danger">
                            <p>Error:</p>
                            <span></span>
                        </div>

                        <label for="signup_firstname" class="col-md-3 control-label">First Name</label>
                        <div style="margin-bottom: 25px" class="input-group" id="signup_firstname">
                            <span class="input-group-addon">
                                <i class="glyphicon glyphicon-user"></i>
                            </span>
                            <input v-validate="'required|max:30|verify_name'" type="text" class="form-control" name="first_name" data-vv-as="first name" placeholder="first name" v-model="first_name">
                        </div>
                        <p class="text-danger font-weight-light align-text-bottom">{{ errors.first('first_name') }}</p>

                        <label for="signup_lastname" class="col-md-3 control-label">Last Name</label>
                        <div style="margin-bottom: 25px" class="input-group" id="signup_lastname">
                            <span class="input-group-addon">
                                <i class="glyphicon glyphicon-user"></i>
                            </span>
                            <input v-validate="'required|max:30|verify_name'" type="text" class="form-control" name="last_name"  data-vv-as="last name" value="" placeholder="last name" v-model="last_name">
                        </div>
                        <p class="text-danger font-weight-light align-text-bottom">{{ errors.first('last_name') }}</p>

                        <label for="signup_username" class="col-md-3 control-label">Username</label>
                        <div style="margin-bottom: 25px" class="input-group" id="signup_username">
                            <span class="input-group-addon">
                                <i class="glyphicon glyphicon-user"></i>
                            </span>
                            <input v-validate="'required|alpha_num|min:6|max:12'" name="username_signup" type="text" class="form-control" placeholder="username" v-model="username"  data-vv-as="username">
                        </div>
                        <p class="text-danger font-weight-light align-text-bottom">{{ errors.first('username_signup') }}</p>


                        <label for="signup_email" class="col-md-1 control-label">Email</label>
                        <div style="margin-bottom: 25px" class="input-group" id="signup_email">
                            <span class="input-group-addon">
                                <i class="glyphicon glyphicon-user"></i>
                            </span>
                            <input v-validate="'required|email'" type="text" class="form-control" name="email" placeholder="email" v-model="email">
                        </div>
                        <p class="text-danger font-weight-light align-text-bottom">{{ errors.first('email') }}</p>


                        <label for="signup_password" class="col-md-3 control-label">Password</label>
                        <div style="margin-bottom: 25px" class="input-group" id="signup_password">
                            <span class="input-group-addon">
                                <i class="glyphicon glyphicon-user"></i>
                            </span>
                            <input  v-validate="'required|verify_password'" type="password" class="form-control" name="password_signup" placeholder="password" v-model="password1" ref="password_signup"  data-vv-as="password">
                        </div>
                        <p class="text-danger font-weight-light align-text-bottom" v-show="errors.has('password_signup')">{{ errors.first('password_signup') }}</p>


                        <label for="signup_confirm_password" class="col-md-3 control-label">Confirm Password</label>
                        <div style="margin-bottom: 25px" class="input-group" id="signup_confirm_password">
                            <span class="input-group-addon">
                                <i class="glyphicon glyphicon-user"></i>
                            </span>
                            <input  v-validate="'required|verify_password|confirmed:password_signup'" type="password" class="form-control"  placeholder="confirm password" v-model="password2"  name="password_confirmation" data-vv-as="password confirmation">
                        </div>
                        <p v-show="errors.has('password_confirmation')" class="text-danger font-weight-light align-text-bottom">{{ errors.first('password_confirmation')}}</p>

                        <label for="signup_photo" class="control-label">Photo Upload</label>
                        <div style="margin-bottom: 25px" class="input-group" id="">

                            <!--<input type="file" id="signup_photo" ref="file" name="photo"  v-on:change="handleFileUpload()" v-validate="'required|image|mimes:image/*'"/>-->

                            <div class="custom-file" id="signup_photo">
                                <input type="file" class="custom-file-input" id="inputGroupFile01" ref="file" name="photo"  v-on:change="handleFileUpload()" v-validate="'required|image|mimes:image/*'">
                                <label id="input_label" class="custom-file-label" for="inputGroupFile01" >Choose file</label>
                            </div>
                        </div>




                        <p v-if="errors.has('photo')" class="text-danger font-weight-light align-text-bottom">{{ errors.first('photo') }}</p>
                        <p v-else-if="photo_error" class="text-danger font-weight-light align-text-bottom">{{ photo_error }}</p>

                        <div class="form-group">
                            <!-- Button -->
                            <div class="col-sm-12 controls">
                                <button id="btn-signup" type="button" class="btn btn-success" @click="signup"  :class="{ disabled: loading === 'loading' }">
                                    Sign Up
                                </button>
                            </div>
                        </div>

                        <div style="padding-top:20px"  class="form-group">
                            <a @click="make_request"  class="btn btn-info" href="http://localhost:8000/accounts/google/login/?process=login" :class="{ disabled: loading === 'loading' }"><i class="fab fa-google"></i></a>
                            <a @click="make_request"  class="btn btn-info"  href="http://localhost:8000/accounts/github/login/?process=login" :class="{ disabled: loading === 'loading' }"><i class="fab fa-github"></i></a>
                            <a style="padding: 0" class="btn btn-info" v-bind:href=" 'https://api.intra.42.fr/oauth/authorize?client_id='+ this.client_id + '&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Flogin&response_type=code&state=' + this.state "
                               :class="{ disabled: loading === 'loading' }">
                                <i class=" fab icon-42"></i> </a>
                        </div>

                        <div class="form-group">
                            <div class="col-md-12 control">
                                <div style="border-top: 1px solid#888; padding-top:15px; font-size:85%" >
                                    <a href="#" @click="show_login">Sign In</a>
                                </div>
                            </div>
                        </div>

                    </form>
                </div>
            </div>

        </div>

    </div>

</template>

<script>
    import axios from 'axios';
    import Alert from "../components/Alert";

    export default {
        name: 'Login',
        components: {
            Alert
        },
        data() {
            return {
                client_id:'',
                state: '42state',
                username: null,
                password: null,
                password1: null,
                password2: null,
                first_name: null,
                last_name: null,
                email: null,
                photo: null,
                reset_pw_1: null,
                reset_pw_2: null,
                show: false,
                account_confirmed:null,
                account_confirmed_ornot:null,
                alert: null,
                confirm_alert: null,
                error_alert: null,
                photo_error: null,
                loginbox: true,
                resetbox: false,
                resetconfirmbox: false,
                signupbox: false,
                error_alert_obj: {},
                key: null
            }
        },
        computed: {
            loading() {
                return this.$store.getters.authStatus;
            },
        },
        mounted(){
            // this.clear()
            window.onscroll = function(){};
            if (this.loading !== 'success')
                this.$store.commit('auth_reset');
            else if (this.loading === 'success' && (!this.$route.query.jwt || !this.$route.query.key || !this.$route.query.confirmed || !(this.$route.query.code && this.$route.query.state)))
            {
                this.$router.push('/');
            }
            if (this.$route.query.key)
            {
                this.key = this.$route.query.key;
                this.resetconfirmbox = true;
                this.loginbox = false;

            }
            else if (this.$route.query.jwt){
                this.store_jwt();
            }
            // If the states don't match, the request has been created by a third party and the process should be aborted.
            else if (this.$route.query.code && this.$route.query.state && this.$route.query.state === '42state'){
                this.login42()
            }

            else if (this.$route.query.confirmed)
            {
                this.account_confirmed_ornot = this.$route.query.confirmed;
                if (this.$route.query.confirmed === "True")
                {
                    this.account_confirmed = "Your account has been activated. You may now log in.";
                }
                else if (this.$route.query.confirmed === "False")
                {
                    this.account_confirmed = "There was an error during your account activation";
                }
            }
        },
        methods: {
            show_login(){
                this.reset_form();
                this.loginbox = true;
                this.signupbox = false;
                this.resetconfirmbox = false;
                this.resetbox = false;

            },
            show_register(){
                this.reset_form();
                this.signupbox = true;
                this.loginbox = false;
                this.resetconfirmbox = false;
                this.resetbox = false;

            },
            show_resetbox(){
                this.reset_form();
                this.loginbox = false;
                this.resetbox = true;
            },
            clear(){
                this.errors.clear();
                this.error_alert = null;
                this.photo_error = null;
                this.error_alert_obj = {};
                this.confirm_alert = null;
                this.account_confirmed_ornot = null;
                this.$store.commit('auth_reset');

            },
            reset_form(){
                this.username = null;
                this.password = null;
                this.password1 = null;
                this.password2 = null;
                this.first_name = null;
                this.last_name = null;
                this.email = null;
                this.photo = null;
                this.$refs.file.value = null;
                document.getElementById("input_label").innerHTML = 'Choose file';
                this.reset_pw_1 = null;
                this.reset_pw_2 = null;
                this.$validator.reset();
                this.clear();

            },
            reset_password(){
                this.clear();
                let self = this;
                this.$validator.validateAll().then(function(){
                    let valid = self.fields.password_reset.valid && self.fields.password_reset_confirm.valid;
                    if (valid && self.key) {
                        let data = {password: self.reset_pw_1, token: self.key};
                        self.$store.dispatch('confirm_reset_pw', data)
                            .then(res => {
                                if (res.data.success)
                                {
                                    self.loginbox = true;
                                    self.resetconfirmbox = false;
                                    self.confirm_alert = "Password changed";
                                    self.errors.clear();
                                }
                                else{
                                    if (res.data.message.status)
                                        self.error_alert = 'Invalid Token';
                                    else if (res.data.message.password)
                                        self.error_alert = res.data.message.password[0];
                                    else
                                        self.error_alert = 'Error';
                                }
                            })
                    }
                })
            },
            make_request() {
                this.$store.commit('auth_request');
            },
            store_jwt() {
                this.$store.dispatch('social_signin', this.$route.query.jwt)
                    .then(() => this.$router.push('/'))
            },
            signin() {
                this.$store.commit('logout');
                this.clear();
                let self = this;
                this.$validator.validateAll().then(function() {
                    let valid = self.fields.username.valid && self.fields.password.valid;
                    if (valid) {
                        // const { username, password } = this
                        let data = {'username': self.username, 'password': self.password, 'email': ''};
                        self.$store.dispatch('signin', data)
                            .then(() => self.$router.push('/'))
                    }
                })
            },
            reset() {
                this.clear();
                let self = this;
                this.$validator.validateAll() .then(function(){
                    if (self.fields.email_reset.valid) {
                        let data = {'email': self.email};
                        self.$store.dispatch('reset', data)
                            .then(res => {
                                if (res.data.success) {
                                    self.confirm_alert = "Mail sent"
                                } else
                                {
                                    if (res.data.message.email)
                                        self.error_alert = res.data.message.email[0]
                                }
                            })
                    }})
            },
            signup() {
                this.$store.commit('logout');
                this.confirm_alert = null;
                this.error_alert_obj = {};
                let self = this;
                this.$validator.validateAll().then(function(){
                    let valid = self.fields.first_name.valid && self.fields.last_name.valid && self.fields.username_signup.valid
                        && self.fields.email.valid && self.fields.password_signup.valid && self.fields.password_confirmation.valid
                        && self.fields.photo.valid && self.photo && !self.photo_error;
                    if (valid) {
                        const formData = new FormData();
                        formData.append('photo', self.photo);
                        formData.set('username', self.username);
                        formData.set('password1', self.password1);
                        formData.set('password2', self.password2);
                        formData.set('first_name', self.first_name);
                        formData.set('last_name', self.last_name);
                        formData.set('email', self.email);
                        self.$store.dispatch('signup', formData)
                            .then(res => {
                                if (res.data.success) {
                                    self.reset_form();
                                    self.confirm_alert = res.data.message;
                                    self.loginbox = true;
                                    self.signupbox = false;
                                } else {
                                    self.error_alert_obj = JSON.parse(res.data.errors);
                                }
                                window.scrollTo(0,0);
                            })
                    }
                })
            },
            login42() {
                this.$store.commit('logout');
                this.$store.commit('auth_request');
                let data = {'code': this.$route.query.code, 'state': this.$route.query.state};
                axios.post('http://localhost:8000/auth/request/login42/', data).then(res => {
                    if (res && res.data && res.data.token && res.data.user) {
                        localStorage.setItem('token', res.data.token);
                        axios.defaults.headers.common['Authorization'] = 'JWT ' + res.data.token;
                        this.$store.commit('auth_success', {token: res.data.token, user: res.data.user, username: res.data.user.login});
                        this.$router.push('/')

                    } else
                        this.$store.commit('auth_error');
                })
            },
            async handleFileUpload() {
                this.photo_error = null;
                if (!window.FileReader || !window.DataView) {
                    this.photo_error = "Error: Your browser doesn't support api ...";
                } else if (this.$refs.file.files[0]) {
                    document.getElementById("input_label").innerHTML = this.$refs.file.files[0].name;
                    let file = this.$refs.file.files[0];
                    this.photo_error = null;
                    /** check the size */
                    if (file.size) {
                        /** check the mime type */
                        if (!file.type.match('image.*')) {
                            this.photo_error = "Error: Wrong format";
                            return;
                        }
                        /** check the size max */
                        if (file.size > 2621440) {
                            this.photo_error = "Error: Image bigger than 2.5 MB";
                            return;
                        }
                        /** check the first4Bytes */
                        const file_error = await this.readUploadedFileAsArrayBuffer(file);

                        if (!file_error) {
                            /** finally read the photo */
                            const fileContents = await this.readUploadedFileAsText(file);
                            if (fileContents) {
                                this.photo = this.$refs.file.files[0];
                            } else this.photo_error = "Error: Wrong format";
                        } else this.photo_error = "Error: Wrong format";
                    }
                    else{
                        this.photo_error = "Error: Wrong format";
                    }
                } else this.photo_error = "Error: Wrong format";
            },
            readUploadedFileAsText(inputFile){
                const temporaryFileReader = new FileReader();
                return new Promise((resolve) => {

                    temporaryFileReader.onerror = () => {
                        temporaryFileReader.abort();
                        resolve(false);
                    };
                    temporaryFileReader.onload = () => {
                        resolve(temporaryFileReader.result);
                    };
                    temporaryFileReader.readAsDataURL(inputFile);
                });
            },
            readUploadedFileAsArrayBuffer(inputFile){
                const temporaryFileReader = new FileReader();
                return new Promise((resolve) => {
                    temporaryFileReader.onerror = () => {
                        temporaryFileReader.abort();
                        resolve(false);
                    };
                    temporaryFileReader.onload = (e) => {

                        let af = e.target.result
                            , view = new DataView(af), file_error = false;
                        if (view && view.getUint32(0, false)) {

                            let first4Bytes = view.getUint32(0, false);

                            let first4BytesHex = Number(first4Bytes).toString(16).toUpperCase();
                            switch (first4BytesHex) {
                                case 'FFD8FFE0':
                                case 'FFD8FFE1':
                                case 'FFD8FFE2':
                                case 'FFD8FFE3':
                                    break;
                                case '89504E47':
                                    break;
                                case '47494638':
                                    break;
                                default:
                                    file_error = true;
                                    break;
                            }
                        }
                        resolve(file_error);
                    };
                    temporaryFileReader.readAsArrayBuffer(inputFile);
                });
            },
        },
        watch: {
            loading() {
                if (this.loading === 'success' && (!this.$route.query.jwt || !this.$route.query.key || !this.$route.query.confirmed || !(this.$route.query.code && this.$route.query.state)))
                {
                    this.$router.push('/');
                }
            },
        },
    }
</script>
<style>
    .icon-42{
        background-image : url(../assets/42.png);
        background-size: cover;
        display: inline-block;
        height: 17px;
        margin: 8px 11px 4px 8px;
        width: 20px;
    }
</style>
