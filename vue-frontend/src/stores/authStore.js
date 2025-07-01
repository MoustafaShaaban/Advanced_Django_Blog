import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";

import { axiosAPI } from "../api/axios";
import { Notify } from "quasar";
import { useRouter } from "vue-router";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    isAuthenticated: useLocalStorage("Authenticated", null),
    username: useLocalStorage("Username", null),
  }),
  actions: {
    async getCSRFToken() {
      const response = await axiosAPI.get("csrf/");
      let token = response.headers.get("X-CSRFToken");
      return token;
    },

    async getSession() {
      await axiosAPI.get("/session/");
    },

    async login(user) {
      try {
        await axiosAPI.post(
          "http://localhost:8000/_allauth/browser/v1/auth/login",
          user
        );
        const response = await axiosAPI.get("username/");
        this.username = response.data.username;
        this.isAuthenticated = true;
      } catch (error) {
        Notify.create({
          message: error.message,
          type: "negative",
          actions: [{ icon: "close", color: "white", round: true }],
        });
      }
    },

    async logout() {
      await axiosAPI.post("/api-auth/logout/");
      this.isAuthenticated = null;
      localStorage.removeItem("Authenticated");
      this.username = null;
      localStorage.removeItem("Username");
      // await axiosAPI.delete("http://localhost:8000/_allauth/browser/v1/auth/session");
    },

    async register(user) {
      const response = axiosAPI.post(
        "http://localhost:8000/_allauth/browser/v1/auth/signup",
        user
      );
      const router = useRouter();
      router.push("/verify-email")
      //router.push({ name: "verify-email" });
      // if (response.status === 201) {
      //   router.push("/verify-email");
      //   return;
      // }
      console.log(response)
      if (response.status === 401 || response.data.flows) {
        const flows = response.data.flows;
        console.log(response.data);
        console.log(flows);
        router.push("/verify-email")
        if (
          flows.some((flow) => flow.id === "verify_email" && flow.is_pending)
        ) {
          router.push("/verify-email"); // Redirect to verification page
          return;
        }
      }
    },

    async verifyEmail(key) {
      await axiosAPI.post(
        "http://localhost:8000/_allauth/browser/v1/auth/email/verify",
        key
      );
    },
  },
});
