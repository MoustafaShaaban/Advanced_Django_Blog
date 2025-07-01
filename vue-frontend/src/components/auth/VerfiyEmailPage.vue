<template>
  <div class="email-verification">
    <h2>Verify Your Email</h2>
    <p>A verification code has been sent to {{ email }}. Please check your inbox (and spam folder) and enter the code below to verify your email address.</p>
    
    <form @submit.prevent="verifyEmail">
      <div class="form-group">
        <label for="code">Verification Code</label>
        <input
          v-model="code"
          type="text"
          id="code"
          placeholder="Enter your code"
          required
          class="input-field"
        />
      </div>
      <button type="submit" class="submit-btn">Verify</button>
    </form>
    
    <p v-if="message" class="success">{{ message }}</p>
    <p v-if="error" class="error">{{ error }}</p>
    
    <div class="resend">
      <p>Didn't receive a code?</p>
      <button @click="resendCode" class="resend-btn">Resend Verification Code</button>
    </div>
  </div>
</template>

<script>
import { axiosAPI } from '@/api/axios';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  name: 'EmailVerification',
  setup() {
    const router = useRouter();
    return { router };
  },
  data() {
    return {
      email: '',
      code: '',
      message: null,
      error: null
    };
  },
  created() {
    // Retrieve email from route query params (passed from sign-up)
    this.email = this.$route.query.email || 'your email';
  },
  methods: {
    async verifyEmail() {
      try {
        //const csrfToken = await this.getCsrfToken();
        const response = await axiosAPI.post(
          'http://localhost:8000/_allauth/browser/v1/auth/email/verify',
          {
            key: this.code.trim()
          },
        );
        this.message = 'Email verified successfully! Redirecting to login...';
        this.error = null;
        // Redirect to login after a short delay
        setTimeout(() => {
          this.router.push('/login');
        }, 2000);
      } catch (error) {
        console.log('Error response:', error.response);
        this.error = error.response?.data?.detail || 
                     error.response?.data?.code?.[0] || 
                     'Failed to verify email. Please check the code and try again.';
        this.message = null;
      }
    },
    async resendCode() {
      try {
        const csrfToken = await this.getCsrfToken();
        const response = await axiosAPI.post(
          'http://localhost:8000/_allauth/browser/v1/auth/email/resend',
          {
            email: this.email
          },
        );
        this.message = 'Verification code resent successfully!';
        this.error = null;
      } catch (error) {
        console.log('Error response:', error.response);
        this.error = error.response?.data?.detail || 
                     'Failed to resend verification code. Please try again.';
        this.message = null;
      }
    }
  }
};
</script>

<style scoped>
.email-verification {
  max-width: 400px;
  margin: 2rem auto;
  padding: 1rem;
  text-align: center;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.input-field {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

.submit-btn, .resend-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.submit-btn {
  background-color: #4CAF50;
  color: white;
}

.submit-btn:hover {
  background-color: #45a049;
}

.resend-btn {
  background-color: #2196F3;
  color: white;
}

.resend-btn:hover {
  background-color: #1976D2;
}

.success {
  color: green;
  margin: 1rem 0;
}

.error {
  color: red;
  margin: 1rem 0;
}

.resend {
  margin-top: 1.5rem;
}
</style>