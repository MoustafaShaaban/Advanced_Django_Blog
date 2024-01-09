import axios from "axios";
import { Cookies } from "quasar";


export const axiosAPI = axios.create({
    baseURL: import.meta.env.VITE_REST_API_URL,
    withCredentials: true,
    timeout: 4000,
})


export const getBlogPosts = async () => {
    const response = await axiosAPI.get("posts/")
    return response.data
}

export const getUserBlogPosts = async () => {
    const response = await axiosAPI.get("user_posts/")
    return response.data
}

export const getPostById = async (id) => {
    const response = await axiosAPI.get("posts/" + id)
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