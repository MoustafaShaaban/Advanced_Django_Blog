import { createApp, h } from 'vue'
import { createPinia } from 'pinia'
import { Quasar, Notify, Dialog, Dark, Cookies } from 'quasar'
import { VueQueryPlugin } from '@tanstack/vue-query'
import { ApolloClient, createHttpLink, InMemoryCache } from '@apollo/client/core'
import { createApolloProvider } from '@vue/apollo-option'
import VueApolloComponents from '@vue/apollo-components'

// Import icon libraries
import '@quasar/extras/material-icons/material-icons.css'
import '@quasar/extras/fontawesome-v5/fontawesome-v5.css'

// Import Quasar css
import 'quasar/src/css/index.sass'

import App from './App.vue'
import router from './router'

const app = createApp({
    render: () => h(App),
})

const cache = new InMemoryCache()

const apolloClient = new ApolloClient({
    cache,
    uri: 'http://localhost:8000/graphql/',
    credentials: 'include',
    headers: {
        'X-CSRFToken': Cookies.get('csrftoken')
    }
})


const apolloProvider = createApolloProvider({
    defaultClient: apolloClient,
})

app.use(createPinia())
app.use(router)

app.use(Quasar, {
    plugins: {
        Notify,
        Dialog,
        Dark,
        Cookies,
    }
})

app.use(VueQueryPlugin)

app.use(apolloProvider)
app.use(VueApolloComponents)

app.mount('#app')
