<script setup>
import { ref, onMounted } from 'vue';
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router';
import { useMutation, useQueryClient, useQuery } from '@tanstack/vue-query'
import { createTag, getAllTags } from '../../api/axios';

const name = ref('')


const queryClient = useQueryClient();

const router = useRouter();
const $q = useQuasar();

onMounted(async () => {
    tags.value = await getAllTags();
});

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
    mutationFn: createTag,
    onSuccess: async () => {
        queryClient.invalidateQueries("tags")
        await router.push('/')
        $q.notify({
            message: 'Tag Added Successfully',
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
        name: name.value
    })
}

function onReset() {
    name.value = null
    content.value = null
}

</script>

<template>
    <q-page class="flex flex-center">
        <div v-if="isPending" class="alert alert-primary" role="alert">
            Adding tag...
        </div>
        <q-card flat bordered class="my-card" :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-2'">
            <q-card-section>
                <div class="row items-center no-wrap">
                    <div class="col">
                        <div class="text-h6">Add Tag</div>
                    </div>
                </div>
            </q-card-section>

            <q-card-section>
                <q-form @submit.prevent="handleSubmit" @reset="onReset">
                    <q-input filled v-model="name" label="Tag Name" required lazy-rules
                        :rules="[val => val && val.length > 0 || 'Tag Name is required']" />

                    <div class="q-pa-sm q-mt-md">
                        <q-btn label="Add Tag" type="submit" color="primary" />
                        <q-btn label="Reset" type="reset" class="bg-grey-8 text-white q-ml-sm" />
                    </div>
                </q-form>
            </q-card-section>
        </q-card>
    </q-page>
</template>