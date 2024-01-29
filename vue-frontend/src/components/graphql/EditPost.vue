<script>
import { Notify } from 'quasar'
import { useQuery } from '@tanstack/vue-query'

import { getAllTags } from '../../api/axios';
import { getPostBySlug } from '@/graphqlQueries';
import { updatePostMutation } from "@/graphqlMutations"

export default {
    name: "GraphQLPostEdit",
    setup() {
        const { isFetching, data, tagsError } = useQuery({
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

        return { isFetching, data, tagsError }
    },
    data() {
        return {
            post: {
                id: "",
                title: "",
                content: "",
                tag: [
                  { id: '',},
                ]
            }
        }
    },
    async mounted() {
        await this.getPost();
    },
    methods: {
        refreshPage() {
            window.location.reload();
        },

        async getPost() {
            let data = await this.$apollo.query({
                query: getPostBySlug,
                variables: {
                    slug: this.$route.params.slug
                },
            })

            // Make a copy of the returned data because the data saved in the cache is read-only
            const postData = { ...data.data.postBySlug }
            this.post = postData
        },

        async updatePost() {
            this.$apollo.mutate({
                mutation: updatePostMutation,
                variables: {
                    "id": parseInt(this.post.id),
                    "title": this.post.title,
                    "content": this.post.content,
                    "tags": this.post.tag
                }
            })

            this.$router.push("/graphql/post-list")
            Notify.create({
                message: 'Post Updated Successfully',
                type: 'positive',
                actions: [
                    { label: 'Refresh', color: 'white', handler: () => { this.refreshPage() } },
                    { icon: 'close', color: 'white', round: true, },
                ]
            })
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
                <span v-if="$apollo.loading">Loading...</span>
                <span v-else-if="$apollo.error">Error: {{ error.message }}</span>
                <q-form v-else @submit.prevent="updatePost">
                    <q-input filled v-model="post.title" label="Post Title" required lazy-rules
                        :rules="[val => val && val.length > 0 || 'Post Title is required']" />

                    <q-input filled v-model="post.content" type="textarea" required label="Post Content" lazy-rules
                        :rules="[val => val && val.length > 0 || 'Post Content is required']" />
                    <q-separator />
                   <select v-model="post.tag" multiple>
                        <option v-for="tag in data" id="tag.id" :value="tag.id">{{ tag.name }}</option>
                    </select>
                    <div class="q-pa-sm q-mt-md">
                        <q-btn label="Edit" type="submit" color="primary" />
                        <q-btn label="Cancel" type="button" @click="() => { this.$router.push('/') }"
                            class="bg-grey-8 text-white q-ml-sm" />
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