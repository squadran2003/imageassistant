<template>
  <div class="min-h-screen bg-gray-900">
    <div class="max-w-3xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <h1 class="text-3xl font-bold text-white mb-8 text-center">Frequently Asked Questions</h1>
      
      <div class="space-y-4">
        <!-- FAQ Item 1 -->
        <div class="bg-gray-800 rounded-lg shadow-sm border border-gray-700">
          <button 
            @click="toggleFAQ(1)" 
            class="w-full px-6 py-4 text-left focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-800 rounded-lg flex justify-between items-center hover:bg-gray-750 transition-colors duration-200"
          >
            <span class="font-medium text-gray-100">I don't see options to enhance and edit?</span>
            <svg 
              v-show="!openFAQ[1]" 
              xmlns="http://www.w3.org/2000/svg" 
              class="h-5 w-5 text-indigo-400" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <svg 
              v-show="openFAQ[1]" 
              xmlns="http://www.w3.org/2000/svg" 
              class="h-5 w-5 text-indigo-400" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 12H6" />
            </svg>
          </button>
          <div 
            v-show="openFAQ[1]" 
            class="px-6 pb-4 mt-2 transition-all duration-200 ease-out"
          >
            <p class="text-gray-300">These services will be available in the near future.</p>
          </div>
        </div>
      
        <!-- FAQ Item 2 -->
        <div class="bg-gray-800 rounded-lg shadow-sm border border-gray-700">
          <button 
            @click="toggleFAQ(2)" 
            class="w-full px-6 py-4 text-left focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-800 rounded-lg flex justify-between items-center hover:bg-gray-750 transition-colors duration-200"
          >
            <span class="font-medium text-gray-100">Is it free to use?</span>
            <svg 
              v-show="!openFAQ[2]" 
              xmlns="http://www.w3.org/2000/svg" 
              class="h-5 w-5 text-indigo-400" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <svg 
              v-show="openFAQ[2]" 
              xmlns="http://www.w3.org/2000/svg" 
              class="h-5 w-5 text-indigo-400" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 12H6" />
            </svg>
          </button>
          <div 
            v-show="openFAQ[2]" 
            class="px-6 pb-4 mt-2 transition-all duration-200 ease-out"
          >
            <p class="text-gray-300">The platform is not free to use. You can earn 100 credits when you sign up and then purchase additional credits as needed.</p>
          </div>
        </div>
      
        <!-- FAQ Item 3 -->
        <div class="bg-gray-800 rounded-lg shadow-sm border border-gray-700">
          <button 
            @click="toggleFAQ(3)" 
            class="w-full px-6 py-4 text-left focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-800 rounded-lg flex justify-between items-center hover:bg-gray-750 transition-colors duration-200"
          >
            <span class="font-medium text-gray-100">How many images can I download?</span>
            <svg 
              v-show="!openFAQ[3]" 
              xmlns="http://www.w3.org/2000/svg" 
              class="h-5 w-5 text-indigo-400" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <svg 
              v-show="openFAQ[3]" 
              xmlns="http://www.w3.org/2000/svg" 
              class="h-5 w-5 text-indigo-400" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 12H6" />
            </svg>
          </button>
          <div 
            v-show="openFAQ[3]" 
            class="px-6 pb-4 mt-2 transition-all duration-200 ease-out"
          >
            <p class="text-gray-300">You can download as many as you like. We only deduct credits when you use a service not when you download an image.</p>
          </div>
        </div>
      
        <!-- FAQ Item 4 -->
        <div class="bg-gray-800 rounded-lg shadow-sm border border-gray-700">
          <button 
            @click="toggleFAQ(4)" 
            class="w-full px-6 py-4 text-left focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-800 rounded-lg flex justify-between items-center hover:bg-gray-750 transition-colors duration-200"
          >
            <span class="font-medium text-gray-100">Why doesn't the background removal service work?</span>
            <svg 
              v-show="!openFAQ[4]" 
              xmlns="http://www.w3.org/2000/svg" 
              class="h-5 w-5 text-indigo-400" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <svg 
              v-show="openFAQ[4]" 
              xmlns="http://www.w3.org/2000/svg" 
              class="h-5 w-5 text-indigo-400" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 12H6" />
            </svg>
          </button>
          <div 
            v-show="openFAQ[4]" 
            class="px-6 pb-4 mt-2 transition-all duration-200 ease-out"
          >
            <p class="text-gray-300">There are instances when the AI model is unable to remove the background, when this happens we do not charge you for the image.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FAQPage',
  data() {
    return {
      openFAQ: {
        1: false,
        2: false,
        3: false,
        4: false
      }
    }
  },
  methods: {
    toggleFAQ(id) {
      this.openFAQ[id] = !this.openFAQ[id]
    }
  }
}
</script>