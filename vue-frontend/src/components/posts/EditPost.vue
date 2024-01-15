<script>
import { Notify, Cookies } from 'quasar'
import { axiosAPI } from "../../api/axios"

export default {
  name: "EditPost",
  data() {
    return {
      post: {
        title: "",
        content: ""
      },
    }
  },
  async created() {
    await axiosAPI.get("/posts/" + this.$route.params.slug)
      .then(response => {
        this.post = response.data
      });
  },
  methods: {
    async updatePost(e) {
      try {
        await axiosAPI.put(`/posts/${this.post.slug}/`, this.post, {
          headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
          }
        })
          .then(response => {
            this.$router.push('/');
            Notify.create({
              message: 'Note Updated Successfully',
              type: "positive",
              actions: [
                { icon: 'close', color: 'white', round: true, }
              ]
            })
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

    },
    async navigateToNotes() {
      await router.push({ name: "notes" })
    }
  }
}
</script>


<template>
  <q-page class="flex flex-center">
    <q-card flat bordered class="my-card" :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-2'">
      <q-card-section>
        <div class="row items-center no-wrap">
          <div class="col">
            <div class="text-h6">Edit Post</div>
          </div>
        </div>
      </q-card-section>

      <q-card-section>
        <q-form @submit.prevent="updatePost" @reset="onReset">
          <q-input filled v-model="post.title" label="Post Title" required lazy-rules
            :rules="[val => val && val.length > 0 || 'Post Title is required']" />

          <q-input filled v-model="post.content" type="text" required label="Post Content" lazy-rules
            :rules="[val => val && val.length > 0 || 'Post Content is required']" />
          <q-separator />
          <div class="q-pa-sm q-mt-md">
            <q-btn label="Edit" type="submit" color="primary" />
            <q-btn label="Reset" type="reset" class="bg-grey-8 text-white q-ml-sm" />
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<style lang="sass" scoped>
.my-card
  width: 100%
  width: 500px
</style>