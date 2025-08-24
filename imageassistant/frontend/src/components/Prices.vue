<template>
  <div class="min-h-screen bg-gray-900">
    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <!-- Header Section -->
      <div class="text-center mb-16">
        <h1 class="text-4xl font-bold text-white mb-4">
          Service Pricing
        </h1>
        <p class="text-xl text-gray-300 max-w-3xl mx-auto">
          Transform your images with our AI-powered tools. Each service costs a specific number of credits.
        </p>
      </div>

      <!-- Pricing Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
        <!-- Remove Background -->
        <div class="bg-gray-800 rounded-2xl shadow-lg border border-gray-700 p-8 hover:shadow-xl hover:border-gray-600 transition-all duration-300">
          <div class="text-center">
            <div class="bg-blue-900 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4h4a4 4 0 004-4V5z"></path>
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-white mb-2">Remove Background</h3>
            <p class="text-gray-400 mb-6">Automatically remove backgrounds from your images with AI precision</p>
            <div class="text-center">
              <span class="text-4xl font-bold text-blue-400">3</span>
              <span class="text-gray-400 ml-2">credits</span>
            </div>
          </div>
        </div>

        <!-- Generate Image -->
        <div class="bg-gray-800 rounded-2xl shadow-lg border-2 border-purple-600 p-8 hover:shadow-xl transition-all duration-300 relative">
          <div class="text-center">
            <div class="bg-purple-900 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-white mb-2">Generate Image</h3>
            <p class="text-gray-400 mb-6">Create stunning images from text descriptions using advanced AI</p>
            <div class="text-center">
              <span class="text-4xl font-bold text-purple-400">9</span>
              <span class="text-gray-400 ml-2">credits</span>
            </div>
            <div class="bg-purple-900 text-purple-200 text-xs font-semibold px-3 py-1 rounded-full mt-4">
              Most Popular
            </div>
          </div>
        </div>

        <!-- Image Outline -->
        <div class="bg-gray-800 rounded-2xl shadow-lg border border-gray-700 p-8 hover:shadow-xl hover:border-gray-600 transition-all duration-300">
          <div class="text-center">
            <div class="bg-green-900 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path>
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-white mb-2">Image Outline</h3>
            <p class="text-gray-400 mb-6">Convert images to coloring book style outlines perfect for printing</p>
            <div class="text-center">
              <span class="text-4xl font-bold text-green-400">2</span>
              <span class="text-gray-400 ml-2">credits</span>
            </div>
            <div class="bg-green-900 text-green-200 text-xs font-semibold px-3 py-1 rounded-full mt-4">
              Best Value
            </div>
          </div>
        </div>

        <!-- Grayscale Image -->
        <div class="bg-gray-800 rounded-2xl shadow-lg border border-gray-700 p-8 hover:shadow-xl hover:border-gray-600 transition-all duration-300">
          <div class="text-center">
            <div class="bg-gray-700 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-white mb-2">Grayscale Image</h3>
            <p class="text-gray-400 mb-6">Convert your images to elegant black and white grayscale</p>
            <div class="text-center">
              <span class="text-4xl font-bold text-gray-400">1</span>
              <span class="text-gray-400 ml-2">credits</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Credits Information -->
      <div class="bg-gray-800 rounded-2xl shadow-lg border border-gray-700 p-8 mb-12 mt-4">
        <div class="text-center mb-8">
          <h2 class="text-3xl font-bold text-white mb-4">How Credits Work</h2>
          <p class="text-gray-300 max-w-2xl mx-auto">
            Credits are our virtual currency that you use to access our AI-powered image services. 
            Each service requires a different number of credits based on its complexity.
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="text-center">
            <div class="bg-blue-900 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4">
              <span class="text-blue-400 font-bold">1</span>
            </div>
            <h3 class="font-semibold text-white mb-2">Purchase Credits</h3>
            <p class="text-gray-400 text-sm">Buy credit packages that suit your needs</p>
          </div>
          
          <div class="text-center">
            <div class="bg-purple-900 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4">
              <span class="text-purple-400 font-bold">2</span>
            </div>
            <h3 class="font-semibold text-white mb-2">Use Services</h3>
            <p class="text-gray-400 text-sm">Spend credits on the services you need</p>
          </div>
          
          <div class="text-center">
            <div class="bg-green-900 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4">
              <span class="text-green-400 font-bold">3</span>
            </div>
            <h3 class="font-semibold text-white mb-2">Get Results</h3>
            <p class="text-gray-400 text-sm">Download your processed images instantly</p>
          </div>
        </div>
      </div>

      <!-- Buy Credits CTA -->
      <div v-if="user.isAuthenticated" class="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl shadow-lg p-8 text-center text-white">
        <div class="mb-6">
          <div class="bg-white/20 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
            </svg>
          </div>
          <h2 class="text-3xl font-bold mb-4">Need More Credits?</h2>
          <p class="text-xl text-white/90 max-w-2xl mx-auto">
            Purchase credit packages to unlock unlimited access to our AI-powered image processing services
          </p>
        </div>
        
        <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <router-link 
            to="/checkout" 
            class="bg-white text-indigo-600 hover:bg-gray-100 font-bold py-4 px-8 rounded-lg transition duration-300 transform hover:scale-105 shadow-lg inline-flex items-center"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
            Buy More Credits
          </router-link>
          
          <div class="text-white/80 text-sm">
            <p>💳 Secure payment • ⚡ Instant delivery • 🔄 No subscription required</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PricesPage',
  inheritAttrs: false,
  props: {
   user: {
      type: Object,
      default: () => ({})
    }
  },
}
</script>