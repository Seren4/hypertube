<template>
    <div v-if="movie">
        <!--VIDEO PLAYER-->
        <b-modal  id="player-modal"  centered size="xl" :busy=true :hide-header=true :hide-footer=true content-class="bg-transparent border-0">
            <video-player  class="video-player-box"
                           ref="videoPlayer"
                           :options="playerOptions"
                           :playsinline="true"
                           id="video"
            >
            </video-player>
            <div class="alert alert-secondary"  id="player_info" :style="{width: my_width + 'px'}">
                <p class="">You should wait at least 40% to have a fluent video streaming.</p>
                <p class="">You can still start the player, but you could encounter freeze that leads you to reload the player.</p>
                <p class="">Percentage complete: <span id="prct_downloaded">0</span> % </p>
                <p class="">Download rate: <span id="rate_downloaded">0</span> /s </p>

            </div>
        </b-modal>


        <div>
            <b-card overlay
                    :img-src="backdrop"
                    img-alt="Card Image"
                    text-variant="white"
                    style="border:none">
                <b-media no-body class="row no-gutters ">

                    <!--SIDE IMAGE-->
                    <b-media-aside  @click="startPlayer"  class="col-12 col-md-4" id="cover_film">
                        <div class="spinner-grow player_icon" style="width: 3rem; height: 3rem;" role="status" v-if="loading"></div>
                        <i class="far fa-play-circle player_icon " v-if="!loading"></i>
                        <b-img :src="movie.thumbnail" class="cover"  v-if="movie.thumbnail" slot="aside"></b-img>
                    </b-media-aside>

                    <b-media-body class="col-12 col-md-6" style="margin-top: 5vw">
                        <b-container class="description">
                            <b-row>
                                <b-col cols="12">
                                    <h5 class="card-title">Title</h5>
                                    <h6  class="card-subtitle mb-2 text-muted" v-if="movie.title"> {{movie.title}}</h6>
                                    <h6  class="card-subtitle mb-2 text-muted" v-else> API timeout</h6>
                                </b-col>
                            </b-row>
                            <b-row>
                                <b-col col md="auto">
                                    <h5 class="card-title">Plot</h5>
                                    <h6  class="card-subtitle mb-2 text-muted" v-if="movie.synopsis"> {{movie.synopsis}}...</h6>
                                    <h6  class="card-subtitle mb-2 text-muted" v-else> API timeout</h6>
                                </b-col>
                            </b-row>
                            <b-row >
                                <b-col >
                                    <h5 class="card-title">Casting</h5>
                                    <h6 class="card-subtitle mb-2 text-muted" v-if="omovie.casting">{{omovie.casting}}</h6>
                                    <h6  class="card-subtitle mb-2 text-muted" v-else> API timeout</h6>
                                </b-col>
                            </b-row>
                            <b-row >
                                <b-col >
                                    <h5 class="card-title">Genres</h5>
                                    <h6 v-if="movie.genre.length">
                                        <span class="tag" v-show="genre" v-for="genre in  movie.genre" :key="genre.id">{{genre.name}}</span>
                                    </h6>
                                    <h6  class="card-subtitle mb-2 text-muted" v-else> API timeout</h6>
                                </b-col>
                            </b-row>
                            <b-row >
                                <b-col>
                                    <h5 class="card-title">Director</h5>
                                    <h6  class="card-subtitle mb-2 text-muted" v-if="omovie.director">{{omovie.director}}</h6>
                                    <h6  class="card-subtitle mb-2 text-muted" v-else> API timeout</h6>
                                </b-col>
                                <b-col>
                                    <h5  class="card-title">Writer</h5>
                                    <h6 class="card-subtitle mb-2 text-muted" v-if="omovie.writer && omovie.writer.length >= 100">{{omovie.writer.substring(0, 100)}}...</h6>
                                    <h6 class="card-subtitle mb-2 text-muted" v-else-if="omovie.writer && omovie.writer.length < 100">{{omovie.writer}}</h6>
                                    <h6  class="card-subtitle mb-2 text-muted" v-else> API timeout</h6>
                                </b-col>
                                <b-col>
                                    <h5 class="card-title">Year</h5>
                                    <h6 class="card-subtitle mb-2 text-muted" v-if="movie.year">{{movie.year}}</h6>
                                    <h6  class="card-subtitle mb-2 text-muted" v-else> API timeout</h6>
                                </b-col>
                            </b-row>


                            <b-row class="justify-content-md-center ">

                                <b-col>
                                    <h5 class="card-title">OMDB</h5>
                                    <h6 class="card-subtitle mb-2 text-muted" v-if="omovie.rating">{{omovie.rating}}</h6>
                                    <h6  class="card-subtitle mb-2 text-muted" v-else> API timeout</h6>
                                </b-col>
                                <b-col>
                                    <h5 class="card-title" >Pop Corn Time</h5>
                                    <h6 class="card-subtitle mb-2 text-muted" v-if="movie.rating_pop_corn">{{movie.rating_pop_corn}}</h6>
                                    <h6  class="card-subtitle mb-2 text-muted" v-else> API timeout</h6>
                                </b-col>
                                <b-col>
                                    <h5 class="card-title" cols="2">Tmdb</h5>
                                    <h6 class="card-subtitle mb-2 text-muted" v-if="movie.rating_tmdb">{{movie.rating_tmdb}}</h6>
                                    <h6  class="card-subtitle mb-2 text-muted" v-else> API timeout</h6>
                                </b-col>
                            </b-row>


                            <b-row >
                                <b-col>
                                    <h5 class="card-title">Language</h5>
                                    <h6 class="card-subtitle mb-2 text-muted" v-if="omovie.language">{{omovie.language}}</h6>
                                    <h6  class="card-subtitle mb-2 text-muted" v-else> API timeout</h6>
                                </b-col>
                                <b-col>
                                    <h5 class="card-title">Length</h5>
                                    <h6 class="card-subtitle mb-2 text-muted" v-if="omovie.length">{{omovie.length}}</h6>
                                    <h6  class="card-subtitle mb-2 text-muted" v-else> API timeout</h6>
                                </b-col>
                                <b-col>
                                    <h5 class="card-title">Country</h5>
                                    <h6 class="card-subtitle mb-2 text-muted" v-if="omovie.country">{{omovie.country}}</h6>
                                    <h6  class="card-subtitle mb-2 text-muted" v-else> API timeout</h6>
                                </b-col>
                            </b-row>
                        </b-container>

                        <hr style="border-top: transparent">
                        <b-container class="description" >
                            <b-card class="comment_item">
                                <b-media no-body>
                                    <b-media-aside  vertical-align="center">
                                        <button type="button" class="btn btn-success" @click="add_comment" style="width:80px;height:80px">Add</button>

                                    </b-media-aside>
                                    <b-media-body class="ml-3" >

                                        <b-form-textarea class="comment-text" v-validate="'max:500'" id="textarea" placeholder="Enter something..." rows="3" max-rows="6" @keyup.enter="add_comment" v-model="comment" name="comment"></b-form-textarea>

                                        <p v-show="errors.has('comment')" class="text-danger font-weight-light align-text-bottom">{{ errors.first('comment')}}</p>

                                    </b-media-body>


                                </b-media>
                            </b-card>
                            <b-card v-for="comment in comments" :key="comment.id" class="comment_item">
                                <b-media no-body>
                                    <b-media-aside @click="profile=comment.user;$bvModal.show('modal-scoped')" vertical-align="center" style="cursor: pointer">
                                        <b-img width="80" height="80" slot="aside" rounded="circle" :src="'http://localhost:8000' + comment.user['profile'].photo"    v-if="comment.user['profile'].photo && !comment.user['profile'].photo.startsWith('http')"></b-img>
                                        <b-img width="80" height="80" slot="aside" rounded="circle" :src="comment.user['profile'].photo"   v-else-if="comment.user['profile'].photo && comment.user['profile'].photo.startsWith('http')"></b-img>
                                        <b-img width="80" height="80" slot="aside" rounded="circle" :src="comment.user['profile'].photo_url"    v-else-if="comment.user['profile'].photo_url && comment.user['profile'].photo_url"></b-img>
                                    </b-media-aside>
                                    <b-media-body class="" >
                                        <div style="margin-left: -10vw">
                                            <span style="color: cornflowerblue;font-size: 13px"><i class="fas fa-user"></i>    {{comment.user.username}}    </span>
                                            <span style="color: lightslategrey;font-size: 13px"><i class="fa fa-clock-o"></i>    {{comment.created.slice(11, 16)}} | {{comment.created.slice(0, 10)}}</span>
                                        </div>

                                        <b-alert  variant="success" class="comment-text" show>{{comment.text}}</b-alert>
                                    </b-media-body>

                                </b-media>
                            </b-card>




                        </b-container>

                    </b-media-body>
                </b-media>
            </b-card>
        </div>

        <b-modal id="modal-scoped" :hide-footer=true  >
            <template slot="modal-header" slot-scope="{ close }">
                <!-- Emulate built in modal header close button action -->
                <b-button size="sm" variant="outline-danger" @click="close()">
                    Close
                </b-button>
            </template>

            <template slot="default" slot-scope="{ hide }">
                <p><strong>Login</strong> {{profile.username}}</p>
                <p><strong>Name</strong> {{profile.first_name}} {{profile.last_name}}</p>
                <p><strong>Language</strong> {{profile['profile'].language}}</p>

                <img :src="'http://localhost:8000' + profile['profile'].photo" alt="..." class="img-thumbnail"   v-if="profile['profile'].photo && !profile['profile'].photo.startsWith('http')">
                <img :src="profile['profile'].photo" alt="..." class="img-thumbnail"  v-if="profile['profile'].photo && profile['profile'].photo.startsWith('http')">
                <img :src="profile['profile'].photo_url" alt="..." class="img-thumbnail"  v-else-if="profile['profile'].photo_url && profile['profile'].photo_url">

            </template>

            <template slot="modal-footer" slot-scope="{ ok, cancel, hide }">
                <b-button size="sm" variant="success" @click="ok()">
                    OK
                </b-button>
                <b-button size="sm" variant="danger" @click="cancel()">
                    Cancel
                </b-button>
            </template>
        </b-modal>



    </div>

</template>



<script>

    import 'video.js/dist/video-js.css'
    import { videoPlayer } from 'vue-video-player'

    import axios from 'axios';
    import videojs from 'video.js'

    export default {
        name: 'movie',
        components: {
            // Alert,
            videoPlayer
        },
        data() {
            return {
                aspectRatio: 264/640,
                language: null,
                comments:[],
                comment:null,
                username:null,
                id:null,
                movie:null,
                omovie:{},
                profile:{},
                imdb_id:null,
                backdrop:null,
                comment_id:null,
                track_list: [ {}],
                playerOptions: {
                    // videojs options
                    muted: false,
                    language: 'en',
                    playbackRates: [0.7, 1.0, 1.5, 2.0],
                    sources: null,
                    poster: "",
                    width: window.innerWidth/2,
                    height: window.innerWidth/2 * 264/640,

                },
                loading:false,
                // my_width:  window.innerWidth/2,
                my_width:  window.innerWidth/2,
            }
        },
        mounted() {
            this.$store.dispatch('authenticate').then(res => {
                if (!res) this.$router.push('/login');
                else
                {
                    axios.defaults.headers.common['Authorization'] = 'JWT ' + this.$store.getters.getToken;
                    // this.username = this.$store.getters.getUsername;
                    this.id = this.$route.params.id;
                    this.imdb_id = this.$route.params.imdb_id;
                    this.get_movie_info();
                    this.get_language()
                }
            });
            window.onresize = this.resizeVideoJS;
        },
        methods:{
            resizeVideoJS(){
                if (document.getElementById('video') && document.getElementById('player_info')) {
                    var width = document.getElementById('video').parentElement.offsetWidth;
                    this.playerOptions.width = width
                    this.playerOptions.height = width * this.aspectRatio
                    this.my_width = width
                }
            },
            get_language(){
                axios.defaults.headers.common['Authorization'] = 'JWT ' + this.$store.getters.getToken;
                axios({url: 'http://localhost:8000/auth/user/get_user/', method: 'GET'})
                    .then(res => {
                        this.language = res.data.profile.language
                    })
            },
            /**
             * videoplayer methods
             **/
            startPlayer() {
                 this.$store.dispatch('authenticate').then(res => {
                     if (!res) this.$router.push('/login');
                     else {
                         if (this.loading !== true) {
                             this.loading = true;
                             let self = this
                             axios.defaults.headers.common['Authorization'] = 'JWT ' + this.$store.getters.getToken;
                             let url = 'http://localhost:8000/movie/player/start?id=' + this.movie.id;
                             axios.get(url).then(function (res) {
                                if (!res.data.prout) {
                                 self.$bvModal.show('player-modal');
                                 window.setTimeout(function () {
                                     self.resizeVideoJS();
                                 }, 300);
                                 self.loading = false;
                                 self.playerOptions.sources = [{
                                     type: "video/mp4",
                                     src: "http://localhost:8082/stream?media_id=" + res.data.media_id
                                 }]
                                 self.playerOptions.tracks = []
                                 if (res.data.en !== "") {
                                     self.playerOptions.tracks.push({
                                         kind: 'captions',
                                         label: 'English',
                                         srclang: 'en',
                                         src: "http://localhost:8082/" + res.data.en
                                     })
                                 }
                                 if (res.data.fr !== "") {
                                     self.playerOptions.tracks.push({
                                         kind: 'captions',
                                         label: 'French',
                                         srclang: 'fr',
                                         src: "http://localhost:8082/" + res.data.fr
                                     })
                                 }
                                 self.playerOptions.tracks.forEach(function (el) {
                                     if (el.srclang === self.language)
                                         el.default = true;
                                 })
                                 var progress = setInterval(function (media_id) {
                                     var prct, rate
                                     if (prct === "100") {
                                         cleanInterval(progress)
                                     } else {
                                         axios.get("http://localhost:8082/info?media_id=" + res.data.media_id)
                                             .then(function (res) {
                                                 prct = res.data.prct;
                                                 rate = res.data.rate;
                                                 $("#prct_downloaded").html(prct)
                                                 $("#rate_downloaded").html(rate)
                                             })
                                     }
                                 }, 2000);
                                } else {self.loading = false;}
                             });
                         }
                     }
                 })
            },
            /**
             * Retrieve movie infos from database
             **/
            get_movie_info(){
                this.$store.dispatch('authenticate').then(res => {
                    if (!res) this.$router.push('/login');
                    else
                    {
                        axios.defaults.headers.common['Authorization'] = 'JWT ' + this.$store.getters.getToken;
                        let url = 'http://localhost:8000/movie/list/movie/?id='+this.id;
                        let self = this;
                        axios.get(url).then(async (res) => {
                            if (res.data.success && res.data.movie.imdb_id === self.imdb_id) {
                                self.movie = res.data.movie;
                                await self.query_omdb();
                                await self.get_comments();
                            } else
                                self.$router.push('/');
                        });
                    }
                })
            },
            /**
             * Retrieve more movie info from OMDB api
             * */
            async query_omdb(){
                delete axios.defaults.headers.common['Authorization'];
                let url = 'http://www.omdbapi.com/?apikey=726643cb&i=' + this.imdb_id;
                let self = this;
                axios.get(url).then(async function (res) {
                    self.omovie.casting = res.data.Actors;
                    self.omovie.director = res.data.Director;
                    self.omovie.country = res.data.Country;
                    self.omovie.language = res.data.Language;
                    self.omovie.production = res.data.Production;
                    self.omovie.writer = res.data.Writer;
                    self.omovie.length = res.data.Runtime;
                    self.omovie.rating = res.data.Rated;

                    self.query_tmdb_images();
                });
            },
            /**
             * Retrieve backdrop movie image from TMDB api
             * */
            query_tmdb_images(){
                let url = 'https://api.themoviedb.org/3/movie/' + this.imdb_id + '/images?api_key=dfcc7fd8cc1b8c0b5bae5f339b7a27c0';
                delete axios.defaults.headers.common['Authorization'];
                let self = this;
                axios.get(url).then(function (res) {
                    if (res && res.data && res.data.backdrops && res.data.backdrops[0])
                    // console.log(res.data.backdrops[0]);
                    self.backdrop = 'http://image.tmdb.org/t/p/original' + res.data.backdrops[0].file_path;
                });
                // }
                // })
            },
            /**
             * Get all movie comments from database
             */
            get_comments(){
                axios.defaults.headers.common['Authorization'] = 'JWT ' + this.$store.getters.getToken;
                this.comments = [];
                let self=this;
                let url = 'http://localhost:8000/movie/comment/'+this.id;
                axios.get(url).then(function (res) {
                    if (res && res.data)
                    {
                        res.data.forEach(function (comment) {
                            self.comments.push(comment);
                        })
                    }
                })
            },
            add_comment()
            {
                if (!this.errors.has('comment') && this.comment) {
                    let self = this;
                    this.$store.dispatch('authenticate').then(res => {
                        if (!res) this.$router.push('/login');
                        else {

                            axios.defaults.headers.common['Authorization'] = 'JWT ' + this.$store.getters.getToken;
                            let url = 'http://localhost:8000/movie/comment/';
                            let data1 = {'movie_id': this.id, 'text': this.comment};
                            axios.post(url, data1).then(function (res) {
                                // console.log(res)
                                self.comments.unshift(res.data);
                                self.comment = null;
                            });
                        }

                    });
                }

            },
        }
    }
</script>

<style scoped>

    .video-js-responsive-container.vjs-hd {
        padding-top: 56.25%;
    }
    .video-js-responsive-container.vjs-sd {
        padding-top: 75%;
    }
    .video-js-responsive-container {
        width: 100%;
        position: relative;
    }
    .video-js-responsive-container .video-js {
        height: 100% !important;
        width: 100% !important;
        position: absolute;
        top: 0;
        left: 0;
    }

    #cover_film{
        display: block!important;
    }
    .comment_item{
        background-color: #F0F0ED;
        opacity: 0.85;
        border:none;
        border-radius: unset
    }




    .description {
        font-size: 16px;
        /*line-height: 26px;*/
        /*padding-left: 10vw;*/
        color: #B1B0AC;
        /*background-color: transparent;*/
        border: none;
        z-index: 30!important;
        background-color: #F0F0ED;
        opacity: 0.85;
        /*height: 20vw;*/
        padding: 1vw;
    }

    .cover {
        /*position: absolute;*/
        margin-top: 5vw;
        margin-left: 5vw;
        z-index: 2;
        width: 20vw;
        cursor: pointer;
    }

    .player_icon {
        top: 20vw;
        left: 19vw;
        z-index: 3;
        position: absolute;
        transform: translate(-50%, -50%);
        cursor: pointer;
        font-size: 10vw;
        opacity: 0.6;
    }


    @media only screen and (max-width: 760px) {
        .cover {
            /*position: absolute;*/
            margin-top: 5vw;
            /*margin-left: 10vw;*/
            width: 30vw;
        }
        .player_icon {
            top: 28vw;
            left: 48vw;
            z-index: 3;
            position: absolute;
            transform: translate(-50%, -50%);
            cursor: pointer;
            font-size: 16vw;
            opacity: 0.6;
        }


    }

    .comment-text{
        /*max-width: 50%;*/
        margin-left: 2vw;
    }

    @media  screen and (min-width: 200px) {
        .comment-text{
            width: 55vw!important;
        }
    }
    @media  screen and (min-width: 600px) {
        .comment-text{
            width: 50vw!important;
            max-width: 80%;
        }
    }
    @media  screen and (min-width: 700px) {
        .comment-text{
            width: 60%;
            max-width: 60%;
        }
    }
    @media  screen and (min-width: 760px) {
        .comment-text{
            width: 50%;
            max-width: 50%;
        }
    }
    @media  screen and (min-width: 1000px) {
        .comment-text{
            width: 60%;
            max-width: 65%;
        }
    }
    @media  screen and (min-width: 1400px) {
        .comment-text{
            width: 80%;
            max-width: 70%;
        }
    }


    .tag {
        background: white;
        border-radius: 10px;
        padding: 3px 8px;
        font-size: 14px;
        margin-right: 4px;
        line-height: 35px;
        cursor: pointer;
    }

    .tag:hover {
        background: #ddd;
    }




    fieldset, label {
        margin: 0;
        padding: 0;
    }




    /* hero */
    .hero-image {
        /*background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5));*/
        height: 15vw;
        background-position: center;
        background-repeat: no-repeat;
        background-size: cover;
        position: relative;
    }

    .hero-text {
        color: white;
        font-size: 44px;
        border-radius: 5px;
        text-align: center;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
    }

    .hero-text button {
        border: none;
        outline: 0;
        display: inline-block;
        padding: 10px 25px;
        color: black;
        background-color: #ddd;
        text-align: center;
        cursor: pointer;
    }

    .hero-text button:hover {
        background-color: #555;
        color: white;
    }

    .card-img-overlay {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        padding: 1.25rem;
        background: rgba(255, 255, 255, 0) linear-gradient(to bottom, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 1) 90%) repeat scroll 0 0;}


</style>