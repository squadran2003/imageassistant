<template>
  <!-- Loading state -->
  <div v-if="!user || !user.isAuthenticated" class="bg-gray-900 min-h-screen py-8 flex items-center justify-center">
    <div class="text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500 mx-auto mb-4"></div>
      <p class="text-gray-300">Loading...</p>
    </div>
  </div>

  <div v-else class="bg-gray-900 min-h-screen py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-white">Your Images</h1>
        <p class="mt-2 text-gray-300">View and manage all your processed images</p>
      </div>

      <!-- Loading state for images -->
      <div v-if="loading" class="flex items-center justify-center py-12">
        <div class="text-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500 mx-auto mb-4"></div>
          <p class="text-gray-300">Loading your images...</p>
        </div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="bg-red-900/20 border border-red-500 rounded-lg p-6 mb-8">
        <div class="flex items-center">
          <svg class="w-5 h-5 text-red-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
          <span class="text-red-400">{{ error }}</span>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else-if="images.length === 0 && !loading" class="text-center py-12">
        <svg class="mx-auto h-24 w-24 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <h3 class="mt-4 text-lg font-medium text-gray-300">No images yet</h3>
        <p class="mt-2 text-gray-400">Start creating images to see them here</p>
        <div class="mt-6">
          <router-link 
            to="/generate/image/" 
            class="inline-flex items-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-md transition-colors duration-200"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Create Your First Image
          </router-link>
        </div>
      </div>

      <!-- Images Grid -->
      <div v-else class="space-y-8">
        <!-- Images grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          <div 
            v-for="image in images" 
            :key="image.id" 
            class="bg-gray-800 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300"
          >
            <!-- Image -->
            <div class="aspect-square bg-gray-700 relative group">
              <img 
                :src="getImageUrl(image)" 
                :alt="image.prompt || 'User image'"
                class="w-full h-full object-cover cursor-pointer"
                @click="openImageModal(image)"
                @error="handleImageError"
              />
              <!-- Overlay on hover -->
              <div class="absolute inset-0 bg-black bg-opacity-50 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center">
                <button 
                  @click="openImageModal(image)"
                  class="text-white hover:text-indigo-300 transition-colors"
                >
                  <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
              </div>
            </div>
            
            <!-- Image info -->
            <div class="p-4">
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-400">
                  {{ formatDate(image.created) }}
                </span>
                <div class="flex space-x-2">
                  <button 
                    @click="downloadImage(image)"
                    class="text-gray-400 hover:text-white transition-colors"
                    title="Download"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                  </button>
                </div>
              </div>
              <p v-if="image.prompt" class="text-sm text-gray-300 mt-2 line-clamp-2">
                {{ image.prompt }}
              </p>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="pagination && pagination.count > 10" class="flex items-center justify-between border-t border-gray-700 pt-6">
          <div class="flex-1 flex justify-between sm:hidden">
            <button 
              @click="goToPage(currentPage - 1)"
              :disabled="!pagination.previous"
              :class="[
                'relative inline-flex items-center px-4 py-2 text-sm font-medium rounded-md',
                pagination.previous 
                  ? 'bg-gray-800 text-gray-300 hover:bg-gray-700' 
                  : 'bg-gray-900 text-gray-500 cursor-not-allowed'
              ]"
            >
              Previous
            </button>
            <button 
              @click="goToPage(currentPage + 1)"
              :disabled="!pagination.next"
              :class="[
                'ml-3 relative inline-flex items-center px-4 py-2 text-sm font-medium rounded-md',
                pagination.next 
                  ? 'bg-gray-800 text-gray-300 hover:bg-gray-700' 
                  : 'bg-gray-900 text-gray-500 cursor-not-allowed'
              ]"
            >
              Next
            </button>
          </div>
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-400">
                Showing 
                <span class="font-medium text-white">{{ startIndex }}</span>
                to 
                <span class="font-medium text-white">{{ endIndex }}</span>
                of 
                <span class="font-medium text-white">{{ pagination.count }}</span>
                images
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                <button 
                  @click="goToPage(currentPage - 1)"
                  :disabled="!pagination.previous"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-600 bg-gray-800 text-sm font-medium text-gray-400 hover:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
                </button>
                
                <span v-for="page in visiblePages" :key="page">
                  <button 
                    v-if="page !== '...'"
                    @click="goToPage(page)"
                    :class="[
                      'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                      page === currentPage 
                        ? 'z-10 bg-indigo-600 border-indigo-600 text-white' 
                        : 'bg-gray-800 border-gray-600 text-gray-300 hover:bg-gray-700'
                    ]"
                  >
                    {{ page }}
                  </button>
                  <span v-else class="relative inline-flex items-center px-4 py-2 border border-gray-600 bg-gray-800 text-sm font-medium text-gray-400">
                    ...
                  </span>
                </span>
                
                <button 
                  @click="goToPage(currentPage + 1)"
                  :disabled="!pagination.next"
                  class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-600 bg-gray-800 text-sm font-medium text-gray-400 hover:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                  </svg>
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Image Modal -->
  <div v-if="selectedImage" class="fixed inset-0 z-50 overflow-y-auto" @click="closeImageModal">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 transition-opacity" @click="closeImageModal">
        <div class="absolute inset-0 bg-gray-900 bg-opacity-75"></div>
      </div>
      
      <div class="inline-block align-bottom bg-gray-800 rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full sm:p-6" @click.stop>
        <div class="sm:flex sm:items-start">
          <div class="w-full">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-medium text-white">
                Image Details
              </h3>
              <button @click="closeImageModal" class="text-gray-400 hover:text-white">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div class="mb-4">
              <img 
                :src="getImageUrl(selectedImage)" 
                :alt="selectedImage.prompt || 'User image'"
                class="w-full max-h-96 object-contain rounded-lg"
              />
            </div>
            
            <div class="space-y-3">
              <div v-if="selectedImage.prompt">
                <label class="block text-sm font-medium text-gray-300">Prompt:</label>
                <p class="text-gray-300 bg-gray-700 p-3 rounded-md">{{ selectedImage.prompt }}</p>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-300">Created:</label>
                <p class="text-gray-300">{{ formatDate(selectedImage.created) }}</p>
              </div>
              
              <div v-if="selectedImage.aspect_ratio">
                <label class="block text-sm font-medium text-gray-300">Aspect Ratio:</label>
                <p class="text-gray-300">{{ selectedImage.aspect_ratio }}</p>
              </div>
            </div>
            
            <div class="mt-6 flex justify-end space-x-3">
              <button 
                @click="downloadImage(selectedImage)"
                class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200"
              >
                Download
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { API_URL } from '../../config.js';
export default {
  name: 'UserImages',
  props: {
    user: {
      type: Object,
      required: false,
      default: () => ({ isAuthenticated: false })
    }
  },
  data() {
    return {
      images: [],
      loading: false,
      error: null,
      pagination: null,
      currentPage: 1,
      selectedImage: null
    };
  },
  computed: {
    startIndex() {
      if (!this.pagination || this.images.length === 0) return 0;
      return (this.currentPage - 1) * 10 + 1;
    },
    endIndex() {
      if (!this.pagination) return this.images.length;
      return Math.min(this.startIndex + this.images.length - 1, this.pagination.count);
    },
    totalPages() {
      if (!this.pagination) return 1;
      return Math.ceil(this.pagination.count / 10);
    },
    visiblePages() {
      const pages = [];
      const total = this.totalPages;
      const current = this.currentPage;
      
      // Always show first page
      pages.push(1);
      
      // Add ellipsis if needed
      if (current > 4) {
        pages.push('...');
      }
      
      // Add pages around current page
      for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) {
        if (!pages.includes(i)) {
          pages.push(i);
        }
      }
      
      // Add ellipsis if needed
      if (current < total - 3) {
        pages.push('...');
      }
      
      // Always show last page (if more than 1 page)
      if (total > 1 && !pages.includes(total)) {
        pages.push(total);
      }
      
      return pages;
    }
  },
  async mounted() {
    if (this.user && this.user.isAuthenticated) {
      await this.fetchImages();
    }
  },
  watch: {
    'user.isAuthenticated': {
      handler(newValue) {
        if (newValue) {
          this.fetchImages();
        }
      }
    }
  },
  methods: {
    async fetchImages(page = 1) {
      this.loading = true;
      this.error = null;
      
      try {
        const token = localStorage.getItem('imageassistant_access_token');
        if (!token) {
          this.error = 'Authentication token not found. Please log in again.';
          return;
        }

        const response = await fetch(`${API_URL}/api/v1/user/images/?page=${page}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.status === 401) {
          this.error = 'Authentication expired. Please log in again.';
          this.$router.push('/users/login');
          return;
        }

        const data = await response.json();
        
        if (response.ok) {
          this.images = data.results || data;
          this.pagination = {
            count: data.count,
            next: data.next,
            previous: data.previous
          };
          this.currentPage = page;
        } else {
          this.error = data.detail || 'Failed to load images.';
        }
      } catch (error) {
        console.error('Error fetching images:', error);
        this.error = 'Network error. Please check your connection and try again.';
      } finally {
        this.loading = false;
      }
    },
    
    async goToPage(page) {
      if (page < 1 || page > this.totalPages) return;
      await this.fetchImages(page);
    },
    
    getImageUrl(image) {
      if (image.alternate_url) {
        return image.alternate_url;
      }
      if (image.image) {
        return image.image.startsWith('http') ? image.image : `${API_URL}${image.image}`;
      }
      return '';
    },
    
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    
    openImageModal(image) {
      this.selectedImage = image;
    },
    
    closeImageModal() {
      this.selectedImage = null;
    },
    
    downloadImage(image) {
      const url = this.getImageUrl(image);
      if (!url) return;
      
      const filename = this.getImageFilename(image);
      
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
        .catch(error => {
          console.error('Error downloading image:', error);
          this.error = 'Failed to download image.';
        });
    },
    
    getImageFilename(image) {
      if (image.image) {
        const urlParts = image.image.split('/');
        let filename = urlParts[urlParts.length - 1];
        
        if (filename.includes('?')) {
          filename = filename.split('?')[0];
        }
        
        if (!filename.includes('.')) {
          filename += '.png';
        }
        
        return filename;
      }
      
      return 'image.png';
    },
    
    handleImageError(event) {
      event.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIGZpbGw9Im5vbmUiIHN0cm9rZT0iY3VycmVudENvbG9yIiB2aWV3Qm94PSIwIDAgMjQgMjQiPjxwYXRoIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgc3Ryb2tlLXdpZHRoPSIyIiBkPSJNNCAxNmw0LjU4Ni00LjU4NmEyIDIgMCAwMTIuODI4IDBMMTYgMTZtLTItMmwxLjU4Ni0xLjU4NmEyIDIgMCAwMTIuODI4IDBMMjAgMTRtLTYtNmguMDFNNiAyMGgxMmEyIDIgMCAwMDItMlY2YTIgMiAwIDAwLTItMkg2YTIgMiAwIDAwLTIgMnYxMmEyIDIgMCAwMDIgMnoiPjwvcGF0aD48L3N2Zz4=';
    }
  }
};
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.aspect-square {
  aspect-ratio: 1 / 1;
}
</style>