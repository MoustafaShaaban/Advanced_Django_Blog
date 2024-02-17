<template>
    <q-page class="flex flex-center">
      <q-card v-if="!this.authStore.isAuthenticated" flat bordered class="my-card"
        :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-2'">
        <q-card-section>
          <div class="row items-center no-wrap">
            <div class="col">
              <div class="text-h6">Sign to your account</div>
            </div>
          </div>
        </q-card-section>
  
        <q-card-section>
          <q-form @submit.prevent="login" @reset="onReset">
            <q-input filled type="email" v-model.lazy.trim="email" label="Email" required lazy-rules
              :rules="[val => val && val.length > 0 || 'Email is required']" />
  
            <q-input filled v-model.lazy.trim="password" type="password" required label="Password" lazy-rules
              :rules="[val => val && val.length > 0 || 'Password is required']" />
            <q-separator />
            <div class="q-pa-sm q-mt-md">
              <q-btn label="Login" type="submit" color="primary" />
              <q-btn label="Reset" type="reset" class="bg-grey-8 text-white q-ml-sm" />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-page>
  </template>
    
  <script>
  import { Notify } from 'quasar'
  import { useRouter } from 'vue-router';
  
  import { useAuthStore } from '../../stores/authStore';
  
  export default {
    name: "LoginPage",
    setup() {
      const authStore = useAuthStore();
      const router = useRouter()
      return { authStore, router };
    },
    data() {
      return {
        email: '',
        password: '',
      }
    },
    methods: {
      async login() {
        try {
          await this.authStore.login(this.email, this.password)
          this.router.push('/')
          Notify.create({
            message: 'Logged in Successfully',
            type: "positive",
            actions: [
              { icon: 'close', color: 'white', round: true, }
            ]
          })
        } catch (error) {
          Notify.create({
            message: error.message,
            color: "negative",
            actions: [
              { icon: 'close', color: 'white', round: true, }
            ]
          })
        }
      },
      onReset() {
        this.email = null
        this.password = null
      }
    },
  
  }
  </script>
    