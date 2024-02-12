<script>
import { ref } from 'vue'
import { Notify, Dialog, useQuasar, date } from 'quasar';
import { useQuery } from "@tanstack/vue-query"
import Multiselect from 'vue-multiselect'

import { useAuthStore } from '@/stores/authStore';
import { getAllPosts } from "../../graphqlQueries";
import { getAllTags, axiosAPI } from '@/api/axios';
import { createPostMutation, deletePostMutation, deleteCommentMutation } from '@/graphqlMutations';

export default {
    name: "GraphQLPostList",
    components: {
        Multiselect
    },
    setup() {
        const authStore = useAuthStore();
        return { authStore }
    },
    async mounted() {
        await axiosAPI.get('/tags/').then(response => {
            this.tags = response.data
        })
        await this.getPosts();
    },
    data() {
        return {
            allPosts: [],
            postCard: false,
            commentsCard: false,
            title: "",
            content: "",
            tag: [],
            tags: [],
        }
    },
    methods: {
        refreshPage() {
            window.location.reload();
        },

        async getPosts() {
            let data = await this.$apollo.query({
                query: getAllPosts,
            })

            this.allPosts = data.data.allPosts
        },

        async addPost() {
            await this.$apollo.mutate({
                mutation: createPostMutation,
                variables: {
                    "title": this.title,
                    "content": this.content,
                    "tags": this.tag
                }
            })
            this.postCard = false,
                this.title = null
            this.content = null
            this.tags = null

            await this.$router.push("/graphql/post-list")

            Notify.create({
                message: 'Post Added Successfully',
                type: 'positive',
                actions: [
                    { label: 'Refresh', color: 'white', handler: () => { this.refreshPage() } },
                    { label: 'Dismiss', color: 'white' }
                ]
            })
        },

        onReset() {
            this.title = null
            this.content = null
            this.tags = null
        },

        confirmDeletePost(id) {
            Dialog.create({
                title: 'Confirm',
                message: 'Are you sure you want to delete this post?',
                cancel: true,
                persistent: true
            }).onOk(() => {
                this.deletePost(id)
                this.$router.push('/graphql/post-list')
                Notify.create({
                    message: 'Post Deleted Successfully',
                    type: 'positive',
                    actions: [
                        { label: 'Refresh', color: 'white', handler: () => { this.refreshPage() } },
                        { label: 'Dismiss', color: 'white' }
                    ]
                })
            }).onCancel(() => {
                return
            }).onDismiss(() => {
                return
            })
        },

        confirmDeleteComment(id) {
            Dialog.create({
                title: 'Confirm',
                message: 'Are you sure you want to delete this comment?',
                cancel: true,
                persistent: true
            }).onOk(() => {
                this.deleteComment(id)
                this.$router.push('/graphql/post-list')
                Notify.create({
                    message: 'Post Deleted Successfully',
                    type: 'positive',
                    actions: [
                        { label: 'Refresh', color: 'white', handler: () => { this.refreshPage() } },
                        { label: 'Dismiss', color: 'white' }
                    ]
                })
            }).onCancel(() => {
                return
            }).onDismiss(() => {
                return
            })
        },

        async deletePost(id) {
            await this.$apollo.mutate({
                mutation: deletePostMutation,
                variables: {
                    // https://stackoverflow.com/questions/73172384/variable-id-got-invalid-value-1-int-cannot-represent-non-integer-value-1
                    id: parseInt(id),
                }
            })
        },

        async deleteComment(id) {
            await this.$apollo.mutate({
                mutation: deleteCommentMutation,
                variables: {
                    // https://stackoverflow.com/questions/73172384/variable-id-got-invalid-value-1-int-cannot-represent-non-integer-value-1
                    id: parseInt(id),
                }
            })
        },
    }
}
</script>

<template>
    <main class="q-mt-sm flex flex-center">
        <span v-if="$apollo.loading">Loading...</span>
        <span v-else-if="$apollo.error">Error: {{ error.message }} Try <q-btn size="sm" color="primary"
                @click="refreshPage">
                Reloading</q-btn> the page</span>
        <!-- We can assume by this point that `isSuccess === true` -->
        <span v-else-if="allPosts.length == 0">No Posts available Try <q-btn size="sm" color="primary" @click="refreshPage">
                Reloading</q-btn> the page
            or click on the plus sign to add a new note</span>
        <div v-else class="q-mt-lg">
            <q-card v-for="post in allPosts" :key="post.id" class="my-card q-mt-md" flat bordered>
                <q-item>
                    <!-- <q-item-section avatar>
                        <q-avatar>
                            <img :src="post.author.avatar" />
                        </q-avatar>
                    </q-item-section> -->

                    <q-item-section>
                        <div class="text-h5">{{ post.title }}</div>
                        <q-item-label caption>
                            by: {{ post.author.username }}
                        </q-item-label>
                        <div class="q-gutter-sm q-mt-xs">
                            <q-badge v-for="tag in post.tag" :key="tag.id" caption outline color="primary"
                                :label="tag.name" />
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

                <q-card-actions v-if="authStore.$state.isAuthenticated">
                    <q-btn flat round icon="event" />
                    <q-btn flat>
                        {{ post.updatedAt }}
                    </q-btn>
                    <router-link :to="{ name: 'graphql-edit-post', params: { slug: post.slug } }">
                        <q-btn flat color="primary">
                            Detail
                        </q-btn>
                    </router-link>
                    <q-btn color="info" flat @click="confirmDeletePost(post.id)">Delete</q-btn>
                </q-card-actions>

                <q-separator />
                <q-card class="my-card">
                    <q-toolbar>
                        <q-toolbar-title><span class="text-weight-bold">Comments</span></q-toolbar-title>
                    </q-toolbar>

                    <q-card-section v-if="post.comments.length > 0">
                        <q-card-section v-for="comment in post.comments" key="comment.id">
                            <div class="text-h5">{{ comment.comment }}</div>
                            <q-item-label caption :class="$q.dark.isActive ? 'text-white' : 'text-dark'">
                                by: {{ comment.user.username }}
                            </q-item-label>
                            <q-card-actions v-if="authStore.$state.isAuthenticated">
                                <router-link :to="{ name: 'graphql-edit-comment', params: { id: comment.id } }">
                                    <q-btn :class="$q.dark.isActive ? 'text-white' : 'text-dark'" flat color="primary">
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

            <q-dialog v-model="postCard">
                <q-card flat bordered class="my-card" :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-2'">
                    <q-card-section class="row items-center q-pb-none">
                        <div class="text-h6">Add Post</div>
                        <q-space />
                        <q-btn icon="close" flat round dense v-close-popup />
                    </q-card-section>


                    <q-card-section>
                        <q-form @submit.prevent="addPost" @reset="onReset">
                            <q-input filled v-model.lazy.trim="title" label="Post Title" required lazy-rules
                                :rules="[val => val && val.length > 0 || 'Post Title is required']" />

                            <q-input filled v-model.lazy.trim="content" type="textarea" required label="Post Content"
                                lazy-rules :rules="[val => val && val.length > 0 || 'Post Content is required']" />
                            <q-separator />
                            <label>Post Tags</label>
                            <!-- https://github.com/shentao/vue-multiselect/issues/133#issuecomment-1652845391 -->
                            <multiselect v-model="tag" :multiple="true"
                                :custom-label="opt => tags.find(e => e.id === opt).name"
                                deselect-label="You must select at least one tag" :options="tags.map(i => i.id)"
                                :searchable="true" :allow-empty="false">
                                <template slot="singleLabel" slot-scope="{ tag }"><strong>{{ tag.name }}</strong></template>
                            </multiselect>
                            <!-- <select v-model="tags" multiple>
                                <option v-for="tag in data" id="tag.id" :value="tag.id">{{ tag.name }}</option>
                            </select> -->
                            <div class="q-pa-sm q-mt-md">
                                <q-btn label="Add Post" type="submit" color="primary" />
                                <q-btn label="Reset" type="reset" class="bg-grey-8 text-white q-ml-sm" />
                            </div>
                        </q-form>
                    </q-card-section>
                </q-card>
            </q-dialog>

            <q-page-sticky position="bottom-right" :offset="[18, 18]">
                <q-btn fab icon="add" color="primary" @click="postCard = true">
                </q-btn>
            </q-page-sticky>
        </div>
    </main>
</template>

<style lang="sass" scoped>
.my-card
  width: 100%
  width: 600px
</style>