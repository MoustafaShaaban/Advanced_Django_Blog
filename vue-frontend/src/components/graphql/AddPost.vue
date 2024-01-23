<script>
import { Notify } from "quasar";
import { createPostMutation } from "@/graphqlMutations";
import { getAllTags } from "@/graphqlQueries";


export default {
    name: "GraphQLAddPost",
    mounted() {
        this.getTags()
    },
    data() {
        return {
            allTags: [],
            title: "",
            content: "",
            tags: {}
        }
    },
    methods: {
        refreshPage() {
            window.location.reload();
        },

        async getTags() {
            let data = await this.$apollo.query({
                query: getAllTags,
            })

            this.allTags = data.data.allTags
        },

        addPost() {
            this.$apollo.mutate({
                mutation: createPostMutation,
                variables: {
                    "title": this.title,
                    "content": this.content,
                    "tags": { "slug": this.tags }
                }
            })
            this.$router.push("/graphql/post-list")
            Notify.create({
                message: 'Post Added Successfully',
                type: 'positive',
                actions: [
                    { label: 'Refresh', color: 'white', handler: () => { this.refreshPage() } },
                    { icon: 'close', color: 'white', round: true, },
                ]
            })
        },
        onReset() {
            this.title = null
            this.content = null
            this.tags = null
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
                        <div class="text-h6">Add Post</div>
                    </div>
                </div>
            </q-card-section>

            <q-card-section>
                <q-form @submit.prevent="addPost" @reset="onReset">
                    <q-input filled v-model.lazy.trim="title" label="Post Title" required lazy-rules
                        :rules="[val => val && val.length > 0 || 'Post Title is required']" />

                    <q-input filled v-model.lazy.trim="content" type="textarea" required label="Post Content" lazy-rules
                        :rules="[val => val && val.length > 0 || 'Post Content is required']" />
                    <q-separator />
                    <select v-model="tags">
                        <option value="">Choose a tag</option>
                        <hr />
                        <optgroup>
                            <option v-for="tag in allTags" id="tag.slug" :value="tag.slug">{{ tag.name }}</option>
                        </optgroup>
                    </select>
                    <div class="q-pa-sm q-mt-md">
                        <q-btn label="Add Post" type="submit" color="primary" />
                        <q-btn label="Reset" type="reset" class="bg-grey-8 text-white q-ml-sm" />
                    </div>
                </q-form>
            </q-card-section>
        </q-card>
    </q-page>
</template>


<!-- <script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { Notify } from "quasar"
import { useQueryClient, useQuery } from '@tanstack/vue-query'
import { useMutation } from '@vue/apollo-composable'

import { createPostMutation } from '@/graphqlMutations';
import { getAllPosts } from '@/graphqlQueries';
import { getAllTags } from '@/api/axios';

const router = useRouter();

const title = ref('')
const content = ref('')
const tags = ref({})

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

const { mutate: addPost } = useMutation(createPostMutation, () => ({
    variables: {
        "title": title.value,
        "content": content.value,
        "tags": { "slug": tags.value }
    }
}))

const handleSubmit = () => {
    addPost()
    router.push("/");
    Notify.create({
        message: 'Post Added Successfully',
        type: 'positive',
        actions: [
            // { label: 'Refresh', color: 'white', handler: () => { this.refreshPage() } },
            { icon: 'close', color: 'white', round: true, },
        ]
    })
}

function onReset() {
    title.value = null
    content.value = null
}

</script> -->