import { createRouter, createWebHistory, useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/authStore'
import HomeView from '../views/HomeView.vue'
import LoginPageVue from '@/components/auth/LoginPage.vue'

import AddBlogPost from '@/components/posts/CreateBlogPost.vue'
import EditBlogPost from '@/components/posts/EditPost.vue'

import GraphQLPostList  from "../components/graphql/PostList.vue"
import GraphQLEditPost from "../components/graphql/EditPost.vue"
import GraphQLAddPost from "../components/graphql/AddPost.vue"
import GraphQLAddTag from "../components/graphql/AddTag.vue";
import AddTagVue from '@/components/posts/AddTag.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Home and Rest API Routes
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        requireAuth: false
      }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPageVue,
      meta: {
        requireAuth: false
      }
    },
    {
      path: '/add-post',
      name: 'add-post',
      component: AddBlogPost,
      meta: {
        requireAuth: true
      }
    },
    {
      path: '/edit-post/:slug',
      name: 'edit-post',
      component: EditBlogPost,
      meta: {
        requireAuth: true
      }
    },
    {
      path: '/add-tag',
      name: 'add-tag',
      component: AddTagVue,
      meta: {
        requireAuth: true
      }
    },
    // GraphQL Routes
    {
      path: '/graphql/post-list',
      name: 'graphql-post-list',
      component: GraphQLPostList,
      meta: {
        requireAuth: true
      }
    },
    {
      path: '/graphql-add-post',
      name: 'graphql-add-post',
      component: GraphQLAddPost,
      meta: {
        requireAuth: true
      }
    },
    {
      path: '/graphql/post-edit/:slug',
      name: 'graphql-post-edit',
      component: GraphQLEditPost,
      meta: {
        requireAuth: true
      }
    },
    {
      path: '/graphql/add-tag',
      name: 'graphql-add-tag',
      component: GraphQLAddTag,
      meta: {
        requireAuth: true
      }
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('../views/NotFound.vue'),
      meta: {
        requireAuth: false
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  let authenticated = authStore.$state.isAuthenticated
  const router = useRouter()
  
  if (to.meta.requireAuth && !authenticated) {
    next({ name: 'login'})
  } else if (to.name == "login" && authenticated) {
    next({ name: 'home'})
  } else if (to.name == "register" && authenticated) {
    next({ name: 'home'})
  } else {
    next()
  }
})

export default router
