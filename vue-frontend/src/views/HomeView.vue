<script setup>
import { ref } from 'vue';
import { useQueryClient, useQuery, useMutation } from '@tanstack/vue-query';
import { Dialog, Notify, useQuasar, date, Cookies } from 'quasar';
import Multiselect from 'vue-multiselect'

import { getBlogPosts, deletePost, getAllTags, createPost, deleteComment, addPostToFavorites, likePost } from '@/api/axios';
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

const { data: tags } = useQuery({
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


const deletePostMutation = useMutation({
  mutationFn: deletePost,
  onSuccess: () => {
    queryClient.invalidateQueries({
      queryKey: ["allBlogPosts"]
    })
  }
})

const deleteCommentMutation = useMutation({
  mutationFn: deleteComment,
  onSuccess: () => {
    queryClient.invalidateQueries({
      queryKey: ["allBlogPosts"]
    })
  }
})

const addPostToFavoritesMutation = useMutation({
  mutationFn: addPostToFavorites,
  onSuccess: () => {
    queryClient.invalidateQueries({
      queryKey: ["allBlogPosts"]
    })
  }
});


const likePostMutation = useMutation({
  mutationFn: likePost,
  onSuccess: () => {
    queryClient.invalidateQueries({
      queryKey: ["allBlogPosts"]
    })
  }
});


const { mutate } = useMutation({
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

function confirmDeletePost(slug) {
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

const removePostFromFavorites = (id) => {
  addPostToFavoritesMutation.mutate(id)
}

const addPostToUserFavorites = (id) => {
  addPostToFavoritesMutation.mutate(id)
}

const HandleLikePost = (id) => {
  likePostMutation.mutate(id)
}

const unlikePost = (id) => {
  likePostMutation.mutate(id)
}

function confirmRemovePostFromFavorites(id) {
  Dialog.create({
    title: 'Confirm',
    message: 'Are you sure you want to remove this post from your favorites list?',
    cancel: true,
    persistent: true
  }).onOk(() => {
    removePostFromFavorites(id)
    router.push('/')
    Notify.create({
      message: 'Removed Post from Favorites Successfully',
      type: 'positive',
      actions: [
        { label: 'Dismiss', color: 'white' }
      ]
    })
  }).onCancel(() => {
    return
  }).onDismiss(() => {
    return
  })
}

const deleteCommentFunction = (id) => {
  deleteCommentMutation.mutate(id)
}

function confirmDeleteComment(id) {
  Dialog.create({
    title: 'Confirm',
    message: 'Are you sure you want to delete this comment?',
    cancel: true,
    persistent: true
  }).onOk(() => {
    deleteCommentFunction(id)
    Notify.create({
      message: 'Comment Deleted Successfully',
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

function addPost() {
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
          <q-item-section avatar>
            <q-avatar>
              <img :src="post.author.avatar">
            </q-avatar>
          </q-item-section>

          <q-item-section>
            <div class="text-h5">{{ post.title }}</div>
            <q-item-label caption>
              by: {{ post.author.username }}
            </q-item-label>
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

        <q-card-actions v-if="authStore.$state.isAuthenticated && authStore.$state.username === post.author.username">
          <router-link :to="{ name: 'edit-post', params: { slug: post.slug } }">
            <q-btn flat color="primary">
              Detail
            </q-btn>
          </router-link>
          <q-btn color="info" flat
            @click="confirmDeletePost(post.slug)">Delete</q-btn>
          <q-btn v-if="post.favorites.length > 0" color="info" flat
            @click="confirmRemovePostFromFavorites(post.id)">Remove from favorites</q-btn>
          <q-btn v-else color="info" flat @click="addPostToUserFavorites(post.id)">Add to favorites</q-btn>
          <q-btn v-if="post.likes.length > 0" color="info" flat
            @click="unlikePost(post.id)">Unlike</q-btn>
          <q-btn v-else color="info" flat @click="HandleLikePost(post.id)">Like</q-btn>
          <q-separator />
        </q-card-actions>
          <q-card class="my-card">
            <q-toolbar>
              <q-toolbar-title><span class="text-weight-bold">Comments</span></q-toolbar-title>
            </q-toolbar>

            <q-card-section v-if="post.comments.length > 0">
              <q-card-section v-for="comment in post.comments" key="comment.id">
                <div class="text-h5">{{ comment.comment }}</div>
                <q-item-label caption>
                  by: {{ comment.user }}
                </q-item-label>
                <q-card-actions
                  v-if="authStore.$state.isAuthenticated && authStore.$state.username === comment.user">
                  <router-link :to="{ name: 'edit-comment', params: { id: comment.id } }">
                    <q-btn flat color="primary">
                      Edit
                    </q-btn>
                  </router-link>
                  <q-btn color="info" flat @click="confirmDeleteComment(comment.id)">Delete</q-btn>
                </q-card-actions>
              </q-card-section>
            </q-card-section>
            <q-card-section horizontal v-else>
              <p>This post has no comments</p>
            </q-card-section>
          </q-card>
      </q-card>

      <q-dialog v-model="card">
        <q-card flat bordered class="my-card">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">Add Post</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>


          <q-card-section>
            <q-form @submit.prevent="addPost" @reset="onReset">
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
              <multiselect v-model="tag" :multiple="true" :custom-label="opt => tags.find(e => e.id === opt).name"
                deselect-label="You must select at least one tag" :options="tags.map(tag => tag.id)" :searchable="true"
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
