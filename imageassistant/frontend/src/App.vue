<template>
  <div v-if="isInitializing" class="min-h-screen bg-gray-900 flex items-center justify-center">
    <div class="text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500 mx-auto mb-4"></div>
      <p class="text-gray-300">Loading...</p>
    </div>
  </div>
  <BaseLayout v-else>
     <!-- Pass Nav component to navigation slot -->
    <template #navigation>
      <NavBar :user="currentUser" :key="navbarKey"/>
    </template>
    <template #content>
       <RouterView 
       :user="currentUser" :setIsAuthenticated="setIsAuthenticated" 
       :initializeAuth="initializeAuth"
      :GOOGLE_CLIENT_ID="GOOGLE_CLIENT_ID"
      :GOOGLE_LOGIN_REDIRECT_URI="GOOGLE_LOGIN_REDIRECT_URI"
      :STRIPE_PUBLIC_KEY="STRIPE_PUBLIC_KEY"
      :CREDIT_MULTIPLIER="CREDIT_MULTIPLIER"
      :DEV_MODE="DEV_MODE"
      @paymentSuccess="onPaymentSuccess"
      />
    </template>


  </BaseLayout>
</template>

<script>

import BaseLayout from './components/BaseLayout.vue'
import NavBar from './components/NavBar.vue'
import { RouterView } from 'vue-router'
import { API_URL } from './config.js'


export default {
  name: 'App',
  components: {
    BaseLayout,
    NavBar,
    RouterView
  },
  data() {
    return {
      currentUser: {
        isAuthenticated: false,
        credits: 0,
        token: '',
        featureFlags: [], // Initialize feature flags
      },
      navbarKey: 0, // Force NavBar re-render
      isInitializing: true, // Flag to show loading state
      GOOGLE_CLIENT_ID: '',
      GOOGLE_LOGIN_REDIRECT_URI: '',
      STRIPE_PUBLIC_KEY: '', // Add Stripe public key
      CREDIT_MULTIPLIER: null,
      DEV_MODE: false, // Add dev mode flag
      API_URL: API_URL
    }
  },
  async mounted() {
    await this.getPublicConfig(); // Fetch public config on mount
    await this.initializeAuth();
  },
  methods: {
    async initializeAuth() {
      try {
        // Check if user is authenticated on mount
        const token = localStorage.getItem('imageassistant_access_token');
        
        if (token) {
          this.currentUser.isAuthenticated = true;
          this.currentUser.token = token;
          fetch(`${this.API_URL}/api/v1/user/info/`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            }
          })
          .then(response => {
            if (response.status === 401) {
              // force relogin and clear invalid token
              localStorage.removeItem('imageassistant_access_token');
              this.currentUser.isAuthenticated = false;
              this.currentUser.token = '';
              this.$router.push('/users/login');
              throw new Error('Unauthorized');
            }
            return response.json();
          })
          .then(userData => {
            this.currentUser.credits = userData.credits || 0;
            this.currentUser.featureFlags = userData.feature_flags || []; // Set feature flags
            this.navbarKey++;
          })
          .catch(error => {
            console.error('Error fetching user information:', error);
          });
        }
      } catch (error) {
        // Clear invalid token
        localStorage.removeItem('imageassistant_access_token');
      } finally {
        this.isInitializing = false; // Allow components to render
      }
    },
    setIsAuthenticated(isAuthenticated) {
      this.currentUser.isAuthenticated = isAuthenticated;
      this.navbarKey++; // Increment key to force re-render
    },
    onPaymentSuccess(data) {
      // Handle successful payment and update user credits
      this.currentUser.credits += data.credits;
      this.navbarKey++; // Force NavBar re-render to show updated credits
    },
    async getPublicConfig() {
      try{
        // Fetch public configuration from the API
        const response = await fetch(`${API_URL}/api/v1/public/config/`);
        const config = await response.json();
        this.GOOGLE_CLIENT_ID = config.GOOGLE_CLIENT_ID || '';
        this.GOOGLE_LOGIN_REDIRECT_URI = config.GOOGLE_LOGIN_REDIRECT_URI || '';
        this.STRIPE_PUBLIC_KEY = config.STRIPE_PUBLIC_KEY || ''; // Set Stripe public key
        this.CREDIT_MULTIPLIER = config.CREDIT_MULTIPLIER || 50; // Set credit multiplier
        this.DEV_MODE = config.DEV_MODE || false; // Set dev mode status
      } catch (error) {
        console.error('Error fetching public config:', error);
      } 
    },
  }
}
</script>
