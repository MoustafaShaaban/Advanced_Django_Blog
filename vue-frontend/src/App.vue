<template>
  <div class="">
    <q-layout view="hHh lpR fFf">

      <q-header reveal elevated class="bg-primary text-white">
        <q-toolbar>
          <q-btn flat icon="menu" @click="drawerLeft = !drawerLeft" />

          <q-toolbar-title>
            <q-breadcrumbs active-color="white" style="font-size: 16px">
              <q-breadcrumbs-el label="Home" icon="home" to="/" />
              <q-breadcrumbs-el v-if="authStore.$state.isAuthenticated" label="Rest API Post List" icon="notes" to="/"  />
              <q-breadcrumbs-el v-if="authStore.$state.isAuthenticated" label="GraphQL Post List" icon="notes" to="/graphql/post-list"  />
              <q-breadcrumbs-el v-if="authStore.$state.isAuthenticated" label="RESTAPI Search" icon="search" to="/post-search" />
              <q-breadcrumbs-el v-if="authStore.$state.isAuthenticated" label="GraphQL Search" icon="search" to="/graphql-search" />
              <q-breadcrumbs-el label="About" icon="info" to="/about" />
              <q-breadcrumbs-el v-if="!authStore.$state.isAuthenticated" label="Login" icon="login" to="/login" />
              <q-breadcrumbs-el v-else label="Logout" icon="logout" @click="logout" to="/" />
            </q-breadcrumbs>
          </q-toolbar-title>

          <q-btn flat icon="menu" @click="drawerRight = !drawerRight" />
        </q-toolbar>
      </q-header>

      <q-drawer v-model="drawerLeft" :width="200" :breakpoint="700" side="left" bordered>
        <q-scroll-area class="fit">
          <q-list padding class="menu-list">
            <q-item exact clickable v-ripple to="/">
              <q-item-section avatar>
                <q-icon name="home" />
              </q-item-section>

              <q-item-section>
                Home
              </q-item-section>
            </q-item>

            <q-item exact clickable v-ripple to="/about">
              <q-item-section avatar>
                <q-icon name="info" />
              </q-item-section>

              <q-item-section :class="$q.dark.isActive ? 'text-white' : 'text-dark'">
                About
              </q-item-section>
            </q-item>
          </q-list>
        </q-scroll-area>
      </q-drawer>

      <q-drawer v-if="authStore.$state.isAuthenticated" v-model="drawerRight" :width="250" :breakpoint="700" side="right" bordered>
        <!-- drawer content -->
        <q-scroll-area style="height: calc(100% - 150px); margin-top: 150px; border-right: 1px solid #ddd">
          <q-list padding>
            <q-item clickable v-ripple>
              <q-item-section avatar>
                <q-icon name="inbox" />
              </q-item-section>

              <q-item-section>
                <router-link :class="$q.dark.isActive ? 'text-white' : 'text-dark'" :to="{ name: 'add-post' }">
                  Add Post
                </router-link>
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple>
              <q-item-section avatar>
                <q-icon name="send" />
              </q-item-section>

              <q-item-section>
                <router-link :class="$q.dark.isActive ? 'text-white' : 'text-dark'" :to="{ name: 'add-tag' }">
                  RestAPI Add Tag
                </router-link>
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple>
              <q-item-section avatar>
                <q-icon name="inbox" />
              </q-item-section>

              <q-item-section>
                <router-link :class="$q.dark.isActive ? 'text-white' : 'text-dark'" :to="{ name: 'graphql-add-post' }">
                  GraphQL Add Post
                </router-link>
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple>
              <q-item-section avatar>
                <q-icon name="send" />
              </q-item-section>

              <q-item-section>
                <router-link :class="$q.dark.isActive ? 'text-white' : 'text-dark'" :to="{ name: 'graphql-post-list' }">
                  GraphQL Post List
                </router-link>
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple>
              <q-item-section avatar>
                <q-icon name="send" />
              </q-item-section>

              <q-item-section>
                <router-link :class="$q.dark.isActive ? 'text-white' : 'text-dark'" :to="{ name: 'graphql-add-tag' }">
                  GraphQL Add Tag
                </router-link>
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple>
              <q-item-section avatar>
                <q-icon name="send" />
              </q-item-section>

              <q-item-section>
                <router-link :class="$q.dark.isActive ? 'text-white' : 'text-dark'" :to="{ name: 'user-favorite-post-list' }">
                  RESTAPI User Favorite Post List
                </router-link>
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple>
              <q-item-section avatar>
                <q-icon name="send" />
              </q-item-section>

              <q-item-section>
                <router-link :class="$q.dark.isActive ? 'text-white' : 'text-dark'" :to="{ name: 'graphql-user-favorite-post-list' }">
                  GraphQL User Favorite Post List
                </router-link>
              </q-item-section>
            </q-item>

            

            <q-item clickable v-ripple>
              <q-item-section avatar>
                <q-icon name="search" />
              </q-item-section>

              <q-item-section>
                <router-link :class="$q.dark.isActive ? 'text-white' : 'text-dark'" :to="{ name: 'post-search' }">
                  REST API Search
                </router-link>
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple>
              <q-item-section avatar>
                <q-icon name="search" />
              </q-item-section>

              <q-item-section>
                <router-link :class="$q.dark.isActive ? 'text-white' : 'text-dark'" :to="{ name: 'graphql-search' }">
                  GraphQL Search
                </router-link>
              </q-item-section>
            </q-item>
            
            <q-item clickable v-ripple @click="toggleDarkMode">
              <q-item-section avatar>
                <q-icon name="dark_mode" />
              </q-item-section>

              <q-item-section>
                Toggle Dark Mode
              </q-item-section>
            </q-item>

            <q-item clickable v-ripple @click="logout">
              <q-item-section avatar>
                <q-icon name="logout" />
              </q-item-section>

              <q-item-section clickable>
                Logout
              </q-item-section>
            </q-item>
          </q-list>
        </q-scroll-area>

        <q-img class="absolute-top" src="https://cdn.quasar.dev/img/material.png" style="height: 150px">
          <div class="absolute-bottom bg-transparent">
            <q-avatar size="56px" class="q-mb-sm">
              <img src="https://cdn.quasar.dev/img/boy-avatar.png">
            </q-avatar>
            <div class="text-weight-bold">Razvan Stoenescu</div>
            <div>@rstoenescu</div>
          </div>
        </q-img>
      </q-drawer>

      <q-drawer v-if="!authStore.$state.isAuthenticated" v-model="drawerRight" :width="250" :breakpoint="700" side="right" bordered>
        <!-- drawer content -->
        <q-scroll-area style="height: calc(100% - 150px); border-right: 1px solid #ddd">
          <q-list padding>
            <q-item clickable v-ripple to="/login">
              <q-item-section avatar>
                <q-icon name="login" />
              </q-item-section>

              <q-item-section>
                Login
              </q-item-section>
            </q-item>
          </q-list>
        </q-scroll-area>
      </q-drawer>

      <q-page-container>
        <router-view />
      </q-page-container>

      <q-footer reveal elevated class="bg-grey-8 text-white">
        <q-toolbar>
          <q-toolbar-title>
            <div>Footer</div>
          </q-toolbar-title>
        </q-toolbar>
      </q-footer>

    </q-layout>
  </div>
</template>

<script>
import { ref } from 'vue'
import { Dark, Notify } from 'quasar'
import { OnClickOutside } from '@vueuse/components'

import { useAuthStore } from './stores/authStore';

export default {
  setup() {
    const authStore = useAuthStore();

    return {
      authStore,
      drawerLeft: ref(false),
      drawerRight: ref(false),
      toggleDarkMode() {
        Dark.toggle()
      },

    }
  },
  methods: {
    async logout() {
      try {
        await this.authStore.logout()
        this.$router.push('/login')
        Notify.create({
          message: 'Logged out Successfully',
          type: "positive",
          actions: [
            { icon: 'close', color: 'white', round: true, }
          ]
        })
      } catch (error) {
        Notify.create({
          message: error.message,
          type: "negative",
          actions: [
            { icon: 'close', color: 'white', round: true, }
          ]
        })
      }
    }
  }
}
</script>

<style lang="sass" scoped>
.menu-list .q-item
  border-radius: 0 32px 32px 0
</style>