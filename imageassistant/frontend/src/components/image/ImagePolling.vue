<template>
  <div v-if="polling" class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75 z-[9999]">
    <div class="bg-gray-700 rounded-lg shadow-lg p-6 max-w-md w-full">
      <h2 class="text-xl font-semibold mb-4 text-white">Image Generation</h2>
      
      <!-- Skeleton Loader -->
      <div class="mb-4">
        <!-- Image placeholder -->
        <div class="w-full h-64 bg-gray-600 rounded-lg mb-4 relative overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-r from-gray-600 via-gray-500 to-gray-600 animate-pulse"></div>
          <div class="absolute inset-0 bg-gradient-to-r from-transparent via-gray-400 to-transparent animate-shimmer"></div>
        </div>
        
        <!-- Title placeholder -->
        <div class="h-4 bg-gray-600 rounded mb-2 w-3/4 animate-pulse"></div>
        
        <!-- Description lines -->
        <div class="h-3 bg-gray-600 rounded mb-2 w-full animate-pulse"></div>
        <div class="h-3 bg-gray-600 rounded mb-2 w-5/6 animate-pulse"></div>
        <div class="h-3 bg-gray-600 rounded w-2/3 animate-pulse"></div>
      </div>
      
      <p class="mb-4 text-center text-gray-300">Your image is being generated. Please wait...</p>
      <p class="text-sm text-gray-400 text-center">This may take up to 30 seconds</p>
    </div>
  </div>
</template>

<script>import { API_URL } from '../../config.js';

export default {
    name: 'ImagePolling',
    data() {
        return {
            prompt: '',
            imageUrl: '',
            pollingInterval: null,
            polling: this.formSubmitted
        };
    },
    props: {
        formSubmitted: {
            type: Boolean,
            default: false
        },
        imageId: {
            type: Number,
            required: true
        },
        getCompletedImage: {
            type: Function,
            required: true
        },
        showError: {
            type: Function,
            required: true
        },
        user:{
            type: Object,
            default: () => ({})
        }
    },
    watch: {
        formSubmitted(newVal) {
            if (newVal) {
                this.startPolling();
                this.polling = true; // Set polling to true when form is submitted
            } else {
                this.stopPolling();
                this.polling = false; // Set polling to false when form is not submitted
            }
        }
    },
    methods: {
        startPolling() {
            // Start polling immediately
            this.checkImageStatus();
            
            // Set up interval for repeated polling
            this.pollingInterval = setInterval(() => {
                this.checkImageStatus();
            }, 5000); // Check every 5 seconds
        },
        
        stopPolling() {
            if (this.pollingInterval) {
                clearInterval(this.pollingInterval);
                this.pollingInterval = null;
            }
        },
        
        async checkImageStatus() {
            try {
                const token = localStorage.getItem('imageassistant_access_token');
                if (!token) {
                    this.showError({ message: 'Authentication token not found. Please log in again.' });
                    this.stopPolling();
                    return;
                }

                const response = await fetch(
                    `${API_URL}/api/v1/image/status/${this.imageId}/`,
                    {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        }
                    }
                );
                
                if (response.status === 401) {
                    this.showError({ message: 'Authentication expired. Please log in again.' });
                    this.stopPolling();
                    return;
                }

                const data = await response.json();
                
                if (response.status === 200) {
                    // Instead of modifying the prop directly, call parent function
                    this.getCompletedImage(data);
                    this.stopPolling(); // Stop polling once image is ready
                    this.polling = false; // Set polling to false when image is ready
                } else if (response.status === 404) {
                    this.showError({ message: 'Image not found or access denied.' });
                    this.stopPolling();
                } else if (response.status !== 202) {
                    // 202 means still processing, anything else is an error
                    this.showError({ message: data.detail || 'An error occurred while processing the image.' });
                    this.stopPolling();
                }
            } catch (error) {
                console.error('Error checking image status:', error);
                this.showError({ message: 'Network error. Please check your connection and try again.' });
                this.stopPolling(); // Stop polling on error
            }
        }
    },
    mounted() {
        if (this.formSubmitted) {
            this.startPolling();
        }
    },
    beforeUnmount() {
        // Clean up interval when component is destroyed
        this.stopPolling();
    }
};
</script>

<style scoped>
@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.animate-shimmer {
  animation: shimmer 2s infinite;
}
</style>