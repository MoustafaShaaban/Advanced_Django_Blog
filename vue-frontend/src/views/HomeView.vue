<script setup>
import { useQueryClient, useQuery } from '@tanstack/vue-query';

import { getBlogPosts } from '@/api/axios';

// Access QueryClient instance
const queryClient = useQueryClient()

// Query
const { isPending, isError, data, error } = useQuery({
  queryKey: ['allBlogPosts'],
  queryFn: getBlogPosts,
})
</script>

<template>
  <main class="absolute-center q-mt-lg">
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
            <div class="q-gutter-sm q-mt-xs">
              <q-badge v-for="tag in post.tag" caption outline color="primary" :label="tag.name" />
            </div>
          </q-item-section>
        </q-item>

        <q-separator />

        <q-card-section horizontal>
          <q-card-section>
            {{ post.content }}
          </q-card-section>
        </q-card-section>

        <q-separator />

        <q-card-actions>
          <q-btn flat round icon="event" />
          <q-btn flat>
            {{ post.published_at }}
          </q-btn>
          <q-btn flat color="primary">
            Detail
          </q-btn>
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