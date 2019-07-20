<template>
    <div class="home" v-if="status==='success'">
        <!--MODALS-->
        <div>
            <!-- YEAR MODAL-->
            <b-modal id="year-modal">
                <template slot="modal-header" slot-scope="{ close }">
                    <!-- Emulate built in modal header close button action -->
                    <b-button size="sm" variant="outline-danger" @click="close()">
                        Close Modal
                    </b-button>
                </template>
                <template slot="default" slot-scope="{ hide }">

                    <label for="year-range-min">Starting year</label>

                    <b-form-input v-validate="'digits:4|numeric|min_value:1900|max_value:2019'" id="year-range-min" v-model="year_min_input" type="range" min="1900" max="2019" name="year min"></b-form-input>
                    <div class="mt-2">
                        <span>Value: {{ year_min_input }}</span>
                        <p v-show="errors.has('year min')" class="text-danger">{{ errors.first('year min') }}</p>
                    </div>
                    <br>
                    <label for="year-range-max">Ending year</label>
                    <b-form-input v-validate="'digits:4|numeric|min_value:1900|max_value:2019'" id="year-range-max" v-model="year_max_input" type="range" min="1900" max="2019"  name="year max"></b-form-input>
                    <div class="mt-2">
                        <span>Value: {{ year_max_input }}</span>
                        <p v-show="errors.has('year max')" class="text-danger">{{ errors.first('year max') }}</p>
                        <p v-show="!errors.has('year min') && !errors.has('year max') && year_min_input > year_max_input" class="text-danger">Invalid range selected.</p>
                    </div>
                </template>
                <template slot="modal-footer" slot-scope="{close, ok, cancel, hide }">
                    <b-button size="sm" variant="success" @click="close();detect_change('year')" :disabled="errors.items.length !== 0 || year_min_input > year_max_input">OK</b-button>
                </template>
            </b-modal>
            <!-- YEAR MODAL END-->

            <!-- RATING MODAL-->
            <b-modal id="rating-modal">
                <template slot="modal-header" slot-scope="{ close }">
                    <!-- Emulate built in modal header close button action -->
                    <b-button size="sm" variant="outline-danger" @click="close()">
                        Close Modal
                    </b-button>
                </template>

                <template slot="default" slot-scope="{ hide }">

                    <label for="rating-range-min">Rating min</label>
                    <b-form-input v-validate="{ decimal: [1, '.'], min_value:0.0, max_value:10.0}" id="rating-range-min" v-model="rating_min_input" type="range" min="0" max="10" step="0.1" name="rating min"></b-form-input>
                    <div class="mt-2">
                        <span>Value: {{ rating_min_input }}</span>
                        <p v-show="errors.has('rating min')" class="text-danger">{{ errors.first('rating min') }}</p>
                    </div>

                    <label for="rating-range-max">Rating max</label>
                    <b-form-input v-validate="{ decimal: [1, '.'], min_value:0.0, max_value:10.0}" id="rating-range-max" v-model="rating_max_input" type="range" min="0" max="10" step="0.1" name="rating max"></b-form-input>
                    <div class="mt-2">
                        <span>Value: {{ rating_max_input }}</span>
                        <p v-show="errors.has('rating max')" class="text-danger">{{ errors.first('rating max') }}</p>
                        <p v-show="!errors.has('rating min') && !errors.has('rating max') && parseFloat(rating_min_input) > parseFloat(rating_max_input)" class="text-danger">Invalid range selected.</p>
                    </div>

                </template>

                <template slot="modal-footer" slot-scope="{close, ok, cancel, hide }">
                    <b-button size="sm" variant="success" @click="close();detect_change('rating')" :disabled="errors.items.length !== 0 || parseFloat(rating_min_input) > parseFloat(rating_max_input)">OK</b-button>
                </template>
            </b-modal>
            <!-- RATING MODAL END -->


            <!-- TITLE MODAL -->
            <b-modal id="title-modal">
                <template slot="modal-header" slot-scope="{ close }">
                    <!-- Emulate built in modal header close button action -->
                    <b-button size="sm" variant="outline-danger" @click="close()">
                        Close Modal
                    </b-button>
                </template>

                <template slot="default" slot-scope="{ hide }">

                    <label for="year-range-min">Title</label>
                    <b-form-input v-validate="'min:1|max:50'" type="text" v-model="title_input" placeholder="name" name="title"></b-form-input>
                    <div class="mt-2">
                        <span v-show="errors.has('title')">{{ errors.first('title') }}</span>
                    </div>
                </template>

                <template slot="modal-footer" slot-scope="{close, ok, cancel, hide }">
                    <b-button size="sm" variant="success" @click="close();detect_change('title')" :disabled="errors.items.length !== 0">OK</b-button>
                </template>
            </b-modal>
            <!-- TITLE MODAL END-->


            <!-- GENRE MODAL -->
            <b-modal id="genre-modal">
                <template slot="modal-header" slot-scope="{ close }">
                    <!-- Emulate built in modal header close button action -->
                    <b-button size="sm" variant="outline-danger" @click="close()" >
                        Close Modal
                    </b-button>
                </template>
                <b-form-select v-model="genre_input" :options="options" name="genre_select">
                    <template slot="first">
                        <option :value="null" disabled> Please select a genre </option>
                    </template>
                </b-form-select>
                <template slot="modal-footer" slot-scope="{close, ok, cancel, hide }">
                    <b-button size="sm" variant="success" @click="close();detect_change('genre')" :disabled="errors.items.length !== 0 || !options.includes(genre_input)">OK</b-button>
                </template>
            </b-modal>
            <!-- GENRE MODAL END -->
        </div>
        <!-- MODALS END-->

        <b-row>
            <b-col cols=12 class="col-lg-4 col-md-6 col-sm-12">
                <!-- FILTERS BUTTONS -->
                <b-button-group>
                    <b-button disabled variant="dark"><i class="fas fa-filter"></i> filter</b-button>
                    <b-button @click="$bvModal.show('title-modal')" variant="primary">title</b-button>
                    <b-button @click="$bvModal.show('year-modal')" variant="primary">year</b-button>
                    <b-button @click="$bvModal.show('rating-modal')" variant="primary">rating</b-button>
                    <b-button @click="$bvModal.show('genre-modal')" variant="primary">genre</b-button>
                </b-button-group>
            </b-col>
            <b-col cols=12 class="col-lg-4 col-md-6 col-sm-12">
                <!-- SORTERS BUTTONS -->
                <b-button-group class="btn-group btn-group-toggle" >
                    <b-button disabled variant="dark"><i class="fas fa-sort"></i> sort</b-button>
                    <b-button :class="[sort_by === 'title' ? 'btn-info active' : 'btn-info']" @click="detect_sort_change('title')">Title</b-button>
                    <b-button :class="[sort_by === 'year' ? 'btn-info active' : 'btn-info']" @click="detect_sort_change('year')">Year</b-button>
                    <b-button :class="[sort_by === 'rating' ? 'btn-info active' : 'btn-info']" @click="detect_sort_change('rating')">Rating</b-button>
                </b-button-group>
            </b-col>
            <b-col cols=12 class="col-lg-4 col-md-3 col-sm-12 col-md-offset-8">
                    <b-button variant="danger" @click="reset">Reset</b-button>
            </b-col>

        </b-row>

        <br>
        <!--        FILTER TAGS -->
        <b-row>
            <b-col>
                <div>
                    <button type="button" class="btn btn-labeled btn-primary" v-if="title">
                        <span class="btn-label" @click="title = null">
                            <i class="fas fa-times"></i>
                        </span>{{title}}
                    </button>
                    <button type="button" class="btn btn-labeled btn-primary" v-if="year.length">
                        <span class="btn-label" @click="year = []">
                            <i class="fas fa-times"></i>
                        </span>{{year[0]}} - {{year[1]}}
                    </button>
                    <button type="button" class="btn btn-labeled btn-primary" v-if="rating.length">
                        <span class="btn-label" @click="rating = []">
                            <i class="fas fa-times"></i>
                        </span>{{rating[0]}} - {{rating[1]}}
                    </button>
                    <button type="button" class="btn btn-labeled btn-primary" v-if="genre">
                        <span class="btn-label" @click="genre = null">
                            <i class="fas fa-times"></i>
                        </span>{{genre}}
                    </button>
                </div>
            </b-col>
        </b-row>
        <!--        FILTER TAGS END-->

        <div class="container">
            <router-link class="movie-card" v-for="movie in movies"  :key="movie.id" :to="{ name: 'Movie', params:{id:movie.id, imdb_id:movie.imdb_id}}" target="_blank" >

                <div class="movie-header" v-bind:style="{ background: 'url(' + movie.thumbnail + ')' }" style="background-size: cover!important;">
                    <i class="fas fa-eye header-icon" v-if="movie.vu"></i></div>
                <!--movie-header-->
                <div class="movie-content">
                    <div class="movie-content-header">
                        <a href="#">
                            <h3 class="movie-title">{{movie.title}}</h3>
                        </a>
                    </div>
                    <div class="movie-info">
                        <div class="info-section">
                            <label>Year</label>
                            <span>{{movie.year}}</span>
                        </div>
                        <!--date,time-->
                        <div class="info-section">
                            <label>Genre</label>
                            <div  v-for="(genre,index) in  movie.genre" :key="index">
                                <span v-if="index < 3">{{genre.name}}</span>
                            </div>
                        </div><!--screen-->
                        <div class="info-section">
                            <label >Rating <span></span></label>
                            <div   v-if="movie.rating_tmdb">
                                <span >{{movie.rating_tmdb}}</span>
                            </div>
                        </div><!--row-->

                    </div>
                    <br>
                    <div class="">
                        <label></label>
                        <span v-if="movie.synopsis">{{movie.synopsis.substring(0, 100)}}...</span>
                    </div><!--row-->

                </div><!--movie-content-->
            </router-link><!--movie-card-->
            <button class="btn btn-info" style="position:fixed;bottom:20px;right: 20px" @click="go_up">
                <i class="fas fa-chevron-up"></i>
            </button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import { mapState } from 'vuex';
    export default {
        name: 'home',
        data() {
            return {
                is_success: false,
                is_error: false,
                movies:[],
                indexes:[],
                page:1,
                page_limit:null,
                token:localStorage.getItem('token'),
                flag: 1,
                sort_by:null,
                // filtering
                title:null,
                rating:[],
                year:[],
                genre:null,
                //filtering input
                title_input:null,
                // rating_input:null,
                year_min_input:1900,
                year_max_input:2019,
                rating_min_input:0.0,
                rating_max_input:10.0,
                genre_input:null,
                movies_names:[],
                api:'tmdb',
                type:null,
                limit : false,
                //genres
                options: [],
                fontSize: '1.5rem',
                normSize: '1rem'
            }
        },
        computed: {
            status() {
                return this.$store.getters.authStatus;
            },
            active_filters() {
                return this.title, this.year, this.genre, this.rating, this.sort_by, Date.now();
            }
        },
        mounted(){
            this.$store.dispatch('authenticate').then(res => {
                if (!res || this.status !== 'success') {
                    // console.log('HOME LOGOUT')
                    this.$store.dispatch('logout');
                    this.$router.push('/login');
                }
                else
                    axios.defaults.headers.common['Authorization'] = 'JWT ' + this.$store.getters.getToken;
            });
            document.documentElement.scrollTop = 0;
            this.get_films();
            this.get_genres();
            this.scroll();

        },
        methods: {
            /**
             * UTILITIES
             **/
            go_up(){
                window.scrollTo(0,0);
            },
            reset() {
                //reset sorters
                this.sort_by = null;
                //reset filters
                this.title = null;
                this.year.length = 0;
                this.genre = null;
                this.rating.length = 0;
                //reset inputs
                this.title_input = null;
                this.year_min_input = 1900;
                this.year_max_input = 2019;
                this.rating_min_input = 0;
                this.rating_max_input = 9.9;
                this.genre_input = null;
                this.rating_input = null;
                //reset movies and retrieve them
                this.page = 1;
                this.movies = [];
                this.limit = false;
                this.get_films();
            },
            detect_change(value) {
                if (!this.errors.items.length)
                {
                    if (value === 'title') this.title = this.title_input;
                    else if (value === 'year'){
                        if (this.year_max_input >= this.year_min_input)
                            this.year = [this.year_min_input, this.year_max_input];
                    }
                    else if (value === 'rating') {
                        if (this.rating_max_input >= this.rating_min_input)
                            this.rating = [this.rating_min_input, this.rating_max_input]; // todo check come year
                    }
                    else if (value === 'genre')
                        if (this.options.includes(this.genre_input))
                            this.genre = this.genre_input;
                }
            },
            detect_sort_change(value){
                this.sort_by = value;
            },
            /**
             * Get all genres for select modal
             * */
            get_genres:function()
            {
                this.$store.dispatch('authenticate').then(res => {
                    if (!res) this.$router.push('/login');
                    else {
                        axios.defaults.headers.common['Authorization'] = 'JWT ' + this.$store.getters.getToken;
                        let url = 'http://localhost:8000/movie/list/genre';
                        let self = this;
                        axios.get(url).then(res => {
                            if (res && res.data && res.data.success) {
                                res.data.genres.forEach(function (el) {
                                    self.options.push(el)
                                })
                            }
                        });
                    }
                })
            },
            // Home on arrival
            get_films: function () {
                this.$store.dispatch('authenticate').then(res => {
                    if (!res) this.$router.push('/login');
                    else
                    {
                        axios.defaults.headers.common['Authorization'] = 'JWT ' + this.$store.getters.getToken;
                        // console.log("get films called");
                        let url = 'http://localhost:8000/movie/list/page/?page=' + this.page;
                        this.page++;
                        this.query_db(url);

                    }
                })
            },
            /**
             * SCROLL ZONE
             **/
            scroll() {
                window.onscroll = () => {
                    let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight >= document.documentElement.offsetHeight;

                    if (bottomOfWindow) {
                        let filters = !!(this.title || this.year.length || this.genre || this.rating.length);
                        this.$store.dispatch('authenticate').then(res => {
                            if (!res) this.$router.push('/login');
                            else
                            {
                                axios.defaults.headers.common['Authorization'] = 'JWT ' + this.$store.getters.getToken;
                                if (!this.limit)
                                {
                                    if (filters && !this.sort_by)
                                        this.filter();
                                    else if (this.sort_by)
                                        this.sort(this.sort_by);
                                    else
                                        this.get_films();
                                }
                            }
                        })

                    }
                };
            },
            /**
             * FILTER
             */
            filter() {
                this.$store.dispatch('authenticate').then(res => {
                    if (!res) this.$router.push('/login');
                    else
                    {
                        axios.defaults.headers.common['Authorization'] = 'JWT ' + this.$store.getters.getToken;
                        let url = 'http://localhost:8000/movie/list/filter/?page=' + this.page;
                        if (this.title) url += '&title=' + this.title;
                        if (this.year.length) url += '&year_min=' + this.year[0] + '&year_max=' + this.year[1];
                        if (this.genre) url += '&genre=' + this.genre;
                        if (this.rating.length) url += '&rating_min=' + this.rating[0] + '&rating_max=' + this.rating[1];
                        if (this.sort_by) url += '&sort=' + this.sort_by;
                        this.page++;
                        this.query_db(url);
                    }
                })
            },
            /**
             * SORT
             * */
            sort(type) {
                this.$store.dispatch('authenticate').then(res => {
                    if (!res) this.$router.push('/login');
                    else
                    {
                        axios.defaults.headers.common['Authorization'] = 'JWT ' + this.$store.getters.getToken;
                        if (!this.sort_by || type !== this.sort_by) {
                            this.page = 1;
                            this.movies = [];
                        }
                        this.sort_by = type;
                        let filters = !!(this.title || this.year.length || this.genre || this.rating.length);
                        if (filters) this.filter();
                        else
                        {
                            let url = 'http://localhost:8000/movie/list/sort/?type=' + type + '&page=' + this.page;
                            this.page++;
                            this.query_db(url);
                        }
                    }
                })

            },
            /**
             * REQUEST
             * */
            query_db(url){
                let self = this;
                if (this.page === 1) this.movies = []; // avoids click repetition errors (duplicates)
                axios.get(url).then(res => {
                    if (res.data && res.data.success)
                    {
                        res.data.movies.forEach(movie => self.movies.push(movie));
                        self.limit = res.data.movies.length < 10;
                    }
                    else
                        self.limit = true;
                });
            }
        },
        watch: {
            active_filters(){
                let filters = !!(this.title || this.year.length || this.genre || this.rating.length);

                 if (filters)
                {
                    this.page = 1;
                    this.movies = [];
                    this.filter();
                }
                 else if (this.sort_by && !filters)
                 {
                     this.page = 1;
                    this.movies = [];
                    this.sort(this.sort_by);
                 }
                 else
                {
                    this.page = 1;
                    this.movies = [];
                    this.get_films();
                }

            },
            token: function () {
                if (this.token !== this.$store.state.token)
                {

                    this.$store.dispatch('logout');
                    this.$router.push('/login')
                }

            }
        }
    }
</script>


<style scoped>
    /*tags*/
    .btn-label {
        position: relative;
        left: -12px;
        display: inline-block;
        padding: 6px 12px;
        background: rgba(0,0,0,0.15);
        border-radius: 3px 0 0 3px;
    }
    .btn-labeled {
        padding-top: 0;
        padding-bottom: 0;
    }
    .btn {
        margin-bottom:10px;
    }

    body {
        height: 100%;
        width: 100%;
        background: #e9e9e9;
        font-family: 'Arimo', Arial, sans-serif;
        font-weight: 400;
        font-size: 14px;
        color: #010b26;
    }

    * {
        -webkit-transition: 300ms;
        transition: 300ms;
    }

    ul {
        list-style-type: none;
    }

    h1, h2, h3, h4, h5, p {
        font-weight: 400;
    }

    a, a:hover{
        text-decoration: none;
        color: inherit;
    }


    .container {
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -ms-flex-wrap: wrap;
        flex-wrap: wrap;
        max-width: 100%;
        margin-top: 10vh;
        margin-left: auto;
        margin-right: auto;
        -webkit-box-pack: center;
        -ms-flex-pack: center;
        justify-content: center;
    }

    .movie-card {
        background: #ffffff;
        box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.1);
        width: 100%;
        max-width: 315px;
        margin: 2em;
        border-radius: 10px;
        display: inline-block;
    }

    .movie-header {
        padding: 0;
        margin: 0;
        height: 500px;
        width: 100%;
        display: block;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        background-size: cover!important;
    }


    .header-icon {
        width: 100%;
        height: 367px;
        line-height: 367px;
        text-align: center;
        vertical-align: middle;
        margin: 0 auto;
        color: #ffffff;
        font-size: 54px;
        text-shadow: 0px 0px 20px #6abcea, 0px 5px 20px #6ABCEA;
        opacity: .85;
    }

    .header-icon:hover {
        background: rgba(0, 0, 0, 0.15);
        font-size: 74px;
        text-shadow: 0px 0px 20px #6abcea, 0px 5px 30px #6ABCEA;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        opacity: 1;
    }

    .movie-card:hover {
        -webkit-transform: scale(1.03);
        transform: scale(1.03);
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.08);
    }

    .movie-content {
        padding: 18px 18px 24px 18px;
        margin: 0;
    }

    .movie-content-header, .movie-info {
        display: table;
        width: 100%;
    }

    .movie-title {
        font-size: 24px;
        margin: 0;
        display: table-cell;
    }

    .movie-info {
        margin-top: 1em;
    }

    .info-section {
        display: table-cell;
        text-transform: uppercase;
        text-align: center;
    }

    .info-section:first-of-type {
        text-align: left;
    }

    .info-section:last-of-type {
        text-align: right;
    }

    .info-section label {
        display: block;
        color: rgba(0, 0, 0, 0.5);
        margin-bottom: .5em;
        font-size: 9px;
    }

    .info-section span {
        font-weight: 700;
        font-size: 11px;
    }

    @media screen and (max-width: 500px) {
        .movie-card {
            width: 95%;
            max-width: 95%;
            margin: 1em;
            display: block;
        }

        .container {
            padding: 0;
            margin: 0;
        }
    }


</style>
