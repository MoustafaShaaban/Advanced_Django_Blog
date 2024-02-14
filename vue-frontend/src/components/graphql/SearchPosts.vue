<script>
import { ref } from 'vue'
import { Notify, Dialog, useQuasar, date } from 'quasar';
import { useQuery } from "@tanstack/vue-query"
import Multiselect from 'vue-multiselect'
import moment from 'moment';

import { useAuthStore } from '@/stores/authStore';
import { getAllPosts, filterPostsByTitle } from "../../graphqlQueries";


export default {
    name: "GraphQLPostSearch",
    components: {
        Multiselect
    },
    setup() {
        const authStore = useAuthStore();
        return { authStore }
    },
    data() {
        return {
            allPosts: [],
            postCard: false,
            commentsCard: false,
            title: "",
            limit: "",
            content: "",
            tag: [],
            tags: [],
            searchForm: false,
        }
    },
    methods: {
        refreshPage() {
            window.location.reload();
        },
        // https://stackoverflow.com/a/54662898
        format_date(value) {
            if (value) {
                return moment(String(value)).format('DD MMMM YYYY')
            }
        },
        async getPosts() {
            let data = await this.$apollo.query({
                query: filterPostsByTitle,
                variables: {
                    "title": this.title,
                    "limit": parseInt(this.limit)
                }

            })

            this.allPosts = data.data.allPostsWithFilters
            this.title = null
            this.limit = null
            this.searchForm = false
        },

        onReset() {
            this.title = null
            this.limit = null
        },
    }
}
</script>

<template>
    <q-page class="flex flex-center column">
        <q-btn v-if="!this.searchForm" @click="this.searchForm = true" class="q-mr-md q-mt-md">Open Search Form</q-btn>
        <q-card v-if="this.searchForm" flat bordered class="form-card"
            :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-2'">
            <q-card-section class="row items-center q-pb-none">
                <div class="text-h6">Search for post by title</div>
                <q-space />
                <q-btn icon="close" flat round dense @click="this.searchForm = false" />
            </q-card-section>

            <q-card-section>
                <q-form @submit.prevent="getPosts" @reset="onReset">
                    <q-input filled v-model="title" label="Search for Post by Title" required lazy-rules
                        :rules="[val => val && val.length > 0 || 'Post Title is required']" />
                    <q-input filled v-model="limit" type="number" label="Limit Results (if not provided default is 5)" />
                    <div class="q-pa-sm q-mt-md">
                        <q-btn label="Search" type="submit" color="primary" />
                        <q-btn label="Reset" type="reset" class="bg-grey-8 text-white q-ml-sm" />
                    </div>
                </q-form>
            </q-card-section>
        </q-card>

        <div v-else class="q-mt-lg">
            <q-btn v-if="this.allPosts.length > 0" @click="this.allPosts = []" class="q-my-md">Clear Search Result</q-btn>
            <q-card v-for="post in allPosts.edges" :key="post.id" class="my-card q-mt-md" flat bordered>
                <q-item>
                    <!-- <q-item-section avatar>
              <q-avatar>
                <img :src="post.author.avatar">
              </q-avatar>
            </q-item-section> -->

                    <q-item-section>
                        <div class="text-h5">{{ post.node.title }}</div>
                        <!-- <div class="q-gutter-sm q-mt-xs">
                <q-badge v-for="tag in post.tag" :key="tag.id" caption outline color="primary" :label="tag.id" />
              </div> -->
                    </q-item-section>
                </q-item>

                <q-separator />

                <q-card-section horizontal>
                    <q-card-section>
                        {{ post.node.content }}
                    </q-card-section>
                </q-card-section>

                <q-separator />

                <q-card-actions v-if="authStore.$state.isAuthenticated" vertical>
                    <q-btn size="sm" flat icon="event">
                        Published At: {{ format_date(post.node.publishedAt) }}
                    </q-btn>
                    <q-btn size="sm" flat icon="event">
                        Last Updated: {{ format_date(post.node.updatedAt) }}
                    </q-btn>
                </q-card-actions>

                <q-separator />

                <q-card-actions v-if="authStore.$state.isAuthenticated">
                    <router-link :to="{ name: 'edit-post', params: { slug: post.node.slug } }">
                        <q-btn :class="$q.dark.isActive ? 'text-white' : 'text-dark'" flat color="primary">
                            Detail
                        </q-btn>
                    </router-link>
                    <!-- <q-btn :class="$q.dark.isActive ? 'text-white' : 'text-dark'" color="info" flat
              @click="confirmDeletePost(post.slug)">Delete</q-btn>
            <q-btn v-if="post.favorites.length > 0" color="info" flat
              @click="confirmRemovePostFromFavorites(post.id)">Remove from favorites</q-btn>
            <q-btn v-else color="info" flat @click="addPostToUserFavorites(post.id)">Add to favorites</q-btn> -->
                    <q-separator />
                    <q-card class="my-card">
                        <q-toolbar>
                            <q-toolbar-title><span class="text-weight-bold">Comments</span></q-toolbar-title>
                        </q-toolbar>

                        <q-card-section v-if="post.node.comments.length > 0">
                            <q-card-section v-for="comment in post.node.comments" key="comment.id">
                                <div class="text-h5">{{ comment.comment }}</div>
                                <q-item-label caption :class="$q.dark.isActive ? 'text-white' : 'text-dark'">
                                    by: {{ comment.user.username }}
                                </q-item-label>
                                <q-card-actions v-if="authStore.$state.isAuthenticated">
                                    <router-link :to="{ name: 'edit-comment', params: { id: comment.id } }">
                                        <q-btn :class="$q.dark.isActive ? 'text-white' : 'text-dark'" flat color="primary">
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
    </q-page>
</template>



<style lang="sass" scoped>
.form-card
  width: 100%
  width: 450px

.my-card
  width: 100%
  width: 600px
</style>