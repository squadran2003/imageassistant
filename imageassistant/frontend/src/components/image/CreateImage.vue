<template>
    <ImagePolling v-if="imageId"
        :formSubmitted="isGenerating"
        :imageId="imageId" 
        :getCompletedImage="getCompletedImage" 
        :showError="showErrorFromPolling"
        :user="user"
      />
  <div class="bg-gray-900 min-h-screen py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        
      <!-- Preview section - shows when image is being generated or complete -->
      <div v-if="image.url" class="p-6 w-full">
          
          <div class="bg-gray-700 rounded-lg p-4">
              <img 
                  :src="image.url" 
                  :alt="image.alt" 
                  class="w-full rounded-lg shadow-lg" 
              />
            </div>
            <div class="mt-4 flex flex-wrap gap-3">
                <a
                @click="downloadImage()"
                class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg inline-flex items-center cursor-pointer"
                >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                Download
                </a>
            </div>
      </div>
      <div v-if="!image.url" class="bg-gray-800 rounded-lg shadow-xl overflow-hidden">
        <!-- Header section -->
        <div class="p-6 border-b border-gray-700">
          <h1 class="text-2xl font-bold text-white">Create AI Image</h1>
          <p class="mt-2 text-gray-300">Generate unique AI-powered images from your text descriptions</p>
        </div>

        <!-- Form section -->
        <form @submit.prevent="generateImage" class="p-6 space-y-6">
          <!-- Prompt input -->
          <div>
            <label for="prompt" class="block text-sm font-medium text-gray-300 mb-2">
              What do you want to create?
            </label>
            <textarea 
              id="prompt" 
              v-model="prompt" 
              rows="3" 
              class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Describe the image you want to generate..."
              required
            ></textarea>
            <p class="text-xs text-gray-400 mt-2">
              Be specific and detailed for best results. 
              <span class="text-indigo-400">{{ charactersLeft }} characters left</span>
            </p>
          </div>

          <!-- Image size selection -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">
              Image Size
            </label>
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
              <div>
                    <label class="block text-sm font-medium text-gray-300 mb-2">
                        Aspect Ratio
                    </label>
                    <select 
                        v-model="aspectRatio" 
                        class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    >
                        <option value="1:1">1:1 (Square)</option>
                        <option value="16:9">16:9 (Widescreen)</option>
                        <option value="21:9">21:9 (Ultrawide)</option>
                        <option value="2:3">2:3 (Portrait)</option>
                        <option value="3:2">3:2 (Landscape)</option>
                        <option value="4:5">4:5 (Portrait)</option>
                        <option value="5:4">5:4 (Landscape)</option>
                        <option value="9:16">9:16 (Mobile)</option>
                        <option value="9:21">9:21 (Tall)</option>
                    </select>
                    <p class="text-xs text-gray-400 mt-2">
                        Select the aspect ratio for your generated image
                    </p>
                </div>
            </div>
          </div>

          <!-- Style selection -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">
              Image Style
            </label>
            <select 
              v-model="style" 
              class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="photo">Photorealistic</option>
              <option value="digital">Digital Art</option>
              <option value="anime">Anime</option>
              <option value="cartoon">Cartoon</option>
              <option value="painting">Painting</option>
            </select>
          </div>

          <!-- Credits display -->
          <div class="bg-gray-700 rounded-lg p-4 flex items-center justify-between">
            <div>
              <h3 class="text-white font-medium">Your credits</h3>
              <p class="text-gray-300">{{ user.credits }} credits available</p>
            </div>
            <div class="text-right">
              <p class="text-white font-medium">Cost: 10 credits</p>
              <router-link 
                to="/checkout" 
                class="text-indigo-400 hover:text-indigo-300 text-sm"
              >
               Buy more credits.
              </router-link>
            </div>
          </div>

          <!-- Error message -->
          <p v-if="error" class="text-red-500 text-sm mt-2">{{ error }}</p>

          <!-- Submit button -->
          <div>
            <button 
              type="submit" 
              class="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-800 disabled:cursor-not-allowed text-white font-medium py-3 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-800 transition-colors duration-200"
              :disabled="isGenerating || prompt.length === 0 || credits < 10"
            >
              <span >Generate Image</span>
            </button>
          </div>
        </form>

      </div>
    </div>
  </div>
</template>

<script>
import ImagePolling from './ImagePolling.vue';
import { API_URL } from '../../config.js';


export default {
  name: 'CreateImage',
  props:{
    user: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      prompt: '',
      aspectRatio: '16:9', // Default aspect ratio
      style: 'photo',
      isGenerating: false,
      generatedImageUrl: '',
      error: null,
      credits: 100, // This would come from your user data
      maxPromptLength: 500,
      image: {
        url: '',
        alt: '',
        alternate_url: ''
      },
      imageId: null
    };
  },
  computed: {
    charactersLeft() {
      return this.maxPromptLength - this.prompt.length;
    }
  },
    components: {
        ImagePolling
    },
  methods: {
    
    async generateImage() {
      if (this.prompt.length === 0) {
        this.error = 'Please enter a prompt to generate an image';
        return;
      }

      if (this.user.credits < 10) {
        this.error = 'You need at least 10 credits to generate an image';
        return;
      }
      
      this.isGenerating = true;
      this.error = null;
      
      try {
        const token = localStorage.getItem('imageassistant_access_token');

        const response = await fetch(`${API_URL}/api/v1/create/image/from/prompt/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            prompt: this.prompt,
            aspect_ratio: this.imageSize,
            style: this.style
          })
        });
        
        const data = await response.json();
        
        if (response.ok) {
          this.generatedImageUrl = data.image_url;
          this.imageId = data.detail; // Store the image ID for polling
        } else {
          this.error = data.detail || 'Failed to generate image. Please try again.';
        }
      } catch (error) {
        console.error('Error generating image:', error);
        this.error = 'An unexpected error occurred. Please try again.';
      } 
    },
    showErrorFromPolling(error) {
      this.error = error.message || 'An error occurred while checking image status';
      this.isGenerating = false; // Stop polling if there's an error
    },
    getCompletedImage(imageData) {
      this.image = {
        url: `${API_URL}${imageData.image}`,
        alt: this.prompt,
        alternate_url: imageData.alternate_url
      };
      this.isGenerating = false; // Stop generating state
      this.credits -= 10; // Deduct credits after successful generation
    },
    getImageFilename(url) {
        // Extract filename from URL or create a default one
        if (!url) return 'generated-image.png';
        
        // Try to extract filename from URL
        const urlParts = url.split('/');
        let filename = urlParts[urlParts.length - 1];
        
        // If filename has query parameters, remove them
        if (filename.includes('?')) {
          filename = filename.split('?')[0];
        }
        
        // If no extension, add .png
        if (!filename.includes('.')) {
          filename += '.png';
        }
        // Ensure filename is safe for download  
      return filename;
    },
    downloadImage() {
      const url = this.image.alternate_url || this.image.url;
      const filename = this.getImageFilename(url);
      
      fetch(url)
        .then(response => response.blob())
        .then(blob => {
          const blobUrl = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.style.display = 'none';
          a.href = blobUrl;
          a.download = filename;
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(blobUrl);
          document.body.removeChild(a);
        })
        .catch(error => console.error('Error downloading image:', error));
    }
  }
};
</script>