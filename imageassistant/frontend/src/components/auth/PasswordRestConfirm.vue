<template>
<div class="min-h-screen bg-gray-900 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-md border border-gray-700">
      <div v-if="!tokenValidated">
        <div class="flex justify-center">
          <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
        <p class="text-gray-300 text-center mt-4">Validating your reset link...</p>
      </div>
      
      <div v-else-if="tokenValid">
        <h2 class="text-2xl font-bold mb-6 text-center text-white">Change Password</h2>
        <form @submit.prevent="resetPassword" class="space-y-6">
          <div class="mb-4 text-left">
            <label for="new_password1" class="block text-gray-300 mb-2">New password</label>
            <input 
              type="password" 
              id="new_password1" 
              v-model="newPassword1"
              class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              required
            />
            <p v-if="errors.newPassword1" class="text-sm text-red-500 mt-1">{{ errors.newPassword1 }}</p>
          </div>
          
          <div class="mb-4 text-left">
            <label for="new_password2" class="block text-gray-300 mb-2">Confirm password</label>
            <input 
              type="password" 
              id="new_password2" 
              v-model="newPassword2"
              class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              required
            />
            <p v-if="errors.newPassword2" class="text-sm text-red-500 mt-1">{{ errors.newPassword2 }}</p>
          </div>
          
          <p v-if="errors.non_field_errors" class="text-sm text-red-500 mt-1">{{ errors.non_field_errors }}</p>
          
          <button 
            type="submit" 
            :disabled="isLoading"
            class="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-800 disabled:cursor-not-allowed text-white font-medium py-3 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-800 transition-colors duration-200"
          >
            {{ isLoading ? 'Saving...' : 'Change Password' }}
          </button>
        </form>
      </div>
      
      <div v-else class="px-4 py-3 rounded relative" role="alert">
        <p class="mb-3 text-white"><strong class="font-bold">Link is invalid or has expired.</strong></p>
        <router-link 
          to="/users/login" 
          class="w-full bg-indigo-600 hover:bg-indigo-700 rounded-lg text-white py-2 px-4 inline-block text-center mt-2"
        >
          Back to Login
        </router-link>
        <hr class="my-3 border-gray-700">
        <router-link 
          to="/users/change/password" 
          class="text-indigo-400 hover:text-indigo-300 block mt-2 text-center"
        >
          Request a new password reset link
        </router-link>
      </div>
      <p v-if="success" class="text-green-500 text-center mt-4">{{ successMessage }}</p>
    </div>
  </div>


</template>
<script>
import { RouterLink } from 'vue-router';
import { API_URL } from '../../config.js';

export default {
    name: 'PasswordResetConfirm',
    components: {
        RouterLink
    },
    data() {
        return {
            newPassword1: '',
            newPassword2: '',
            errors: {},
            isLoading: false,
            tokenValidated: true,
            tokenValid: true,
            success: false,
            successMessage: '',
            token: this.$route.params.token,
            uidb64: this.$route.params.uidb64,
            apiUrl: API_URL,
        };
    },
    methods: {
        async resetPassword() {
            this.isLoading = true;
            this.errors = {};
            this.tokenValid = false;
            this.success = false;
            this.successMessage = '';
            if (this.newPassword1 !== this.newPassword2) {
                this.errors.non_field_errors = ['The two password fields didn\'t match.'];
                this.isLoading = false;
                return;
            }
            try {
                const response = await fetch(`${this.apiUrl}/api/v1/users/password/reset/confirm/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        new_password1: this.newPassword1,
                        new_password2: this.newPassword2,
                        new_password: this.newPassword1,
                        uidb64: this.uidb64,
                        token: this.token
                    })
                });
                if(response.status === 400) {
                    const data = await response.json();
                    this.errors = data;
                    return;
                }
                if (response.ok) {
                    this.tokenValid = true;
                    this.tokenValidated = true;
                    this.success = true;
                    this.successMessage = 'Your password has been successfully reset. Redirecting to login..';
                    setTimeout(() => {
                        this.$router.push('/users/login');
                    }, 2000);
                } else {
                    this.tokenValid = true;
                    this.errors.non_field_errors = ['An error occurred while resetting your password.'];
                }                
            } catch (error) {
              console.error('Error during password reset:', error);
                if (error.response && error.response.data) {
                    this.errors = error.response.data;
                } else {
                    this.errors.non_field_errors = ['An unexpected error occurred. Please try again.'];
                }
            } finally {
                this.isLoading = false;
            }
        }
    },
};
</script>