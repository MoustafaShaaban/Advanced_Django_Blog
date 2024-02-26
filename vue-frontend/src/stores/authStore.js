import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";
import { Cookies } from "quasar"

import { axiosAPI } from "../api/axios";

export const useAuthStore = defineStore('auth', {
    state: () => ({
        isAuthenticated: useLocalStorage('Authenticated', null),
        username: useLocalStorage("Username", null),
    }),
    actions: {
        async getCSRFToken() {
            const response = await axiosAPI.get("csrf/", {
                credentials: "include",
            });

            let token = response.headers.get("X-CSRFToken");
            return token
        },

        async getSession() {
            await axiosAPI.get('/session/')
        },

        async login(email, password) {
            await axiosAPI.post('/login/', {email, password}, {
                headers: {
                    'X-CSRFToken': Cookies.get("csrftoken")
                }
            })
            const response = await axiosAPI.get('username/',)
            this.username = response.data.username
            this.isAuthenticated = true;
        },

        async register(name, email, username, password, password_confirm, birthday) {
            await axiosAPI.post('accounts/register/', {name, email, username, password, password_confirm, birthday}, {
            })
        },

        async logout() {
            await axiosAPI.post('accounts/logout/', {}, {
                headers: {
                    'X-CSRFToken': Cookies.get('csrftoken')
                }
            })
            this.isAuthenticated = null;
            localStorage.removeItem('Authenticated')

            this.username = null;
            localStorage.removeItem('Username')
        },
    }
})