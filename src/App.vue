<template>
    <div id="app">
        <navigation :profile='profile'></navigation>
        <router-view :profile='profile' :is-loading='isLoading' />
    </div>
</template>

<script>
    import Navigation from '@/components/Navigation.vue';

    export default {
        components: {
            Navigation
        },
        data() {
            return {
                profile: null,
                isLoading: false
            };
        },
        created() {
            this.isLoading = true;
            this.$axios.get('/api/me').then((result) => {
                this.profile = result.data;
                this.isLoading = false;
            }).catch(() => {
                this.profile = null;
                this.isLoading = false;
            })
            .finally(() => {
                this.isLoading = false;
            });
        }
    };

</script>


<style lang="scss">

    body {
        background: #dedede;
    }

    .spinner-container {
        margin-top: 4em;
    }

    div[class*="col-"],
    .col {
        margin-top: 2em;
    }

    .bottom-row {
        margin-bottom: 2em;
    }

    .page-container {
        margin-top: 2em;

        .title-card {
            .row {
                margin-bottom: 0;
            }

            div[class*="col-"],
            .col {
                margin-top: 0;
            }
        }
    }

    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
    }

    #nav {
        padding: 30px;

        a {
            font-weight: bold;
            color: #2c3e50;

            &.router-link-exact-active {
                color: #42b983;
            }
        }
    }

</style>
