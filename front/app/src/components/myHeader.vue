<template>
    <div id="nav">
        <nav class="navbar navbar-expand-lg navbar-dark primary-color">
            <router-link to="/" class="nav-link">Hypertube <span class="sr-only">(current)</span></router-link>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
                    aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation" style="background-color:whitesmoke ">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item">
                        <router-link to="/login" class="nav-link" v-if="status!=='success'"> Login  <span class="sr-only">(current)</span> </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/about" class="nav-link" v-if="status==='success'"> User Area <span class="sr-only">(current)</span> </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="#" class="nav-link" v-if="status==='success'" v-on:click.native="logout">Logout <span class="sr-only">(current)</span> </router-link>
                    </li>
                </ul>

            </div>
        </nav>
    </div>
</template>


<script>

    export default {
        name: 'myHeader',
        mounted() {
            this.$store.dispatch('authenticate').then(res => {
                if (!res) {
                    this.$router.push('/login');
                }
            })
        },
        computed: {
            status() {
                return this.$store.getters.authStatus;
            },
        },
        methods: {

            logout(){
                this.$store.dispatch('logout');
                this.$router.push('/login')
            }
        },
        watch: {
            status() {
                if (this.status !== "success"){
                    this.$router.push('/login');
                }
            },
        },
    }

</script>

<style scoped>
    #nav {
        padding: 30px;
    }
    #nav a {
        font-weight: bold;
        color: #2c3e50;
    }
    #nav a.router-link-exact-active {
        color: #42b983;
    }

</style>