<script setup>
import { ref } from 'vue';
import { useQueryClient, useQuery, useMutation } from '@tanstack/vue-query';
import { Dialog, Notify, useQuasar, date } from 'quasar';
import Multiselect from 'vue-multiselect'
import { getBlogPosts, deletePost, getAllTags, createPost, axiosAPI, getAllComments } from '@/api/axios';
import router from '@/router';
import { useAuthStore } from '@/stores/authStore';

// Access QueryClient instance
const queryClient = useQueryClient()

const authStore = useAuthStore();
const $q = useQuasar();

const card = ref(false);
const title = ref('')
const content = ref('')
const tag = ref([])

// Query
const { isPending, isError, data, error } = useQuery({
  queryKey: ['allBlogPosts'],
  queryFn: getBlogPosts,
  onError: async (error) => {
    $q.notify({
      message: error.message,
      color: "negative",
      actions: [
        { icon: 'close', color: 'white', round: true, }
      ]
    })
  }
})

const { isFetching, data: tags, tagsError } = useQuery({
  queryKey: ['tags'],
  queryFn: getAllTags,
  onError: async (error) => {
    $q.notify({
      message: error.message,
      color: "negative",
      actions: [
        { icon: 'close', color: 'white', round: true, }
      ]
    })
  }
})

const { isPending: commentsIsPending, isError: commentsIsError, data: comments, error: commentsError } = useQuery({
  queryKey: ['comments'],
  queryFn: getAllComments,
  onError: async (error) => {
    $q.notify({
      message: error.message,
      color: "negative",
      actions: [
        { icon: 'close', color: 'white', round: true, }
      ]
    })
  }
})

const deletePostMutation = useMutation({
  mutationFn: deletePost,
  onSuccess: () => {
    queryClient.invalidateQueries({
      queryKey: ["allBlogPosts"]
    })
  }
})

const { isPendingAddBlogPost, isErrorAddBlogPost, errorAddBlogPost, isSuccess, mutate, reset } = useMutation({
  mutationFn: createPost,
  onSuccess: async () => {
    queryClient.invalidateQueries("allBlogPosts")
    await router.push('/')
    $q.notify({
      message: 'Post Added Successfully',
      type: "positive",
      actions: [
        { icon: 'close', color: 'white', round: true, }
      ]
    })
  },
  onError: async (error) => {
    $q.notify({
      message: error.message,
      color: "negative",
      actions: [
        { icon: 'close', color: 'white', round: true, }
      ]
    })
  },
})

const deletePostFunction = (slug) => {
  deletePostMutation.mutate(slug)
}

function confirm(slug) {
  $q.dialog({
    title: 'Confirm',
    message: 'Are you sure you want to delete this post?',
    cancel: true,
    persistent: true
  }).onOk(() => {
    deletePostFunction(slug)
    router.push('/')
    $q.notify({
      message: 'Post Deleted Successfully',
      type: "positive",
      actions: [
        { icon: 'close', color: 'white', round: true, }
      ]
    })
  }).onCancel(() => {
    return
  }).onDismiss(() => {
    return
  })
}

function handleSubmit() {
  mutate({
    title: title.value,
    content: content.value,
    tag: tag.value
  })
  card.value = false;
  title.value = null
  content.value = null
  tag.value = null
}

function onReset() {
  title.value = null
  content.value = null
}
</script>

<template>
  <main class="q-mt-sm flex flex-center">
    <span v-if="isPending">Loading...</span>
    <span v-else-if="isError">Error: {{ error.message }}</span>
    <!-- We can assume by this point that `isSuccess === true` -->
    <span v-else-if="data.length == 0">No posts found</span>
    <div v-else class="q-mt-lg">
      <q-card v-for="post in data" :key="post.id" class="my-card q-mt-md" flat bordered>
        <q-item>
          <!-- <q-item-section avatar>
            <q-avatar>
              <img :src="post.author.avatar">
            </q-avatar>
          </q-item-section> -->

          <q-item-section>
            <div class="text-h5">{{ post.title }}</div>
            <!-- <div class="q-gutter-sm q-mt-xs">
              <q-badge v-for="tag in post.tag" :key="tag.id" caption outline color="primary" :label="tag.id" />
            </div> -->
          </q-item-section>
        </q-item>

        <q-separator />

        <q-card-section horizontal>
          <q-card-section>
            {{ post.content }}
          </q-card-section>
        </q-card-section>

        <q-separator />

        <q-card-actions vertical>
          <q-btn size="sm" flat icon="event">
            Published At: {{ date.formatDate(post.published_at, 'DD MMMM YYYY') }}
          </q-btn>
          <q-btn size="sm" flat icon="event">
            Last Updated: {{ date.formatDate(post.updated_at, 'DD MMMM YYYY') }}
          </q-btn>
        </q-card-actions>

        <q-separator />

        <q-card-actions v-if="authStore.$state.isAuthenticated">
          <router-link :to="{ name: 'edit-post', params: { slug: post.slug } }">
            <q-btn :class="$q.dark.isActive ? 'text-white' : 'text-dark'" flat color="primary">
              Detail
            </q-btn>
          </router-link>
          <q-btn :class="$q.dark.isActive ? 'text-white' : 'text-dark'" color="info" flat
            @click="confirm(post.slug)">Delete</q-btn>
        </q-card-actions>
      </q-card>

      <q-dialog v-model="card">
        <q-card flat bordered class="my-card" :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-2'">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">Add Post</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>


          <q-card-section>
            <q-form @submit.prevent="handleSubmit" @reset="onReset">
              <q-input filled v-model="title" label="Post Title" required lazy-rules
                :rules="[val => val && val.length > 0 || 'Post Title is required']" />

              <q-input filled v-model="content" type="textarea" required label="Post Content" lazy-rules
                :rules="[val => val && val.length > 0 || 'Post Content is required']" />
              <q-separator />
              <!-- <select v-model="tag" multiple>
                <option v-for="tag in tags" id="tag.id" :value="tag.id">{{ tag.name }}</option>
              </select> -->
              <label>Post Tags</label>
              <!-- https://github.com/shentao/vue-multiselect/issues/133#issuecomment-1652845391 -->
              <multiselect 
                v-model="tag" 
                :multiple="true" 
                :custom-label="opt => tags.find(e => e.id === opt).name" 
                deselect-label="You must select at least one tag" 
                :options="tags.map(tag => tag.id)" 
                :searchable="true" 
                :allow-empty="false">
                  <template slot="singleLabel" slot-scope="{ tag }"><strong>{{ tag.name }}</strong></template>
              </multiselect>
              <div class="q-pa-sm q-mt-md">
                <q-btn label="Add Post" type="submit" color="primary" />
                <q-btn label="Reset" type="reset" class="bg-grey-8 text-white q-ml-sm" />
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </q-dialog>
      <q-page-sticky v-if="authStore.$state.isAuthenticated" position="bottom-right" :offset="[18, 18]">
        <q-btn fab icon="add" color="primary" @click="card = true">
        </q-btn>
      </q-page-sticky>
    </div>
  </main>
</template>

<style lang="sass" scoped>
.my-card
  width: 100%
  width: 500px
</style>