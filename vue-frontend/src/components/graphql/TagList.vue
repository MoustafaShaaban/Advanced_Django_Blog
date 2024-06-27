<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useQueryClient, useQuery, useMutation } from '@tanstack/vue-query';
import { Notify, Cookies } from 'quasar';
import { useRouter } from 'vue-router';


const queryClient = useQueryClient();
const router = useRouter();
const name = ref('');
const tagCard = ref(false);

async function getTags() {
    const response = await axios({
        url: import.meta.env.VITE_GraphQL_URL,
        method: 'post',
        withCredentials: true,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        data: {
            query: `
                query getAllTags {
                    allTags {
                        id
                        name
                        slug
                    }
                }
            `
        }
    });

    return response.data;
};

const { data: tagsData, error, isPending, isLoading, isError } = useQuery({
    queryKey: ['graphqlTagsList'],
    queryFn: getTags
})

async function addTag() {
    const response = await axios({
        url: import.meta.env.VITE_GraphQL_URL,
        method: 'post',
        withCredentials: true,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        data: {
            query: `
                mutation createTag($name: String!) {
                    createTag(input: {name: $name}) {
                        errors {
                            messages
                            field
                        }
                        tag {
                            id
                            name
                        }
                    }
                }
                `,
                variables: {
                    name: name.value
                }
        }
    });
    
    return response.data;
};

const { mutate } = useMutation({
    mutationFn: addTag,
    onSuccess: async () => {
        queryClient.invalidateQueries("graphqlTagsList")
        await router.push('/graphql/tags')
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

function handleSubmit() {
    mutate({
        name: name.value
    })
    tagCard.value = false;
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
        <!-- We can assume by this point that `isSuccess === true` -->
        <span v-else-if="tagsData.length == 0">No posts found</span>
        <div v-else class="q-mt-lg">
            <div class="q-pa-md" style="max-width: 350px">
                <q-list bordered separator>
                    <q-item clickable v-ripple>
                        <q-item-section>Avilable Tag Names</q-item-section>
                    </q-item>
                    <q-item v-for="tag in tagsData.data.allTags" clickable v-ripple>
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
                    <q-form @submit.prevent="handleSubmit" @reset="onReset">
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