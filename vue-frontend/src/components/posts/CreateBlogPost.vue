<template>
    <q-page class="flex flex-center">
        <div v-if="isPending" class="alert alert-primary" role="alert">
            Adding note...
        </div>
        <q-card flat bordered class="my-card" :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-2'">
            <q-card-section>
                <div class="row items-center no-wrap">
                    <div class="col">
                        <div class="text-h6">Add Note</div>
                    </div>
                </div>
            </q-card-section>

            <q-card-section>
                <q-form @submit.prevent="handleSubmit" @reset="onReset">
                    <q-input filled v-model="title" label="Post Title" required lazy-rules
                        :rules="[val => val && val.length > 0 || 'Post Title is required']" />

                    <q-input filled v-model="content" type="text" required label="Post Content" lazy-rules
                        :rules="[val => val && val.length > 0 || 'Post Content is required']" />
                    <q-separator />
                    <select v-model="tag" multiple>
                        <option v-for="tag in data" id="tag.id" :value="tag.id">{{ tag.name }}</option>
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
  
<script setup>
import { ref } from 'vue';
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router';
import { useMutation, useQueryClient, useQuery } from '@tanstack/vue-query'
import { createPost, getAllTags } from '../../api/axios';

const title = ref('')
const content = ref('')
const tag = ref([
  { id: ''},
])

const queryClient = useQueryClient();

const router = useRouter();
const $q = useQuasar();

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

const { isPending, isError, error, isSuccess, mutate, reset } = useMutation({
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

function handleSubmit() {
  mutate({
    title: title.value,
    content: content.value,
    tag: tag.value
    
  })
}

function onReset() {
    title.value = null
    content.value = null
}

</script>