<script setup>
import { ref, onMounted } from 'vue';
import { useQuasar } from 'quasar'
import Multiselect from 'vue-multiselect'
import { useRouter } from 'vue-router';
import { useMutation, useQueryClient, useQuery } from '@tanstack/vue-query'
import { createPost, getAllTags } from '../../api/axios';

const title = ref('')
const content = ref('')
const tag = ref([])

const queryClient = useQueryClient();

const router = useRouter();
const $q = useQuasar();

const { isFetching, data: tags, tagsError } = useQuery({
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

                    <q-input filled v-model="content" type="textarea" required label="Post Content" lazy-rules
                        :rules="[val => val && val.length > 0 || 'Post Content is required']" />
                    <q-separator />
                    <label>Post Tags</label>
                    <!-- https://github.com/shentao/vue-multiselect/issues/133#issuecomment-1652845391 -->
                    <multiselect v-model="tag" :multiple="true" :custom-label="opt => tags.find(e => e.id === opt).name"
                        deselect-label="You must select at least one tag" :options="tags.map(i => i.id)" :searchable="true"
                        :allow-empty="false">
                        <template slot="singleLabel" slot-scope="{ tag }"><strong>{{ tag.name }}</strong></template>
                    </multiselect>
                    <!-- <select v-model="tag" multiple>
                        <option v-for="tag in data" id="tag.id" :value="tag.id">{{ tag.name }}</option>
                    </select> -->
                    <div class="q-pa-sm q-mt-md">
                        <q-btn label="Add Post" type="submit" color="primary" />
                        <q-btn label="Reset" type="reset" class="bg-grey-8 text-white q-ml-sm" />
                    </div>
                </q-form>
            </q-card-section>
        </q-card>
    </q-page>
</template>