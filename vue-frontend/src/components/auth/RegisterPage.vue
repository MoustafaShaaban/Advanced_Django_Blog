<template>
  <q-page class="flex flex-center">
    <q-card v-if="!authStore.isAuthenticated" flat bordered class="my-card">
      <q-card-section>
        <div class="row items-center no-wrap">
          <div class="col">
            <div class="text-h6">Register for a new account</div>
          </div>
        </div>
      </q-card-section>

      <q-card-section>
        <q-form @submit.prevent="register" @reset="onReset">
          <!-- <q-input filled v-model="user.name" label="Name" required lazy-rules
            :rules="[val => val && val.length > 0 || 'Name is required']" /> -->
          <q-input filled v-model="user.email" type="email" required label="Email" lazy-rules
            :rules="[val => val && val.length > 0 || 'Email is required']" />
          <q-input filled v-model="user.username" type="text" label="Username" required lazy-rules
            :rules="[val => val && val.length > 0 || 'Username is required']" />
          <q-input filled v-model="user.password" type="password" required label="Password" lazy-rules
            :rules="[val => val && val.length > 0 || 'Password is required']" />
          <q-input filled v-model="user.password2" type="password" required label="Confirm Password" lazy-rules
            :rules="[val => val && val.length > 0 || 'Password is required']" />
          <!-- <q-input filled v-model="user.birthday" type="date" required label="Date of Birth" lazy-rules
            :rules="[val => val && val.length > 0 || 'Date of Birth is required']" /> -->
          <q-separator />
          <div class="q-pa-sm q-mt-md">
            <q-btn label="Register" type="submit" color="primary" />
            <q-btn label="Reset" type="reset" class="bg-grey-8 text-white q-ml-sm" />
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { reactive, onMounted } from 'vue';
import { Notify, Cookies } from 'quasar'
import { useRouter } from 'vue-router';

import { useAuthStore } from '@/stores/authStore';
import { axiosAPI } from '@/api/axios';

const authStore = useAuthStore();
const router = useRouter();

onMounted(() => {
  if (!Cookies.get('csrftoken')) {
    try {
      authStore.getCSRFToken();
    } catch (error) {
      Notify.create({
        message: error.message,
        color: "negative",
        actions: [
          { icon: 'close', color: 'white', round: true, }
        ]
      })
    }
  }
});

// const user = reactive({
//   name: '',
//   email: '',
//   username: '',
//   password: '',
//   password_confirm: '',
//   birthday: '',
// })

const user = reactive({
  username: '',
  email: '',
  password: '',
  password2: '',
})


async function register() {
  const response = axiosAPI.post(
    "http://localhost:8000/_allauth/browser/v1/auth/signup",
    user
  );
  console.log(response)
  router.push("/verify-email")
}

function onReset() {
  user.value = null
}
</script>

<!-- <script>
import { Notify } from 'quasar'
import { useRouter } from 'vue-router';

import { useAuthStore } from '@/stores/authStore';

export default {
  name: "RegisterPage",
  setup() {
    const authStore = useAuthStore();
    const router = useRouter()
    return { authStore, router };
  },
  data() {
    return {
      name: '',
      email: '',
      username: '',
      password: '',
      password_confirm: '',
      birthday: '',
    }
  },
  methods: {
    async register() {
      try {
        await this.authStore.register(this.name, this.email, this.username, this.password, this.password_confirm, this.birthday)
        this.router.push('/login')
        Notify.create({
          message: 'Registered Successfully, You can now login',
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
      this.username = null
      this.password = null
      this.password_confirm = null
    }
  },

}
</script> -->