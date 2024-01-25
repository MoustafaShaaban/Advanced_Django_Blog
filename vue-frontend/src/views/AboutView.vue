<template>
  <q-page class="flex flex-center">
    <q-card flat bordered class="my-card" :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-2'">
      <q-card-section>
        <div class="row items-center no-wrap">
          <div class="col">
            <div class="text-h5">Advanced Django Blog</div>
            <div class="text-subtitle2">by Moustafa Shaaban</div>
          </div>
        </div>
      </q-card-section>
      <q-separator />

      <q-card-section class="q-pt-none">
        A blog project built using
        <q-list bordered separator>
          <q-item clickable v-ripple>
            <a :class="$q.dark.isActive ? 'text-white' : 'text-dark'" href="https://www.djangoproject.com/" target="_blank">Django Web Framework</a>
          </q-item>
          <q-item clickable v-ripple>
            <a :class="$q.dark.isActive ? 'text-white' : 'text-dark'" href="https://www.django-rest-framework.org/" target="_blank">Django REST Framework</a>
          </q-item>
          <q-item clickable v-ripple>
            <a :class="$q.dark.isActive ? 'text-white' : 'text-dark'" href="https://docs.graphene-python.org/projects/django/en/latest/" target="_blank">Graphene Django</a>
          </q-item>
          <q-item clickable v-ripple>
            <a :class="$q.dark.isActive ? 'text-white' : 'text-dark'" href="https://github.com/cookiecutter/cookiecutter-django/" target="_blank">Cookiecutter Django</a>
          </q-item>
          <q-item clickable v-ripple>
            <a :class="$q.dark.isActive ? 'text-white' : 'text-dark'" href="https://vuejs.org/" target="_blank">Vue.js 3</a>
          </q-item>
          <q-item clickable v-ripple>
            <a :class="$q.dark.isActive ? 'text-white' : 'text-dark'" href="https://quasar.dev/" target="_blank">Quasar Framework</a>
          </q-item>
          <q-item clickable v-ripple>
            <a :class="$q.dark.isActive ? 'text-white' : 'text-dark'" href="https://tanstack.com/query/latest/docs/vue/overview/" target="_blank">Tanstack Vue Query</a>
          </q-item>
          <q-item clickable v-ripple>
            <a :class="$q.dark.isActive ? 'text-white' : 'text-dark'" href="https://apollo.vuejs.org/" target="_blank">Vue Apollo</a>
          </q-item>
        </q-list>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<style lang="sass" scoped>
.my-card
  width: 100%
  max-width: 400px
</style>
