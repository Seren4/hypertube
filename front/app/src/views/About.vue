<template>
    <div class="" v-if="user" :key="user.id">
        <h3 v-if="user.login_method && user.login_method !== 'standard'">Logged via: {{user.login_method}}</h3>
        <div v-else style="margin: 2%"></div>
        <Alert  v-if="error_alert" :msg="error_alert" is_error class=""/>
        <div  v-if="error_alert_obj">
            <Alert v-for="(item, index) in error_alert_obj" :msg="index + ': ' + item[0]" :key="index" is_error />
            <Alert v-if="confirm_alert" :msg="confirm_alert" is_success   />

        </div>

        <div>
            <b-card class="" style="padding: 1vw">

                <b-media no-body class="row justify-content-center align-self-center no-gutters">

                    <b-media-aside class="col-12 col-md-5" style="display: inline-block; max-width: 700px; max-height: 600px;">
                        <img class="img-fluid img-thumbnail"  v-if="user.photo" :src="user.photo" alt="profile photo"  id="profile_pic" style="max-height: 40vw!important;margin-left: auto;margin-right: auto;">
                    </b-media-aside>

                    <b-media-body class="col-12 col-md-7">

                        <b-card bg-variant="light" >
                            <b-form-group label-cols-lg="3" label="Your Photo" label-size="lg" label-class="font-weight-bold pt-0" class="mb-0">

                                <b-form-group label-cols-sm="3" label-align-sm="right" >
                                    <input :disabled=isDisabled  type="file" class="custom-file-input" id="inputGroupFile01" ref="file" name="photo"  v-on:change="handleFileUpload()" v-validate="'required|image|mimes:image/*'">
                                    <label id="input_label" class="custom-file-label" for="inputGroupFile01" >Choose file</label>
                                </b-form-group>
                            </b-form-group>
                            <div style="padding-top: 1%">
                                <b-button variant="success" @click="submit" :disabled=isDisabled > upload </b-button>
                                <b-button variant="danger" @click="reset_photo()"  :disabled=isDisabled >reset</b-button>
                            </div>
                            <p v-if="errors.has('photo')" class="text-danger font-weight-light align-text-bottom">{{ errors.first('photo') }}</p>
                            <p v-else-if="photo_error" class="text-danger font-weight-light align-text-bottom">{{ photo_error }}</p>
                        </b-card>

                        <b-card bg-variant="light" >
                            <b-form-group label-cols-lg="3" label="Your Profile Information" label-size="lg" label-class="font-weight-bold pt-0" class="mb-0" name="profile-form">

                                <b-form-group label-cols-sm="3" label="First name:" label-align-sm="right" label-for="first_name" v-if="first_name !== null">
                                    <b-form-input  v-validate="'max:30|verify_name'" :disabled=isDisabled  id="first_name" name="first name" v-model="first_name" ></b-form-input>
                                </b-form-group>
                                <p class="text-danger font-weight-light align-text-bottom">{{ errors.first('first name') }}</p>


                                <b-form-group label-cols-sm="3" label="Last name:" label-align-sm="right" label-for="last_name" v-if="last_name !== null">
                                    <b-form-input  v-validate="'max:30|verify_name'" :disabled=isDisabled  id="last_name" name="last name" v-model="last_name" ></b-form-input>
                                </b-form-group>
                                <p class="text-danger font-weight-light align-text-bottom">{{ errors.first('last name') }}</p>


                                <b-form-group label-cols-sm="3" label="Username:" label-align-sm="right" label-for="username" v-if="username !== null">
                                    <b-form-input v-validate="'alpha_num|min:6|max:12'" :disabled=isDisabled  id="username" name="username" v-model="username" placeholder="username"></b-form-input>
                                </b-form-group>
                                <p class="text-danger font-weight-light align-text-bottom">{{ errors.first('username') }}</p>


                                <b-form-group label-cols-sm="3" label="Email:" label-align-sm="right" label-for="email" v-if="email !== null">
                                    <b-form-input  v-validate="'email'" :disabled=isDisabled  id="email" v-model="email" name="email"></b-form-input>
                                </b-form-group>
                                <p class="text-danger font-weight-light align-text-bottom">{{ errors.first('email') }}</p>

                                <b-form-group label-cols-sm="3" label="Language:" label-align-sm="right" label-for="language">
                                    <b-form-select v-model="language" :options="codes"  name="language"></b-form-select>

                                </b-form-group>
                                <p v-show="language_error" class="text-danger font-weight-light align-text-bottom">{{ language_error }}</p>

                            </b-form-group>
                            <div>
                                <b-button variant="success" @click="edit_profile" >update</b-button>
                                <b-button variant="danger"  @click="reset">reset</b-button>
                            </div>
                        </b-card>

                        <div >
                            <b-card bg-variant="light" >
                                <b-form-group label-cols-lg="3" label="Your Password" label-size="lg" label-class="font-weight-bold pt-0" class="mb-0" name="password-form">
                                    <b-form-group label-cols-sm="3" label="Password:" label-align-sm="right" label-for="nested-state">
                                        <b-form-input v-validate="'required|min:8|max:20|verify_password'" :disabled=isDisabled id="password1" v-model="password1" name="password" type="password" ref="password"></b-form-input>
                                    </b-form-group>
                                    <p class="text-danger font-weight-light align-text-bottom" v-show="errors.has('password')" >{{ errors.first('password') }}</p>

                                    <b-form-group label-cols-sm="3" label="Confirm Password:" label-align-sm="right" label-for="nested-country">
                                        <b-form-input  v-validate="'required|min:8|max:20|verify_password|confirmed:password'" :disabled=isDisabled id="password2" v-model="password2" name="password confirmation" type="password" data-vv-as="password"></b-form-input>
                                    </b-form-group>
                                    <p class="text-danger font-weight-light align-text-bottom" v-show="errors.has('password confirmation')" >{{ errors.first('password confirmation')}}</p>


                                </b-form-group>
                                <div>
                                    <b-button variant="success" @click="edit_password"  :disabled=isDisabled >update</b-button>
                                </div>
                            </b-card>
                        </div>
                    </b-media-body>
                </b-media>
            </b-card>
        </div>





    </div>
</template>


<script>
    import Alert from '@/components/Alert.vue'
    import axios from 'axios';
    export default {
        name: 'about',
        components: {
            Alert,
        },
        data() {
            return {
                is_success: false,
                is_error: false,
                token:localStorage.getItem('token'),
                user: {},
                photo: null,
                username: null,
                password:null,
                password1: null,
                password2:null,
                first_name:null,
                last_name:null,
                email:null,
                language: '',
                photo_error: null,
                error_alert: null,
                confirm_alert: null,
                language_error: null,
                error_alert_obj: {},
                codes: ['fr', 'en'],
            }
        },
        mounted(){
            this.$store.dispatch('authenticate').then(res => {
                if (!res) this.$router.push('/login');
                else
                {
                    axios.defaults.headers.common['Authorization'] = 'JWT ' + this.$store.getters.getToken;
                    this.get_user_data();
                }
            })
        },
        methods: {
            reset(){
                this.error_alert = null;
                this.confirm_alert = null;
                this.language_error = null;
                this.error_alert_obj = {};
                this.errors.clear();
                this.get_user_data()
            },
            reset_photo(){
                document.getElementById("input_label").innerHTML = 'Choose file';
                this.errors.clear();
                this.$refs.file.value = null;
                this.photo_error = null;
                this.error_alert = null;
                this.confirm_alert = null;
                this.error_alert_obj = {};
                this.photo = null;
            },
            edit_password(){
                this.error_alert_obj = {};
                this.confirm_alert = null;
                let valid = this.fields.password.valid && this.fields['password confirmation'].valid;
                if (valid) {
                    this.$store.dispatch('authenticate').then(res => {
                        if (!res) this.$router.push('/login');
                        else {
                            axios.defaults.headers.common['Authorization'] = 'JWT ' + this.$store.getters.getToken;
                            let url = ' http://localhost:8000/auth/user/edit_password/';
                            let self = this;
                            let data = {new_password1: this.password1, new_password2: this.password2};
                            axios({url, data: data, method: 'POST', headers: {}}).then(resp => {
                                if (resp.data.success) {
                                    localStorage.setItem('token', resp.data.token);
                                    axios.defaults.headers.common['Authorization'] = 'JWT ' + resp.data.token;
                                    self.token = resp.data.token;
                                    self.$store.commit('update_token', self.token);
                                    self.confirm_alert = "Password updated";
                                    self.password1 = null;
                                    self.password2 = null;
                                    self.$validator.reset();
                                } else {
                                    self.error_alert_obj = resp.data.message;
                                }
                                window.scrollTo(0,0);

                            })
                        }
                    })
                }
            },
            edit_profile(){
                this.error_alert_obj = {};
                this.confirm_alert = null;
                this.language_error = null;
                let changes = false;
                if (!this.codes.includes(this.language))
                    this.language_error = "Language error";
                if (this.username !== this.user.username || this.first_name !== this.user.first_name ||
                    this.last_name !== this.user.last_name || this.email !== this.user.email || this.language !== this.user.language)
                    changes = true;
                let valid = !this.language_error && this.fields.username.valid && this.fields.email.valid && this.fields['first name'].valid && this.fields['last name'].valid;
                if (valid && changes) {
                    this.$store.dispatch('authenticate').then(res => {
                        if (!res) this.$router.push('/login');
                        else {
                            axios.defaults.headers.common['Authorization'] = 'JWT ' + this.$store.getters.getToken;
                            let url = 'http://localhost:8000/auth/user/edit_profile/';
                            let self = this;
                            const formData = new FormData();
                            if (this.user.login_method === 'standard') {
                                if (this.username !== this.user.username) formData.set('username', this.username);
                                if (this.first_name !== this.user.first_name) formData.set('first_name', this.first_name);
                                if (this.last_name !== this.user.last_name) formData.set('last_name', this.last_name);
                                if (this.email !== this.user.email) formData.set('email', this.email);
                            }
                            if (this.language !== this.user.language)
                                formData.set('profile.language', this.language);

                            axios({
                                url, data: formData, method: 'POST', headers: {}
                            }).then(resp => {
                                // console.log(resp.data);
                                if (resp.data.success) {
                                    if (resp.data.message)
                                        self.confirm_alert = resp.data.message;
                                    else
                                        self.confirm_alert = "Profile updated";
                                    localStorage.setItem('token', resp.data.token);
                                    axios.defaults.headers.common['Authorization'] = 'JWT ' + resp.data.token;
                                    self.token = resp.data.token;
                                    self.$store.commit('update_token', self.token);
                                } else {
                                    self.error_alert_obj =  resp.data.message;
                                }
                                self.get_user_data()
                                window.scrollTo(0,0);

                            })
                        }
                    })
                }
            },
            backup_data(data){
                this.username = data.username;
                this.first_name = data.first_name;
                this.last_name = data.last_name;
                this.email = data.email;
                this.language = data.profile.language;
            },
            get_user_data(){
                this.$store.dispatch('authenticate').then(res => {
                    if (!res) this.$router.push('/login');
                    else
                    {
                        axios.defaults.headers.common['Authorization'] = 'JWT ' + this.$store.getters.getToken;
                        axios({url: 'http://localhost:8000/auth/user/get_user/', method: 'GET' }).then(res => {
                            if (res){
                                this.user = res.data;
                                if (res.data.profile.photo) this.user.photo = "http://localhost:8000"+res.data.profile.photo;
                                else if (res.data.profile.photo_url) this.user.photo = res.data.profile.photo_url;
                                else this.user.photo = null;
                                this.user.language = res.data.profile.language;
                                this.backup_data(this.user);
                            }
                        })
                    }
                })
            },
            submit(){
                this.error_alert_obj = {};
                this.confirm_alert = null;
                if (!this.photo_error && this.fields.photo.valid && this.photo) {
                    this.$store.dispatch('authenticate').then(res => {
                        if (!res) this.$router.push('/login');
                        else {
                            axios.defaults.headers.common['Authorization'] = 'JWT ' + this.$store.getters.getToken;
                            const formData = new FormData();
                            formData.append('photo', this.photo);
                            formData.set('user', this.user.id);
                            axios({
                                url: 'http://localhost:8000/auth/photo/' + this.user.profile.id + '/',
                                data: formData,
                                method: 'PUT',
                                headers: {}
                            }).then(resp => {
                                if (resp.data.success) {
                                    this.confirm_alert = "Photo updated";

                                    this.get_user_data()
                                } else {
                                    this.error_alert_obj =  resp.data.message;
                                }
                                this.photo = null;
                                this.$refs.file.value = null
                                document.getElementById("input_label").innerHTML = 'Choose file';
                            })
                        }
                    })
                }
            },
            async handleFileUpload() {
                this.photo_error = null;
                if (this.user.login_method === 'standard') {
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
                                    // this.photo = fileContents;
                                    // console.log(fileContents)
                                } else this.photo_error = "Error: Wrong format";
                            } else this.photo_error = "Error: Wrong format";
                        } else {
                            this.photo_error = "Error: Wrong format";
                        }
                    } else this.photo_error = "Error: Wrong format";
                }else this.photo_error = "Error: Not allowed";
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
        computed: {
            isDisabled() {
                return this.user.login_method !== 'standard';

            }
        }

    }
</script>

