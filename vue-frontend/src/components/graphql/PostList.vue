<script>
import { Notify, Dialog, useQuasar } from 'quasar';
import { useQuery } from '@vue/apollo-composable';

import { useAuthStore } from '@/stores/authStore';
import { getAllPosts } from "../../graphqlQueries";
import { createPostMutation, deletePostMutation } from '@/graphqlMutations';

export default {
    name: "GraphQLPostList",
    setup() {
        const authStore = useAuthStore();

        return { authStore }
    },
    mounted() {
        this.getPosts();
    },
    data() {
        return {
            allPosts: [],
            card: false,
            title: "",
            content: "",
            tags: [
                { id: '' }
            ]
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

        async handleSubmit() {
            await this.$apollo.mutate({
                mutation: createPostMutation,
                variables: {
                    "title": this.title,
                    "content": this.content,
                    "tag": this.tags,
                }
            })
            this.card = false,

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

        confirm(id) {
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

        async deletePost(id) {
            await this.$apollo.mutate({
                mutation: deletePostMutation,
                variables: {
                    // https://stackoverflow.com/questions/73172384/variable-id-got-invalid-value-1-int-cannot-represent-non-integer-value-1
                    id: parseInt(id),
                }
            })
        }
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
                    <router-link :to="{ name: 'graphql-post-edit', params: { slug: post.slug } }">
                        <q-btn flat color="primary">
                            Detail
                        </q-btn>
                    </router-link>
                    <q-btn color="info" flat @click="confirm(post.id)">Delete</q-btn>
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
                            <q-input filled v-model.lazy.trim="title" label="Post Title" required lazy-rules
                                :rules="[val => val && val.length > 0 || 'Post Title is required']" />

                            <q-input filled v-model.lazy.trim="content" type="text" required label="Post Content" lazy-rules
                                :rules="[val => val && val.length > 0 || 'Post Content is required']" />
                            <q-separator />
                            <select v-model="tags" multiple>
                                <option v-for="tag in tags" id="tag.id" :value="tag.id">{{ tag.name }}</option>
                            </select>
                            <div class="q-pa-sm q-mt-md">
                                <q-btn label="Add Post" type="submit" color="primary" />
                                <q-btn label="Reset" type="reset" class="bg-grey-8 text-white q-ml-sm" />
                            </div>
                        </q-form>
                    </q-card-section>
                </q-card>
            </q-dialog>
            <q-page-sticky position="bottom-right" :offset="[18, 18]">
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