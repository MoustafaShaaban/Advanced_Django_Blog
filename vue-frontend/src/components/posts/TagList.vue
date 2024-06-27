<script setup>
import { ref } from 'vue';
import { Notify } from 'quasar';
import { useRouter } from 'vue-router';
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';

import { getAllTags, createTag } from '@/api/axios';


const name = ref('');
const tagCard = ref(false);

const router = useRouter();
const queryClient = useQueryClient();

const { data: tagsData, error, isError, isPending } = useQuery({
    queryKey: ['allTagsQuery'],
    queryFn: getAllTags,
})

const { mutate } = useMutation({
    mutationFn: createTag,
    onSuccess: async () => {
        queryClient.invalidateQueries("allTagsQuery")
        await router.push('/tags')
        Notify.create({
            message: 'Tag Added Successfully',
            type: "positive",
            actions: [
                { icon: 'close', color: 'white', round: true, }
            ]
        })
    },
    onError: async (error) => {
        Notify.create({
            message: error.message,
            type: "negative",
            actions: [
                { icon: 'close', color: 'white', round: true, }
            ]
        })
    },
})

function addTag() {
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
    <q-page class="q-mt-sm flex flex-center">
        <span v-if="isPending">Loading...</span>
        <span v-else-if="isError">Error: {{ error.message }}</span>
        <span v-else-if="tagsData.length == 0">No posts found</span>
        <div v-else class="q-mt-lg">
            <div class="q-pa-md" style="max-width: 350px">
                <q-list bordered separator>
                    <q-item clickable v-ripple>
                        <q-item-section>Avilable Tag Names</q-item-section>
                    </q-item>
                    <q-item v-for="tag in tagsData" clickable v-ripple>
                        <q-item-section>{{ tag.name }}</q-item-section>
                    </q-item>
                </q-list>
            </div>
        </div>

        <q-dialog v-model="tagCard">
                <q-card flat bordered class="my-card">
                    <q-card-section class="row items-center q-pb-none">
                        <div class="text-h6">Add Tag</div>
                        <q-space />
                        <q-btn icon="close" flat round dense v-close-popup />
                    </q-card-section>


                    <q-card-section>
                        <q-form @submit.prevent="addTag" @reset="onReset">
                            <q-input filled v-model.lazy.trim="name" label="Tag Name" required lazy-rules
                                :rules="[val => val && val.length > 0 || 'Tag Name is required']" />
                            <div class="q-pa-sm q-mt-md">
                                <q-btn label="Add Tag" type="submit" color="primary" />
                                <q-btn label="Reset" type="reset" class="bg-grey-8 text-white q-ml-sm" />
                            </div>
                        </q-form>
                    </q-card-section>
                </q-card>
            </q-dialog>

        <q-page-sticky position="bottom-right" :offset="[18, 18]">
            <q-btn fab icon="add" color="primary" @click="tagCard = true">
            </q-btn>
        </q-page-sticky>
    </q-page>
</template>