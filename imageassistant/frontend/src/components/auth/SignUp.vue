<template>
  <div class="min-h-screen bg-gray-900 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <div class="bg-gray-800 rounded-xl shadow-xl overflow-hidden">
        <div class="lg:grid lg:grid-cols-2">
          <!-- Left Column - Benefits -->
          <div class="bg-gradient-to-br from-indigo-600 to-purple-700 text-white p-8 lg:p-12">
            <div class="max-w-lg">
              <h1 class="text-3xl md:text-4xl font-bold mb-4">Let's get started</h1>
              <h3 class="text-xl font-medium text-indigo-100 mb-8">Create an account and enjoy our premium AI services.</h3>
              
              <div class="mt-8 space-y-6">
                <div class="flex items-start">
                  <div class="flex-shrink-0 bg-indigo-500 bg-opacity-30 p-2 rounded-lg">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 0 1 1-1h16a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V4zm5 4l4 4m0 0l4-4m-4 4v4"></path>
                    </svg>
                  </div>
                  <div class="ml-4">
                    <h4 class="text-lg font-semibold">Create Images with AI</h4>
                    <p class="mt-1 text-indigo-100">Generate unique images by simply describing what you want to see.</p>
                  </div>
                </div>
                
                <div class="flex items-start">
                  <div class="flex-shrink-0 bg-indigo-500 bg-opacity-30 p-2 rounded-lg">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5h16M4 12h16M4 19h16M9 5v14"></path>
                    </svg>
                  </div>
                  <div class="ml-4">
                    <h4 class="text-lg font-semibold">Remove Backgrounds</h4>
                    <p class="mt-1 text-indigo-100">Automatically remove image backgrounds with one click.</p>
                  </div>
                </div>
              </div>
              
              <div class="mt-12 hidden lg:block">
                <p class="text-indigo-100">Already have an account?</p>
                <RouterLink to="/users/login" class="mt-2 inline-flex items-center px-5 py-2 border border-indigo-300 text-base font-medium rounded-md text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-indigo-700 transition-colors duration-200">
                  Sign in
                  <svg xmlns="http://www.w3.org/2000/svg" class="ml-2 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </RouterLink>
              </div>
            </div>
          </div>
          
          <!-- Right Column - Signup Form -->
          <div class="p-8 lg:p-12">
            <div class="max-w-md mx-auto">
              <h2 class="text-2xl font-bold text-white mb-6">Create your account</h2>
              
              <div v-if="success" class="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 rounded-md shadow-sm mb-6 animate-fade-in" role="alert">
                <div class="flex items-center">
                  <svg class="h-5 w-5 mr-2 text-green-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  <div>
                    <strong class="font-bold">Account successfully created!</strong>
                    <RouterLink to="/users/login" class="ml-2 text-green-800 font-medium underline">
                      Proceed to login
                      <svg xmlns="http://www.w3.org/2000/svg" class="inline h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                      </svg>
                    </RouterLink>
                  </div>
                </div>
              </div>
              
              <form @submit.prevent="register" class="space-y-4">
                <!-- honeypot field -->
                <input type="text" name="website" style="display:none" tabindex="-1" autocomplete="off">
                
                <div class="mb-4">
                  <label for="email" class="block text-sm font-medium text-gray-300 mb-1">Email</label>
                  <div class="mt-1 relative rounded-md shadow-sm">
                    <input 
                      v-model="email" 
                      id="email" 
                      type="email" 
                      required 
                      class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-200"
                      placeholder="Enter your email address"
                    />
                  </div>
                  <p v-if="errors.email" class="mt-1 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md p-2">{{ errors.email }}</p>
                </div>
                
                <div class="mb-4">
                  <label for="password" class="block text-sm font-medium text-gray-300 mb-1">Password</label>
                  <div class="mt-1 relative rounded-md shadow-sm">
                    <input 
                      v-model="password" 
                      id="password" 
                      type="password" 
                      required 
                      class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-200"
                      placeholder="Create a password"
                    />
                  </div>
                  <p v-if="errors.password" class="mt-1 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md p-2">{{ errors.password }}</p>
                </div>
                
                <div class="mb-4">
                  <label for="password2" class="block text-sm font-medium text-gray-300 mb-1">Confirm Password</label>
                  <div class="mt-1 relative rounded-md shadow-sm">
                    <input 
                      v-model="password2" 
                      id="password2" 
                      type="password" 
                      required 
                      class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-200"
                      placeholder="Confirm your password"
                    />
                  </div>
                  <p v-if="errors.password2" class="mt-1 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md p-2">{{ errors.password2 }}</p>
                </div>
                <div class="mb-4">
                  <label for="first_name" class="block text-sm font-medium text-gray-300 mb-1">First Name</label>
                  <div class="mt-1 relative rounded-md shadow-sm">
                    <input 
                      v-model="first_name" 
                      id="first_name" 
                      type="text" 
                      required 
                      class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-200"
                      placeholder="Enter your first name"
                    />
                  </div>
                  <p v-if="errors.first_name" class="mt-1 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md p-2">{{ errors.first_name }}</p>
                </div>
                <div class="mb-4">
                  <label for="last_name" class="block text-sm font-medium text-gray-300 mb-1">Last Name</label>
                  <div class="mt-1 relative rounded-md shadow-sm">
                    <input 
                      v-model="last_name" 
                      id="last_name" 
                      type="text" 
                      required 
                      class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors duration-200"
                      placeholder="Enter your last name"
                    />
                  </div>
                  <p v-if="errors.last_name" class="mt-1 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md p-2">{{ errors.last_name }}</p>
                </div>
                
                <p class="mt-2 text-sm text-gray-400">
                  By creating an account, or signing up with google you agree to our 
                  <RouterLink to="/privacy-policy" class="text-indigo-400 font-medium hover:text-indigo-300 underline decoration-2 decoration-indigo-400 transition-all px-1 py-0.5 rounded hover:bg-indigo-900">
                    Privacy Policy
                  </RouterLink>
                  and  
                  <RouterLink to="/terms-conditions" class="text-indigo-400 font-medium hover:text-indigo-300 underline decoration-2 decoration-indigo-400 transition-all px-1 py-0.5 rounded hover:bg-indigo-900">
                    Terms and Conditions
                  </RouterLink>
                </p>
                
                <button 
                  type="submit" 
                  :disabled="isLoading"
                  class="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200 disabled:bg-indigo-800 disabled:cursor-not-allowed"
                >
                  <svg v-if="!isLoading" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
                  </svg>
                  {{ isLoading ? 'Creating Account...' : 'Create Account' }}
                </button>
              </form>
              <div v-if="!isLoading" class="mt-4">
                <RobotChecker :onVerified="isRobotVerified" />
                <p v-if="robotError" class="mt-1 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md p-2">{{ robotError }}</p>
              </div>
              <div class="mt-6">
                <div class="relative">
                  <div class="absolute inset-0 flex items-center">
                    <div class="w-full border-t border-gray-600"></div>
                  </div>
                  <div class="relative flex justify-center text-sm">
                    <span class="px-2 bg-gray-800 text-gray-400">Or</span>
                  </div>
                </div>
                
                <!-- <button 
                  @click="initiateGoogleLogin" 
                  class="w-full mt-4 py-3 px-4 bg-gray-700 border border-gray-600 hover:bg-gray-600 text-gray-300 font-medium rounded-md shadow-sm flex items-center justify-center transition duration-150"
                >
                  <svg class="h-5 w-5 mr-2" viewBox="0 0 24 24">
                    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                    <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                    <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                  </svg>
                  Continue with Google
                </button> -->
                <div id="visible-google-signin" class="mt-4 w-full" @click="initiateGoogleLogin"></div>
                
                <div class="mt-6 text-center lg:hidden">
                  <p class="text-sm text-gray-400">Already have an account?</p>
                  <RouterLink to="/users/login" class="mt-2 text-indigo-400 hover:text-indigo-300 font-medium">
                    Sign in to your account
                  </RouterLink>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import { RouterLink } from 'vue-router';
import { API_URL } from '../../config.js';
import RobotChecker from '../RobotChecker.vue';

export default {
  name: 'SignUp',
  components: {
    RouterLink,
    RobotChecker
  },
  props:{
    setIsAuthenticated: {
      type: Function,
      required: true
    },
    initializeAuth: {
      type: Function,
      required: true
    },
    GOOGLE_CLIENT_ID: {
      type: String,
      required: true
    },
    GOOGLE_LOGIN_REDIRECT_URI: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      email: '',
      password: '',
      password2: '',
      isLoading: false,
      success: false,
      errors: {
        email: null,
        password: null,
        password2: null,
        first_name: null,
        last_name: null,
        non_field_errors: null
      },
      apiUrl: API_URL,
      googleAuthInitialized: false,
      isRobot: true,
      robotError: null,
    };
  },
  mounted() {
      this.loadGoogleScript();
  },
  methods: {
      loadGoogleScript() {
        // Load Google Sign-In API
        const script = document.createElement('script')
        script.src = "https://accounts.google.com/gsi/client"
        script.async = true
        script.defer = true
        script.onload = this.initializeGoogleAuth
        document.head.appendChild(script)
    },
    initializeGoogleAuth() {
      console.log(this.apiUrl, this.GOOGLE_CLIENT_ID);
      window.google.accounts.id.initialize({
        client_id: this.GOOGLE_CLIENT_ID,
        callback: this.handleGoogleCredentialResponse,
        auto_select: false,
        cancel_on_tap_outside: true,
      });
        // Render the button
      window.google.accounts.id.renderButton(
        document.getElementById('visible-google-signin'),
        { 
          theme: 'outline',
          size: 'large',
          text: 'continue_with',
          width: '100%'
        }
      );
      this.googleAuthInitialized = true;
    },
    async register() {
      this.isLoading = true;
      this.clearErrors();
      // Validate passwords match
      if (this.password !== this.password2) {
        this.errors.password2 = "Passwords don't match";
        this.isLoading = false;
        return;
      }
      if(this.isRobot) {
        this.robotError = 'Please verify you are not a robot.';
        this.isLoading = false;
        return;
      }
      try {
        const response = await fetch(`${this.apiUrl}/api/v1/users/signup/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
            password2: this.password2,
            first_name: this.first_name,
            last_name: this.last_name
          })
        });
        
        const data = await response.json();
        
        if (response.ok) {
          this.success = true;
          this.clearForm();
        } else {
          // Handle API validation errors
          if (data.email) this.errors.email = data.email[0];
          if (data.password) this.errors.password = data.password[0];
          if (data.password2) this.errors.password2 = data.password2[0];
          if (data.first_name) this.errors.first_name = data.first_name[0];
          if (data.last_name) this.errors.last_name = data.last_name[0];
          if (data.non_field_errors) this.errors.general = data.non_field_errors[0];
        }
      } catch (error) {
        console.error('Registration error:', error);
      } finally {
        this.isLoading = false;
      }
    },
    
    
    clearErrors() {
      this.errors = {
        username: null,
        email: null,
        password: null,
        password2: null,
        general: null
      };
    },
    
    clearForm() {
      this.username = '';
      this.email = '';
      this.password = '';
      this.password2 = '';
    },
    async handleGoogleCredentialResponse(response) {
        // Send the ID token to your backend
        try {
          console.log(`${this.apiUrl}/api/v1/google/login/`);
          const backendResponse = await fetch(`${this.apiUrl}/api/v1/google/login/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
              credential: response.credential 
            })
          });
          const data = await backendResponse.json();
          if (backendResponse.ok) {
            // Handle successful authentication
            localStorage.setItem('imageassistant_access_token', data.access);
            this.setIsAuthenticated(true);
            this.initializeAuth();
            this.$router.push('/');
          } else {
            console.error('Google auth backend error:', await backendResponse.text());
          }
        } catch (error) {
          console.error('Error during Google authentication:', error);
        }
      },
      isRobotVerified(isRobot) {
        this.isRobot = isRobot;
        this.robotError = null;
      }
  }
};
</script>
