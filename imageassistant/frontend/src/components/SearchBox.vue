<template>
    <div class="w-full max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 mt-2" id="drop-down-link">
        <form @submit="search">
            <div class="relative flex items-center w-full">
                <input type="text" name="q" placeholder="Search for images..." :value="searchQuery" @input="searchQuery = $event.target.value"
                    class="pl-10 pr-16 py-4 rounded-full border-2 border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white text-gray-700 text-base w-full shadow-lg transition-all duration-200 text-left" 
                    aria-label="Search images" required>
                
                <!-- Search Icon -->
                <div class="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                </div>
                
                <!-- Submit Button -->
                <button type="submit" class="absolute right-2 top-1/2 transform -translate-y-1/2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-full shadow-md transition-colors duration-200 flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                </button>
            </div>
        </form>
    </div>
</template>

<script>
export default {
  name: 'SearchBox',
  data() {
    return {
      searchQuery: ''
    }
  },
  methods: {
    search(e) {
        e.preventDefault();
      if (this.searchQuery.trim()) {
        // Here you would typically emit an event or call a method to perform the search
        // this.$emit('search', this.searchQuery);
      }
    }
  }
}
</script>