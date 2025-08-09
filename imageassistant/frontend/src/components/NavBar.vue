<template>
     <!-- Navigation -->
    <nav class="bg-gray-800 border-b border-gray-700 shadow-lg sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16"> 
            <div class="flex items-center">
                <a href="/" class="flex-shrink-0 flex items-center">
                    <span class="text-xl font-bold text-gray-300">ImageAssistant.io</span>
                </a>
            </div>
          
          <!-- Desktop Navigation -->
          <div class="hidden md:flex md:items-center md:space-x-6">
            <RouterLink to="/" class="text-gray-300 hover:text-indigo-400 px-3 py-2 text-sm font-medium transition-colors duration-200">
              Home
            </RouterLink>
            <RouterLink to="/contact" class="text-gray-300 hover:text-indigo-400 px-3 py-2 text-sm font-medium transition-colors duration-200">
              Contact
            </RouterLink>
            <RouterLink to="/faq" class="text-gray-300 hover:text-indigo-400 px-3 py-2 text-sm font-medium transition-colors duration-200">
              FAQs
            </RouterLink>
            <RouterLink to="/pricing" class="text-gray-300 hover:text-indigo-400 px-3 py-2 text-sm font-medium transition-colors duration-200">
              Prices
            </RouterLink>
            
            <!-- Services Dropdown (Authenticated Users) -->
            <div v-if="isAuthenticated" class="relative" ref="servicesDropdown">
              <button @click="toggleServicesMenu" class="text-gray-300 hover:text-indigo-400 px-3 py-2 text-sm font-medium flex items-center transition-colors duration-200">
                Services
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
              
              <div v-show="showServicesMenu" class="absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-gray-700 ring-1 ring-gray-600 ring-opacity-50">
                <div class="py-1">
                  <RouterLink to="/generate/image/" class="block px-4 py-2 text-sm text-gray-200 hover:bg-gray-600 hover:text-indigo-300 transition-colors duration-200">
                    Generate Image
                  </RouterLink>
                  <RouterLink to="/remove/background" class="block px-4 py-2 text-sm text-gray-200 hover:bg-gray-600 hover:text-indigo-300 transition-colors duration-200">
                    Remove Background
                  </RouterLink>
                  <RouterLink to="/create/outline" class="block px-4 py-2 text-sm text-gray-200 hover:bg-gray-600 hover:text-indigo-300 transition-colors duration-200">
                    Create Image Outline
                  </RouterLink>
                  <RouterLink to="/create/grayscale" class="block px-4 py-2 text-sm text-gray-200 hover:bg-gray-600 hover:text-indigo-300 transition-colors duration-200">
                    Create Grayscale Image
                  </RouterLink>
                </div>
              </div>
            </div>

            <!-- User Menu (Authenticated Users) -->
            <div v-if="isAuthenticated" class="relative ml-3" ref="userDropdown">
              <button @click="toggleUserMenu" class="text-gray-300 hover:text-indigo-400 px-2 py-2 text-sm font-medium flex items-center transition-colors duration-200">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
              
              <div v-show="showUserMenu" class="absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-gray-700 ring-1 ring-gray-600 ring-opacity-50">
                <div class="py-1">
                  <!-- Credits Display -->
                  <div v-if="user.featureFlags.includes('show_credits')" class="px-4 py-2 text-sm text-gray-200 border-b border-gray-600">
                    <div class="flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-indigo-400" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z" />
                        <path fill-rule="evenodd" d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" clip-rule="evenodd" />
                      </svg>
                      <span class="font-medium text-gray-200">Credits: </span>
                      <span class="ml-1 font-semibold text-green-400">
                        {{ user.credits }}
                      </span>
                      <RouterLink to="/checkout" class="ml-2 text-indigo-400 hover:text-indigo-300 text-sm transition-colors duration-200">
                        Buy More
                      </RouterLink>
                    </div>
                  </div>
                  
                  <RouterLink to="/users/images/" class="block px-4 py-2 text-sm text-gray-200 hover:bg-gray-600 hover:text-indigo-300 transition-colors duration-200">
                    <div class="flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      Your Images
                    </div>
                  </RouterLink>
                  <RouterLink to="/users/logout" class="block px-4 py-2 text-sm text-gray-200 hover:bg-gray-600 hover:text-indigo-300 transition-colors duration-200">
                    <div class="flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                      </svg>
                      Logout
                    </div>
                  </RouterLink>
                </div>
              </div>
            </div>
            
            <!-- Login Button (Non-authenticated Users) -->
            <RouterLink 
              v-if="!isAuthenticated" 
              to="/users/login" 
              class="ml-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 focus:ring-offset-gray-800 transition-all duration-200"
            >
              Login
            </RouterLink>
            
          </div>

          <!-- Mobile Menu Button -->
          <div class="flex items-center md:hidden">
            <button @click="toggleMobileMenu" ref="mobileMenuButton" class="inline-flex items-center justify-center p-2 rounded-md text-gray-300 hover:text-indigo-400 hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500 transition-colors duration-200">
              <span class="sr-only">Open main menu</span>
              <svg class="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
        
        <!-- Mobile Menu -->
        <div v-if="showMobileMenu" class="bg-gray-800 border-t border-gray-700" ref="mobileMenu">
          <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            <RouterLink to="/" class="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-indigo-400 hover:bg-gray-700 transition-colors duration-200">
              Home
            </RouterLink>
            <RouterLink to="/contact" class="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-indigo-400 hover:bg-gray-700 transition-colors duration-200">
              Contact
            </RouterLink>
            <RouterLink to="/faq" class="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-indigo-400 hover:bg-gray-700 transition-colors duration-200">
              FAQs
            </RouterLink>
            <RouterLink to="/pricing" class="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-indigo-400 hover:bg-gray-700 transition-colors duration-200">
              Prices
            </RouterLink>
            
            <!-- Mobile Services Section (Authenticated Users) -->
            <div v-if="isAuthenticated">
              <button @click="toggleMobileServices" class="w-full flex items-center justify-between px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-indigo-400 hover:bg-gray-700 transition-colors duration-200">
                <span>Services</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transform transition-transform duration-200" :class="{ 'rotate-180': showMobileServices }" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
              
              <div v-show="showMobileServices" class="pl-4 space-y-1">
                <RouterLink to="/generate/image/" class="block px-3 py-2 rounded-md text-sm font-medium text-gray-400 hover:text-indigo-300 hover:bg-gray-700 transition-colors duration-200">
                  Generate Image
                </RouterLink>
                <RouterLink to="/remove/background" class="block px-3 py-2 rounded-md text-sm font-medium text-gray-400 hover:text-indigo-300 hover:bg-gray-700 transition-colors duration-200">
                  Remove Background
                </RouterLink>
                <RouterLink to="/create/outline" class="block px-3 py-2 rounded-md text-sm font-medium text-gray-400 hover:text-indigo-300 hover:bg-gray-700 transition-colors duration-200">
                  Create Image Outline
                </RouterLink>
                <RouterLink to="/create/grayscale" class="block px-3 py-2 rounded-md text-sm font-medium text-gray-400 hover:text-indigo-300 hover:bg-gray-700 transition-colors duration-200">
                  Create Grayscale Image
                </RouterLink>
              </div>
            </div>
            
            <!-- Mobile User Section (Authenticated Users) -->
            <div v-if="isAuthenticated" class="border-t border-gray-700 pt-2 mt-2">
              <!-- Credits Display -->
              <div v-if="user.featureFlags && user.featureFlags.includes('show_credits')" class="px-3 py-2 text-sm text-gray-300 bg-gray-700 rounded-md mb-2">
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-indigo-400" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z" />
                      <path fill-rule="evenodd" d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" clip-rule="evenodd" />
                    </svg>
                    <span class="font-medium text-gray-300">Credits: </span>
                    <span class="ml-1 font-semibold text-green-400">{{ user.credits }}</span>
                  </div>
                  <RouterLink to="/add-credit" class="text-indigo-400 hover:text-indigo-300 text-sm transition-colors duration-200">
                    Buy More
                  </RouterLink>
                </div>
              </div>
              
              <RouterLink to="/users/images/" class="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-indigo-400 hover:bg-gray-700 transition-colors duration-200">
                <div class="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  Your Images
                </div>
              </RouterLink>
              
              <RouterLink to="/users/logout" class="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-indigo-400 hover:bg-gray-700 transition-colors duration-200">
                <div class="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  Logout
                </div>
              </RouterLink>
            </div>
            
            <!-- Mobile Login Button (Non-authenticated Users) -->
            <RouterLink 
              v-if="!isAuthenticated"
              to="/users/login" 
              class="block w-full text-center px-3 py-2 mt-2 rounded-md text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700 transition-colors duration-200"
            >
              Login
            </RouterLink>
          </div>
        </div>
      </div>
    </nav>
</template>
<script>
import { RouterLink } from 'vue-router'
export default {
  name: 'NavBar',
  components: {
    RouterLink
  },
  props: {
    user: {
      type: Object,
      required: true,
      default: () => ({
        isAuthenticated: false,
        credits: 0,
        showCredits: true
      })
    }
  },
  data() {
    return {
      isAuthenticated: this.user.isAuthenticated,
      showServicesMenu: false,
      showUserMenu: false,
      showMobileMenu: false,
      showMobileServices: false
    }
  },
  watch: {
    'user.isAuthenticated': {
      handler(newValue) {
        this.isAuthenticated = newValue;
      },
      immediate: true
    }
  },
  mounted() {
  // Add event listener when component is mounted
  document.addEventListener('click', this.handleClickOutside);
  },
  beforeUnmount() {
    // Remove event listener when component is destroyed
    document.removeEventListener('click', this.handleClickOutside);
  },
  methods: {
    toggleServicesMenu() {
      this.showServicesMenu = !this.showServicesMenu;
      this.showUserMenu = false; // Close other dropdowns
    },
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu;
      this.showServicesMenu = false; // Close other dropdowns
    },
    toggleMobileMenu() {
      this.showMobileMenu = !this.showMobileMenu;
    },
    toggleMobileServices() {
      this.showMobileServices = !this.showMobileServices;
    },
    handleClickOutside(event) {
     // Check if click is outside services dropdown
      if (this.$refs.servicesDropdown && !this.$refs.servicesDropdown.contains(event.target)) {
        this.showServicesMenu = false;
      }
      
      // Check if click is outside user dropdown
      if (this.$refs.userDropdown && !this.$refs.userDropdown.contains(event.target)) {
        this.showUserMenu = false;
      }

      // Check if click is outside mobile menu and mobile menu button
      if (this.showMobileMenu && 
          this.$refs.mobileMenu && 
          !this.$refs.mobileMenu.contains(event.target) &&
          this.$refs.mobileMenuButton && 
          !this.$refs.mobileMenuButton.contains(event.target)) {
        this.showMobileMenu = false;
      }
    }
  }
}
</script>