<script setup>
import { useQueryClient, useQuery, useMutation } from '@tanstack/vue-query';
import { Dialog, Notify, useQuasar } from 'quasar';
import { getBlogPosts, deletePost } from '@/api/axios';
import router from '@/router';
import { useAuthStore } from '@/stores/authStore';

// Access QueryClient instance
const queryClient = useQueryClient()

const authStore = useAuthStore();
const $q = useQuasar();

// Query
const { isPending, isError, data, error } = useQuery({
  queryKey: ['allBlogPosts'],
  queryFn: getBlogPosts,
})

const deletePostMutation = useMutation({
  mutationFn: deletePost,
  onSuccess: () => {
    queryClient.invalidateQueries({
      queryKey: ["allBlogPosts"]
    })
  }
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

        <q-card-actions v-if="authStore.$state.isAuthenticated">
          <q-btn flat round icon="event" />
          <q-btn flat>
            {{ post.published_at }}
          </q-btn>
          <router-link :to="{ name: 'edit-post', params: { slug: post.slug } }">
            <q-btn flat color="primary">
              Detail
            </q-btn>
          </router-link>
          <q-btn color="info" flat @click="confirm(post.slug)">Delete</q-btn>
        </q-card-actions>
      </q-card>
    </div>
  </main>
</template>

<style lang="sass" scoped>
.my-card
  width: 100%
  width: 500px
</style>