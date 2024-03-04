import axios from "axios";
import { Cookies } from "quasar";


export const axiosAPI = axios.create({
    baseURL: import.meta.env.VITE_REST_API_URL,
    withCredentials: true,
    timeout: 4000,
    headers: {
        'X-CSRFToken': Cookies.get('csrftoken')
    }
})

export const axiosGraphQL = axios.create({
    baseURL: import.meta.env.VITE_BASE_URL,
    withCredentials: true,
    timeout: 4000,
    headers: {
        'X-CSRFToken': Cookies.get('csrftoken')
    }
})


export const getBlogPosts = async () => {
    const response = await axiosAPI.get("posts/", {
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    })
    return response.data
}

export const getUserFavoritePosts = async () => {
    const response = await axiosAPI.get("favorite-posts/", {
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    })
    return response.data
}

export const getUserPosts = async () => {
    const response = await axiosAPI.get("user-posts/", {
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    })
    return response.data
}

export const getPostById = async (slug) => {
    const response = await axiosAPI.get("posts/" + slug)
    return response.data
}

export const getAllTags = async () => {
    const response = await axiosAPI.get("tags/")
    return response.data
}

export const getTagById = async (id) => {
    const response = await axiosAPI.get("tags/" + id)
    return response.data
}

export const getAllComments = async () => {
    const response = await axiosAPI.get("comments/")
    return response.data
}

export const getCommentById = async (id) => {
    const response = await axiosAPI.get("comments/" + id)
    return response.data
}

export const createPost = async (post) => {
    const response = await axiosAPI.post("posts/", post, {
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    })
    return response.data
}

export const deletePost = async (slug) => {
    await axiosAPI.delete("/posts/" + slug, {
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    })
}

export const deleteComment = async (id) => {
    await axiosAPI.delete("/comments/" + id, {
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
        }
    })
}


export const createTag = async (tag) => {
    const response = await axiosAPI.post("tags/", tag, {
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    })
    return response.data
}

export const searchPost = async (title) => {
    const response = await axiosAPI.get("/posts/?title=" + title)
    return response.data
}

export const addPostToFavorites = async (id) => {
    const response = await axiosAPI.post("/favorite-post/", {id}, {
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    })
    return response.data
};

export const likePost = async (id) => {
    const response = await axiosAPI.post("/like-post/", {id}, {
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    })
    return response.data
}

export const getUserFavoritePostList = async () => {
    const response = await axiosGraphQL("/graphql/",{}, {
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        data: {
            query: `
                query {
                    userFavoritePosts {
                    title
                    slug
                    author {
                        username
                    }
                    content
                    tag {
                        id
                        name
                    }
                    publishedAt
                    updatedAt
                    slug
                    favorites {
                        username
                    }
                    comments {
                        user {
                        username
                        }
                        comment
                    }
                    }
                }
            `
        }
    })
    return response.data
}