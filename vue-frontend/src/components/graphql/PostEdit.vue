<script setup>
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useQuery } from '@vue/apollo-composable';

import { useAuthStore } from '@/stores/authStore';
import { getPostBySlug, getAllTags } from '@/graphqlQueries';

const route = useRoute()
const authStore = useAuthStore()

const post = ref({
    title: "",
    content: "",
    tag: [
        { id: '' },
    ]
})


const variables = ref({
    slug: route.params.slug
})

const { result: data, loading: tagsLoading, tagsErrorrror } = useQuery(getAllTags)

const { result, loading, error } = useQuery(getPostBySlug, variables)

const title = ref("")
const content = ref("")

title.value = result.value?.postBySlug.title
content.value = result.value?.postBySlug.content

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
                <span v-if="loading">Loading...</span>
                <span v-else-if="error">Error: {{ error.message }}</span>
                <q-form v-else-if="result" @submit.prevent="">
                    <q-input filled v-model="title" label="Post Title" required lazy-rules
                        :rules="[val => val && val.length > 0 || 'Post Title is required']" />

                    <q-input filled v-model="content" type="textarea" required label="Post Content" lazy-rules
                        :rules="[val => val && val.length > 0 || 'Post Content is required']" />
                    <q-separator />
                    <select v-model="post.tag">
                        <option v-for="tag in data?.allTags" id="tag.id" :value="tag.id">{{ tag.name }}</option>
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