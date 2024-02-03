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


export const getBlogPosts = async () => {
    const response = await axiosAPI.get("posts/", {
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    })
    return response.data
}

export const getUserBlogPosts = async () => {
    const response = await axiosAPI.get("user_posts/")
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


export const createTag = async (tag) => {
    const response = await axiosAPI.post("tags/", tag, {
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    })
    return response.data
}