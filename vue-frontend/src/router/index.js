import { createRouter, createWebHistory, useRouter } from 'vue-router';

import { useAuthStore } from '@/stores/authStore';
import HomeView from '../views/HomeView.vue';
import LoginPageVue from '@/components/auth/LoginPage.vue';

import AddBlogPost from '@/components/posts/CreateBlogPost.vue';
import EditBlogPost from '@/components/posts/EditPost.vue';
import SearchPosts from '@/components/posts/SearchPosts.vue';
import UserFavoritePostList from '@/components/posts/FavoritePostList.vue';
import UserPostList from '@/components/posts/UserPostList.vue';
import TagList from '@/components/posts/TagList.vue';

import GraphQLPostList  from "../components/graphql/PostList.vue";
import GraphQLAddPost from "../components/graphql/AddPost.vue";
import GraphQLEditPost from "../components/graphql/EditPost.vue";
import GraphQLUserFavoritePostList from '@/components/graphql/FavoritePostList.vue';
import GraphQLUserPostList from '@/components/graphql/UserPostList.vue';
import GraphQLAddTag from "../components/graphql/AddTag.vue";
import GraphQLEditComment from "../components/graphql/EditComment.vue";
import AddTagVue from '@/components/posts/AddTag.vue';
import EditComment from '@/components/posts/EditComment.vue';

import GraphQLSearchPosts from "@/components/graphql/SearchPosts.vue";
import RegisterPageVue from '@/components/auth/RegisterPage.vue';

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
      path: '/register',
      name: 'register',
      component: RegisterPageVue,
      meta: {
        requireAuth: false
      }
    },
    {
      path: '/post-search',
      name: 'post-search',
      component: SearchPosts,
      meta: {
        requireAuth: true
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
      path: '/user-favorite-post-list',
      name: 'user-favorite-post-list',
      component: UserFavoritePostList,
      meta: {
        requireAuth: true
      }
    },
    {
      path: '/user-post-list',
      name: 'user-post-list',
      component: UserPostList,
      meta: {
        requireAuth: true
      }
    },
    {
      path: '/edit-comment/:id',
      name: 'edit-comment',
      component: EditComment,
      meta: {
        requireAuth: true
      }
    },
    {
      path: '/tags',
      name: 'tags',
      component: TagList,
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
      path: '/graphql/edit-post/:slug',
      name: 'graphql-edit-post',
      component: GraphQLEditPost,
      meta: {
        requireAuth: true
      }
    },
    {
      path: '/graphql-user-favorite-post-list',
      name: 'graphql-user-favorite-post-list',
      component: GraphQLUserFavoritePostList,
      meta: {
        requireAuth: true
      }
    },
    {
      path: '/graphql-user-post-list',
      name: 'graphql-user-post-list',
      component: GraphQLUserPostList,
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
      path: '/graphql/edit-comment/:id',
      name: 'graphql-edit-comment',
      component: GraphQLEditComment,
      meta: {
        requireAuth: true
      }
    },
    {
      path: '/graphql-search',
      name: 'graphql-search',
      component: GraphQLSearchPosts,
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
