<script setup>
import axios from 'axios';
import { useQuery } from '@tanstack/vue-query';
import { useQuasar, date, Cookies } from 'quasar';

import { useAuthStore } from '@/stores/authStore';



const authStore = useAuthStore();
const $q = useQuasar();
// Source: https://stackoverflow.com/a/59778006
async function getData() {
    const response = await axios({
        url: import.meta.env.VITE_GraphQL_URL,
        method: 'post',
        withCredentials: true,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        data: {
            query: `
                query {
                    userFavoritePosts {
                    title
                    slug
                    author {
                        username
                    }
                    content
                    tag {
                        id
                        name
                    }
                    publishedAt
                    updatedAt
                    slug
                    favorites {
                        username
                    }
                    comments {
                        id
                        user {
                        username
                        }
                        comment
                    }
                    }
                }
            `
        }
    })

    return response.data
}

const { data, error, isPending, isLoading, isError } = useQuery({
    queryKey: ['userFavoritePostList'],
    queryFn: getData
})

</script>

<template>
    <main class="q-mt-sm flex flex-center">
        <span v-if="isPending">Loading...</span>
    <span v-else-if="isError">Error: {{ error.message }}</span>
    <!-- We can assume by this point that `isSuccess === true` -->
    <span v-else-if="data.data.userFavoritePosts.length == 0">You did not add any post to your favorites list</span>
    <div v-else class="q-mt-lg">
        <q-card v-for="post in data.data.userFavoritePosts" :key="post.id" class="my-card q-mt-md" flat bordered>
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
                    Published At: {{ date.formatDate(post.publishedAt, 'DD MMMM YYYY') }}
                </q-btn>
                <q-btn size="sm" flat icon="event">
                    Last Updated: {{ date.formatDate(post.updatedAt, 'DD MMMM YYYY') }}
                </q-btn>
            </q-card-actions>

            <q-separator />

            <q-card-actions v-if="authStore.$state.isAuthenticated">
                <router-link :to="{ name: 'edit-post', params: { slug: post.slug } }">
                    <q-btn  flat color="primary">
                        Detail
                    </q-btn>
                </router-link>
                <!-- <q-btn color="info" flat
                    @click="confirmDeletePost(post.slug)">Delete</q-btn>
                <q-btn v-if="post.favorites.length > 0" color="info" flat
                    @click="confirmRemovePostFromFavorites(post.id)">Remove from favorites</q-btn>
                <q-btn v-else color="info" flat @click="addPostToUserFavorites(post.id)">Add to favorites</q-btn> -->
                <q-separator />
                <q-card class="my-card">
                    <q-toolbar>
                        <q-toolbar-title><span class="text-weight-bold">Comments</span></q-toolbar-title>
                    </q-toolbar>

                    <q-card-section v-if="post.comments.length > 0">
                        <q-card-section v-for="comment in post.comments" key="comment.id">
                            <div class="text-h5">{{ comment.comment }}</div>
                            <q-item-label caption>
                                by: {{ comment.user.username }}
                            </q-item-label>
                            <q-card-actions v-if="authStore.$state.isAuthenticated">
                                <router-link :to="{ name: 'edit-comment', params: { id: comment.id } }">
                                    <q-btn>
                                        Edit
                                    </q-btn>
                                </router-link>
                                <!-- <q-btn color="info" flat @click="confirmDeleteComment(comment.id)">Delete</q-btn> -->
                            </q-card-actions>
                        </q-card-section>
                    </q-card-section>
                    <q-card-section horizontal v-else>
                        <p>This post has no comments</p>
                    </q-card-section>
                </q-card>
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