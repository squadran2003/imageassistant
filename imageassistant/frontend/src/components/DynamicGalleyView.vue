<template>
    <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
        <div v-for="image in images" :key="image.id">
                <div class="relative h-56 sm:h-64 overflow-hidden">
                        <img v-if="image.alternate_url"   :src="image.alternate_url" :alt="image.alt" class="w-full h-full object-cover hover:scale-105 transition-transform duration-300"/>
                        <img v-else :src="image.image.url" :alt="image.alt" class="w-full h-full object-cover hover:scale-105 transition-transform duration-300"/>
                    <div class="absolute bottom-0 right-0 p-2">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-indigo-100 text-indigo-800">
                            AI Generated
                        </span>
                    </div>
                </div>
                <div class="p-4">
                    <p class="text-sm text-gray-700 font-medium">Prompt: {{ image.prompt }}</p>
                    <div class="mt-4">
                        <a v-if="image.alternate_url" :href="image.alternate_url" download="image.alternate_url" class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                            </svg>
                            Download
                        </a>
                        <a v-else :href="image.image.url" download="image.image.url" class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                            </svg>
                            Download
                        </a>
                    </div>
                </div>
        </div>
    </div>
</template>
<script>
export default {
  name: 'DynamicGalleryView',
  props: {
    images: {
      type: Array,
      required: true
    }
  }
}
</script>