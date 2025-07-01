export const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("@/layouts/MainLayout.vue"),
    children: [
      {
        path: "/",
        name: "home",
        component: () => import("@/views/HomeView.vue"),
        meta: {
          requireAuth: false,
        },
      },
      // Auth Routes
      {
        path: "/login",
        name: "login",
        component: () => import("@/components/auth/LoginPage.vue"),
        meta: {
          requireAuth: false,
        },
      },
      {
        path: "/register",
        name: "register",
        component: () => import("@/components/auth/RegisterPage.vue"),
        meta: {
          requireAuth: false,
        },
      },
      {
        path: "/verify-email",
        name: "verify-email",
        component: () => import("@/components/auth/VerfiyEmailPage.vue"),
        meta: {
          requireAuth: false,
        },
      },
      // Rest APIs Routes
      // Posts List and CRUD
      {
        path: "/search-posts",
        name: "search-posts",
        component: () => import("@/components/restapi/posts/SearchPosts.vue"),
        meta: {
          requireAuth: false,
        },
      },
      {
        path: "/posts-list",
        name: "posts-list",
        component: () => import("@/components/restapi/posts/PostsList.vue"),
        meta: {
          requireAuth: false,
        },
      },
      {
        path: "/create-post",
        name: "create-post",
        component: () => import("@/components/restapi/posts/CreatePost.vue"),
        meta: {
          requireAuth: true,
        },
      },
      {
        path: "/update-post/:slug",
        name: "update-post",
        component: () => import("@/components/restapi/posts/UpdatePost.vue"),
        meta: {
          requireAuth: true,
        },
      },
      {
        path: "/user-favorite-posts-list",
        name: "user-favorite-posts-list",
        component: () =>
          import("@/components/restapi/posts/UserFavoritePostsList.vue"),
        meta: {
          requireAuth: true,
        },
      },
      {
        path: "/user-posts-list",
        name: "user-posts-list",
        component: () => import("@/components/restapi/posts/UserPostsList.vue"),
        meta: {
          requireAuth: true,
        },
      },

      // Tags List and CRUD
      {
        path: "/tags",
        name: "tags",
        component: () => import("@/components/restapi/tags/TagsList.vue"),
        meta: {
          requireAuth: true,
        },
      },
      {
        path: "/create-tag",
        name: "create-tag",
        component: () => import("@/components/restapi/tags/CreateTag.vue"),
        meta: {
          requireAuth: true,
        },
      },

      // Comments List and CRUD
      {
        path: "/update-comment/:id",
        name: "update-comment",
        component: () =>
          import("@/components/restapi/comments/UpdateComment.vue"),
        meta: {
          requireAuth: true,
        },
      },

      // GraphQL Routes
      // Posts List and CRUD
      {
        path: "/graphql/posts-list/",
        name: "graphql-posts-list",
        component: () => import("@/components/graphql/posts/PostsList.vue"),
        meta: {
          requireAuth: true,
        },
      },
      {
        path: "/graphql/create-post/",
        name: "graphql-create-post",
        component: () => import("@/components/graphql/posts/CreatePost.vue"),
        meta: {
          requireAuth: true,
        },
      },
      {
        path: "/graphql/update-post/:slug/",
        name: "graphql-update-post",
        component: () => import("@/components/graphql/posts/UpdatePost.vue"),
        meta: {
          requireAuth: true,
        },
      },
      {
        path: "/graphql/search/",
        name: "graphql-search-posts",
        component: () => import("@/components/graphql/posts/SearchPosts.vue"),
        meta: {
          requireAuth: true,
        },
      },
      {
        path: "/graphql/user-posts-list/",
        name: "graphql-user-posts-list",
        component: () => import("@/components/graphql/posts/UserPostsList.vue"),
        meta: {
          requireAuth: true,
        },
      },
      {
        path: "/graphql/user-favorite-posts-list/",
        name: "graphql-user-favorite-posts-list",
        component: () =>
          import("@/components/graphql/posts/UserFavoritePostsList.vue"),
        meta: {
          requireAuth: true,
        },
      },
      // Tags List and CRUD
      {
        path: "/graphql/tags/",
        name: "graphql-tags",
        component: () => import("@/components/graphql/tags/TagsList.vue"),
        meta: {
          requireAuth: true,
        },
      },
      {
        path: "/graphql/create-tag/",
        name: "graphql-create-tag",
        component: () => import("@/components/graphql/tags/CreateTag.vue"),
        meta: {
          requireAuth: true,
        },
      },
      // Comments List and CRUD
      {
        path: "/graphql/update-comment/:id/",
        name: "graphql-update-comment",
        component: () =>
          import("@/components/graphql/comments/UpdateComment.vue"),
        meta: {
          requireAuth: true,
        },
      },

      {
        path: "/about",
        name: "about",
        // route level code-splitting
        // this generates a separate chunk (About.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import("@/views/AboutView.vue"),
      },
      {
        path: "/:pathMatch(.*)*",
        name: "NotFound",
        component: () => import("@/views/NotFound.vue"),
        meta: {
          requireAuth: false,
        },
      },
    ],
    meta: {
      requireAuth: false,
    },
  },
];
