<template>
    <div class="bg-gradient-to-r from-gray-900 via-slate-800 to-gray-900 py-16 border-b border-gray-700">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h1 class="text-4xl md:text-6xl font-extrabold text-white mb-2">
                <span class="block gradient-text">Turn Words Into Amazing Images</span>
            </h1>
            <p class="text-xl md:text-2xl font-medium text-gray-300 max-w-3xl mx-auto mb-8">
                Create stunning visuals instantly with AI-powered image generation
            </p>
        </div>
        <SearchBox />
        <div class="flex justify-center mt-6 mb-6" v-if="!isAuthenticated">
            <div class="inline-flex items-center bg-gradient-to-r from-indigo-500/20 to-purple-500/20 backdrop-blur-sm rounded-full px-6 py-3 border border-indigo-400/30 shadow-lg hover:shadow-indigo-500/25 transition-all duration-300 group">
                <div class="flex items-center">
                    <div class="bg-gradient-to-r from-yellow-400 to-orange-400 rounded-full p-2 mr-3 group-hover:scale-110 transition-transform duration-300">
                        <svg class="w-5 h-5 text-yellow-900" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                    </div>
                    <span class="text-white font-semibold text-lg">
                        🎉 <span class="text-transparent bg-clip-text bg-gradient-to-r from-yellow-300 to-orange-300 font-bold">100 FREE</span> Credits on Signup!
                    </span>
                    <!-- Small sparkle effect -->
                    <div class="ml-2 w-1 h-1 bg-yellow-300 rounded-full animate-ping"></div>
                </div>
            </div>
        </div>
    
        <div class="flex justify-center mt-8" v-if="isAuthenticated">
          <a href="#" class="inline-flex items-center px-8 py-4 border border-transparent text-lg font-bold rounded-full shadow-lg text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-300 transform hover:scale-105">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
              </svg>
              Create New Image
              <div class="ml-3 bg-white/20 text-white text-xs px-2 py-1 rounded-full">
                  AI Powered
              </div>
          </a>
      </div>


    </div>
    <FeaturesBanner />
    <GalleryView />
    <BackgroundRemovalExample />
</template>
<script>
import SearchBox from './SearchBox.vue';
import GalleryView from './GalleryView.vue';
import FeaturesBanner from './FeaturesBanner.vue';
import BackgroundRemovalExample from './BackgroundRemovalExample.vue';
 



export default {
  name: 'IndexPage',
  props:{
     user: {
        isAuthenticated: false,
      }
  },
  components: {
    SearchBox,
    FeaturesBanner,
    GalleryView,
    BackgroundRemovalExample
  },
  data() {
    return {
      isAuthenticated: this.user.isAuthenticated
    };
    
  }
}
</script>
<style scoped>
.gradient-text {
  background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 50%, #10b981 100%); 
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>