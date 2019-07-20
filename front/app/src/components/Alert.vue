<template>
    <div>
        <b-alert variant="success" show v-if="is_success" dismissible>{{msg}}</b-alert>
        <div v-if="is_error">
            <b-alert v-model="showDismissibleAlert" variant="danger" dismissible fade show>
                {{msg}}
            </b-alert>
        </div>

    </div>
</template>


<script>
    export default {
        name: 'Alert',
        props: {
            msg: String,
            is_success: Boolean,
            is_error: Boolean
        },
        data() {
            return {
                showDismissibleAlert: true
            }
        },
        methods: {}

    }
</script>

<style scoped>
    h3 {
        margin: 40px 0 0;
    }
    ul {
        list-style-type: none;
        padding: 0;
    }
    li {
        display: inline-block;
        margin: 0 10px;
    }
    a {
        color: #42b983;
    }
</style>
