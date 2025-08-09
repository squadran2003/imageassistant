<template>
  <div class="min-h-screen bg-gray-900 flex items-center justify-center py-3 px-4 sm:px-6 lg:px-3">
    <div class="max-w-md w-full bg-gray-800 rounded-lg shadow-xl p-8 border border-gray-700 -mt-24">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-extrabold text-white">Sign in to your account</h2>
        <p class="mt-2 text-sm text-gray-400">
          Welcome back! Please enter your details.
        </p>
      </div>
      
      <form @submit.prevent="login" class="space-y-6">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-300 mb-2">
            Email
          </label>
          <input 
            type="email" 
            id="email"
            v-model="email" 
            required 
            class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-200"
            placeholder="Enter your email"
          />
        </div>
        
        <div>
          <label for="password" class="block text-sm font-medium text-gray-300 mb-2">
            Password
          </label>
          <input 
            type="password" 
            id="password"
            v-model="password" 
            required 
            class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-200"
            placeholder="Enter your password"
          />
          <p v-if="!isLoading && error" class="text-sm text-red-500 mt-2">
            {{ error }}
          </p>
        </div>
        <!-- honeypot field -->
        <input type="text" name="website" style="display:none" tabindex="-1" autocomplete="off">
        <button 
          type="submit" 
          :disabled="isLoading"
          class="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-800 disabled:cursor-not-allowed text-white font-medium py-3 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-800 transition-colors duration-200"
        >
          {{ isLoading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>
      <div v-if="!isLoading" class="mt-4">
        <RobotChecker :onVerified="isRobotVerified" />
        <p v-if="robotError" class="mt-1 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md p-2">{{ robotError }}</p>
      </div>
      <div class="mt-6 flex justify-between items-center">
        <RouterLink to="/" class="text-sm text-indigo-400 hover:text-indigo-300 transition-colors duration-200">
          ← Back to Home
        </RouterLink>
         <RouterLink to="/users/change/password" class="text-sm text-indigo-400 hover:text-indigo-300 transition-colors duration-200">
            Forgot your password?
        </RouterLink>
      </div>
      <hr class="my-6 border-gray-700" />
      <p class="text-sm text-gray-400 text-center">
        Dont have an account?
        <RouterLink to="/users/signup" class="text-sm text-indigo-400 hover:text-indigo-300 transition-colors duration-200">
          Register here
        </RouterLink>
      </p>
    </div>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router';
import { API_URL } from '../../config.js';

import RobotChecker from '../RobotChecker.vue';
export default {
    name: 'LoginForm',
    components: {
        RouterLink,
        RobotChecker
    },
    props: {
        setIsAuthenticated: {
        type: Function,
        required: true
        },
        initializeAuth: {
          type: Function,
          required: true
        }
    },
    data() {
        return {
        email: '',
        password: '',
        isLoading: false,
        error: null,
        apiUrl: API_URL,
        isRobot: true,
        robotError: null
        };
    },
    mounted(){
      // remove any old token from localStorage
      localStorage.removeItem('imageassistant_access_token');
    },
    methods: {
        async login() {
            this.isLoading = true;
            const honeypotValue = document.querySelector('input[name="website"]').value;
            if(!this.email || !this.password) {
                this.error = 'Email and password are required.';
                this.isLoading = false;
                return;
            }
            if(this.isRobot) {
                this.robotError = 'Please verify you are not a robot.';
                this.isLoading = false;
                return;
            }
            try {
                const response = await fetch(`${this.apiUrl}/api/v1/custom/token/obtain/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: this.email,
                        password: this.password,
                        website: honeypotValue
                    })
                });
                
                if (response.ok) {
                    this.setIsAuthenticated(true);
                    this.$router.push('/'); // Navigate to home after successful login
                    const data = await response.json();
                    localStorage.setItem('imageassistant_access_token', data.access);
                    // Clear form on success
                    this.email = '';
                    this.password = '';
                    this.initializeAuth(); // Reinitialize auth to fetch user data
                } else {
                    if (response.status === 401) {
                        this.error = 'Invalid email or password.';
                    } else {
                        this.error = 'An unexpected error occurred. Please try again later.';
                    }
                }
            } catch (error) {
                this.error = 'An error occurred. Please try again.';
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