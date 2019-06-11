<template>
    <b-container class='page-container'>
        <b-row class='justify-content-center'>
            <b-col sm="12">
                <b-card>
                    <b-row v-if='isLoading' class='justify-content-center'>
                        <grid-loader color='#00274c'></grid-loader>
                    </b-row>
                    <div v-else-if='profile'>
                        <h1>Welcome to CFBDemic Allies!</h1>
                    </div>
                    <div class='login' v-else>
                        <h1>
                            CFBDemic Allies
                        </h1>
                        <h3 class='lead'>
                            Login using Reddit:
                        </h3>
                        <b-link href='/auth/reddit' class='text-danger'>
                            <font-awesome-icon :icon="['fab', 'reddit']" size='3x'></font-awesome-icon>
                        </b-link>
                    </div>
                </b-card>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
export default {
    props: ['profile', 'isLoading']
}
</script>

<style lang='scss'>

</style>
