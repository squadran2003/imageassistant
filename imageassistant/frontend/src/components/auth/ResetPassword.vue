<template>
  <div class="min-h-screen bg-gray-900 flex items-center justify-center py-3 px-4 sm:px-6 lg:px-3">
    <div class="max-w-md w-full bg-gray-800 rounded-lg shadow-xl p-8 border border-gray-700">
      <h2 class="text-2xl font-bold text-white mb-4">Reset Your Password</h2>
      <form @submit.prevent="resetPassword" class="space-y-4">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-300">Email</label>
          <input v-model="email" type="email" id="email" required
               class="mt-1 block w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
               placeholder="Enter your email">
        </div>
        <button type="submit"
                :disabled="isLoading"
                class="w-full py-2 px-4 bg-indigo-600 hover:bg-indigo-500 disabled:bg-indigo-800 disabled:cursor-not-allowed text-white font-semibold rounded-md transition-colors duration-200">
          {{ isLoading ? 'Sending Reset Link...' : 'Reset Password' }}
        </button>
        <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
        <p v-if="success" class="text-green-500 text-sm">{{ successMessage }}</p>
        <div class="mt-4">
          <RouterLink to="/users/login" class="text-sm text-indigo-400 hover:text-indigo-300 transition-colors duration-200">
            ← Back to Login
          </RouterLink>
        </div>
         <div v-if="!isLoading" class="mt-4">
            <RobotChecker :onVerified="isRobotVerified" />
            <p v-if="robotError" class="mt-1 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md p-2">{{ robotError }}</p>
          </div>
      </form>

    </div>
  </div>
</template>
<script>
import RobotChecker from '../RobotChecker.vue';
import { API_URL } from '../../config.js';

export default {
  name: 'ResetPassword',
   components: {
    RobotChecker
  },
  data() {
    return {
      email: '',
      isLoading: false,
      error: null,
      success: false,
      successMessage: 'Password reset link sent successfully.',
      apiUrl: API_URL,
      robotError: null,
      isRobot: true,
    };
  },
  methods: {
    async resetPassword() {
      this.isLoading = true;
      this.error = null;
      this.success = false;
      if(!this.email) {
        this.error = 'Email is required';
        this.isLoading = false;
        return;
      }
      if(this.isRobot) {
        this.robotError = 'Please verify you are not a robot.';
        this.isLoading = false;
        return;
      }

      try {
        // Simulate API call to reset password
        const response = await fetch(`${this.apiUrl}/api/v1/users/change/password/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: this.email,
          })
        });
        const data = await response.json();
        if (response.status === 200) {
          this.success = true;
          this.successMessage = data.detail || this.successMessage;
          this.email = ''; // Clear email field after success
        } else {
          this.error = data.detail || 'Failed to send reset link. Please try again.';
        }
      } catch (err) {
        this.error = 'Failed to send reset link. Please try again.';
      } finally {
        this.isLoading = false;
      }
    },
    isRobotVerified(isRobot) {
        this.isRobot = isRobot;
        this.robotError = null;
    }
  }
};
</script>