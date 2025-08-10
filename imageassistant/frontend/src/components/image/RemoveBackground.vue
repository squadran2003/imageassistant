<template>
  <ImagePolling 
    v-if="imageId"
    :formSubmitted="isProcessing"
    :imageId="imageId" 
    :getCompletedImage="getCompletedImage" 
    :showError="showErrorFromPolling"
    :user="user"
  />
  
  <!-- Loading state -->
  <div v-if="!user || !user.isAuthenticated" class="bg-gray-900 min-h-screen py-8 flex items-center justify-center">
    <div class="text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500 mx-auto mb-4"></div>
      <p class="text-gray-300">Loading...</p>
    </div>
  </div>

  <div v-else class="bg-gray-900 min-h-screen py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- Preview section - shows when image is processed or complete -->
      <div v-if="processedImage.url" class="p-6 w-full mb-8">
        <div class="bg-gray-800 rounded-lg p-6">
          <h3 class="text-xl font-bold text-white mb-4">Background Removed Successfully!</h3>
          <div class="bg-gray-700 rounded-lg p-4">
            <img 
              :src="processedImage.alternate_url ? processedImage.alternate_url : processedImage.url"
              :alt="processedImage.alt" 
              class="w-full rounded-lg shadow-lg" 
            />
          </div>
          <div class="mt-4 flex flex-wrap gap-3">
            <button
              @click="downloadImage()"
              class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg inline-flex items-center"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Download
            </button>
            <button
              @click="resetForm()"
              class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg"
            >
              Process Another Image
            </button>
          </div>
        </div>
      </div>

      <div v-if="!processedImage.url" class="bg-gray-800 rounded-lg shadow-xl overflow-hidden">
        <!-- Header section -->
        <div class="p-6 border-b border-gray-700">
          <h1 class="text-2xl font-bold text-white">Remove Background</h1>
          <p class="mt-2 text-gray-300">Upload an image to automatically remove its background using AI</p>
        </div>

        <!-- Form section -->
        <form @submit.prevent="processImage" class="p-6 space-y-6">
          <!-- File upload -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">
              Upload Image
            </label>
            <div 
              @drop="handleDrop"
              @dragover.prevent
              @dragenter.prevent
              class="border-2 border-dashed border-gray-600 rounded-lg p-6 text-center hover:border-gray-500 transition-colors"
            >
              <input 
                type="file" 
                ref="fileInput"
                @change="handleFileSelect"
                accept="image/jpeg,image/jpg,image/png,image/webp"
                class="hidden"
              />
              
              <div v-if="!selectedFile" @click="$refs.fileInput.click()" class="cursor-pointer">
                <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                  <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <p class="mt-2 text-sm text-gray-300">
                  <span class="font-medium text-indigo-400 hover:text-indigo-300">Click to upload</span> or drag and drop
                </p>
                <p class="text-xs text-gray-400">PNG, JPG, JPEG, WebP up to 10MB</p>
              </div>
              
              <div v-if="selectedFile" class="flex items-center justify-center space-x-4">
                <img 
                  :src="previewUrl" 
                  alt="Preview" 
                  class="h-32 w-32 object-cover rounded-lg"
                />
                <div class="text-left">
                  <p class="text-white font-medium">{{ selectedFile.name }}</p>
                  <p class="text-gray-400 text-sm">{{ formatFileSize(selectedFile.size) }}</p>
                  <button 
                    type="button"
                    @click="removeFile()"
                    class="mt-2 text-red-400 hover:text-red-300 text-sm"
                  >
                    Remove file
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Credits display -->
          <div class="bg-gray-700 rounded-lg p-4 flex items-center justify-between">
            <div>
              <h3 class="text-white font-medium">Your credits</h3>
              <p class="text-gray-300">{{ user.credits }} credits available</p>
            </div>
            <div class="text-right">
              <p class="text-white font-medium">Cost: 5 credits</p>
              <router-link 
                to="/users/credits/add" 
                class="text-indigo-400 hover:text-indigo-300 text-sm"
              >
                Need more credits?
              </router-link>
            </div>
          </div>

          <!-- Error message -->
          <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>

          <!-- Submit button -->
          <div>
            <button 
              type="submit" 
              class="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-800 disabled:cursor-not-allowed text-white font-medium py-3 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-800 transition-colors duration-200"
              :disabled="isProcessing || !selectedFile || user.credits < 5"
            >
              <span v-if="!isProcessing">Remove Background</span>
              <span v-else>Processing...</span>
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
  name: 'RemoveBackground',
  components: {
    ImagePolling
  },
  props: {
    user: {
      type: Object,
      required: false,
      default: () => ({ isAuthenticated: false, credits: 0 })
    }
  },
  data() {
    return {
      selectedFile: null,
      previewUrl: null,
      isProcessing: false,
      error: null,
      imageId: null,
      processedImage: {
        url: '',
        alt: '',
        alternate_url: ''
      }
    };
  },
  methods: {
    handleFileSelect(event) {
      const file = event.target.files[0];
      if (file) {
        this.setSelectedFile(file);
      }
    },
    
    handleDrop(event) {
      event.preventDefault();
      const files = event.dataTransfer.files;
      if (files.length > 0) {
        this.setSelectedFile(files[0]);
      }
    },
    
    setSelectedFile(file) {
      // Validate file type
      const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
      if (!allowedTypes.includes(file.type)) {
        this.error = 'Invalid file type. Only JPEG, PNG, and WebP are allowed.';
        return;
      }
      
      // Validate file size (10MB)
      if (file.size > 10 * 1024 * 1024) {
        this.error = 'File too large. Maximum size is 10MB.';
        return;
      }
      
      this.selectedFile = file;
      this.previewUrl = URL.createObjectURL(file);
      this.error = null;
    },
    
    removeFile() {
      this.selectedFile = null;
      if (this.previewUrl) {
        URL.revokeObjectURL(this.previewUrl);
        this.previewUrl = null;
      }
      this.error = null;
    },
    
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    
    async processImage() {
      if (!this.selectedFile) {
        this.error = 'Please select an image file';
        return;
      }
      
      if (this.user.credits < 5) {
        this.error = 'You need at least 5 credits to remove background';
        return;
      }
      
      this.isProcessing = true;
      this.error = null;
      
      try {
        const token = localStorage.getItem('imageassistant_access_token');
        const formData = new FormData();
        formData.append('image', this.selectedFile);
        
        const response = await fetch(`${API_URL}/api/v1/remove/background/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
          this.imageId = data.image_id;
        } else {
          this.error = data.detail || 'Failed to process image. Please try again.';
          this.isProcessing = false;
        }
      } catch (error) {
        console.error('Error processing image:', error);
        this.error = 'An unexpected error occurred. Please try again.';
        this.isProcessing = false;
      }
    },
    
    showErrorFromPolling(error) {
      this.error = error.message || 'An error occurred while processing image';
      this.isProcessing = false;
    },
    
    getCompletedImage(imageData) {
      this.processedImage = {
        url: `${API_URL}${imageData.image}`,
        alt: 'Background removed image',
        alternate_url: imageData.alternate_url
      };
      this.isProcessing = false;
      
      // Emit event to parent to update credits (Background removal costs 5 credits)
      this.$emit('creditsUsed', 5);
    },
    
    downloadImage() {
      const url = this.processedImage.alternate_url ? this.processedImage.alternate_url : this.processedImage.url;
      const filename = 'background-removed.png';
      
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
    },
    
    resetForm() {
      this.selectedFile = null;
      this.previewUrl = null;
      this.processedImage = { url: '', alt: '', alternate_url: '' };
      this.imageId = null;
      this.error = null;
      this.isProcessing = false;
    }
  },
  
  beforeUnmount() {
    if (this.previewUrl) {
      URL.revokeObjectURL(this.previewUrl);
    }
  }
};
</script>