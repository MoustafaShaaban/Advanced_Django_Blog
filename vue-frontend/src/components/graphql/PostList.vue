<script setup>
import { computed, watch } from 'vue';
import { Notify, Dialog, useQuasar } from 'quasar';
import { useQuery } from '@vue/apollo-composable';

import { useAuthStore } from '@/stores/authStore';
import { getAllPosts } from "../../graphqlQueries";

const authStore = useAuthStore();
const $q = useQuasar();

const { result, loading, error } = useQuery(getAllPosts)

const refreshPage = () => {
    window.location.reload()
}
</script>

<template>
    <main class="q-mt-sm flex flex-center">
        <span v-if="loading">Loading...</span>
        <span v-else-if="error">Error: {{ error.message }} Try <q-btn size="sm" color="primary" @click="refreshPage">
                Reloading</q-btn> the page</span>
        <!-- We can assume by this point that `isSuccess === true` -->
        <span v-else-if="result.length == 0">No Posts available Try <q-btn size="sm" color="primary" @click="refreshPage">
                Reloading</q-btn> the page
            or click on the plus sign to add a new note</span>
        <div v-else class="q-mt-lg">
            <q-card v-for="post in result.allPosts" :key="post.id" class="my-card q-mt-md" flat bordered>
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
                    <!-- <q-btn color="info" flat @click="confirm(post.slug)">Delete</q-btn> -->
                </q-card-actions>
            </q-card>
        </div>
    </main>
</template>

<style lang="sass" scoped>
.my-card
  width: 100%
  width: 500px
</style>