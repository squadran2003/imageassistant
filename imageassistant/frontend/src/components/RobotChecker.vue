<template>
  <div class="captcha-container bg-gray-800 p-4 rounded-lg border border-gray-700 mb-4">
    <div v-if="!verified && !loading" class="flex items-center">
      <div 
        class="flex items-center space-x-3 cursor-pointer"
        @click="verifyHuman"
      >
        <div 
          class="w-6 h-6 border-2 rounded flex items-center justify-center"
          :class="isChecked ? 'bg-indigo-600 border-indigo-600' : 'border-gray-500'"
        >
          <svg v-if="isChecked" class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </div>
        <span class="text-gray-200">I am a human</span>
      </div>
    </div>
    
    <div v-if="loading" class="py-2 flex items-center">
      <svg class="animate-spin h-5 w-5 mr-3 text-indigo-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <span class="text-gray-300">Verifying...</span>
    </div>
    
    <div v-if="verified" class="flex items-center text-green-500">
      <svg class="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
      </svg>
      <span class="font-medium">Verification successful!</span>
    </div>
    
    <p v-if="error" class="mt-2 text-sm text-red-500">{{ error }}</p>
  </div>
</template>

<script>
export default {
  name: 'RobotChecker',
  props: {
    // Allow parent component to know when verification is complete
    onVerified: {
      type: Function,
      default: () => {}
    }
  },
  data() {
    return {
      verified: false,
      loading: false,
      error: null,
      isChecked: false
    };
  },
  methods: {
    verifyHuman() {
      this.isChecked = true;
      this.loading = true;
      
      // Simulate a short verification delay to make it seem like it's checking something
      setTimeout(() => {
        this.verified = true;
        this.loading = false;
        this.onVerified(false);
      }, 1000);
    }
  }
};
</script>