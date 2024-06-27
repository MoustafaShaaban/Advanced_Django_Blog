<script>
import { Notify } from "quasar";
import { createTagMutation } from "@/graphqlMutations";


export default {
    name: "GraphQLAddTag",
    data() {
        return {
            name: "",
        }
    },
    methods: {
        refreshPage() {
            window.location.reload();
        },
        addTag() {
            try {
                this.$apollo.mutate({
                    mutation: createTagMutation,
                    variables: {
                        "name": this.name,
                    }
                })
                this.$router.push({name: "graphql-tags"})
                Notify.create({
                    message: 'Tag Created Successfully',
                    type: 'positive',
                    actions: [
                        { label: 'Refresh', color: 'white', handler: () => { this.refreshPage() } },
                        { icon: 'close', color: 'white', round: true, },
                    ]
                })
            } catch (error) {
                Notify.create({
                    message: error.message,
                    type: 'negative',
                    actions: [
                        { icon: 'close', color: 'white', round: true, },
                    ]
                })
            }
        },
        onReset() {
            this.name = null
        }
    }
}

</script>

<template>
    <q-page class="flex flex-center">
        <q-card flat bordered class="my-card">
            <q-card-section>
                <div class="row items-center no-wrap">
                    <div class="col">
                        <div class="text-h6">Add Post</div>
                    </div>
                </div>
            </q-card-section>

            <q-card-section>
                <q-form @submit.prevent="addTag" @reset="onReset">
                    <q-input filled v-model.lazy.trim="name" label="Tag name" required lazy-rules
                        :rules="[val => val && val.length > 0 || 'Tag name is required']" />
                    <div class="q-pa-sm q-mt-md">
                        <q-btn label="Create Tag" type="submit" color="primary" />
                        <q-btn label="Reset" type="reset" class="bg-grey-8 text-white q-ml-sm" />
                    </div>
                </q-form>
            </q-card-section>
        </q-card>
    </q-page>
</template>
