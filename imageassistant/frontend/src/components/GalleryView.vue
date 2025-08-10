<template>
     <div class="text-center mb-2 mt-4">
        <h2 class="text-3xl font-extrabold text-white">Sample Gallery</h2>
        <p class="mt-2 text-lg text-gray-300">Check out what our AI can create</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 m-4 mt-0">
        <div class="group bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 border border-gray-100">
            <div class="relative h-56 sm:h-64 overflow-hidden bg-gradient-to-br from-purple-50 to-indigo-50">
                <img @error="handleImageError" :src="require('@/assets/img/kitten_in_a_forest.png')" alt="Kitten in a forest" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"/>
                <!-- Gradient overlay on hover -->
                <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                <!-- AI Generated Badge -->
                <div class="absolute top-3 right-3 transform translate-x-full group-hover:translate-x-0 transition-transform duration-300">
                    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg backdrop-blur-sm">
                        <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                        AI Generated
                    </span>
                </div>
            </div>
            <div class="p-5">
                <div class="flex items-start justify-between mb-3">
                    <h3 class="text-sm font-bold text-gray-900 group-hover:text-indigo-600 transition-colors duration-200">Kitten in a Forest</h3>
                </div>
                <p class="text-xs text-gray-600 mb-4 leading-relaxed">
                    <span class="font-medium text-indigo-600">Prompt:</span> kitten in a forest
                </p>
            </div>
        </div>

        <div class="group bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 border border-gray-100">
            <div class="relative h-56 sm:h-64 overflow-hidden bg-gradient-to-br from-green-50 to-emerald-50">
                <img @error="handleImageError" :src="require('@/assets/img/man_walking_in_the_forest.png')" alt="Man walking in the forest" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"/>
                <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                <div class="absolute top-3 right-3 transform translate-x-full group-hover:translate-x-0 transition-transform duration-300">
                    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg backdrop-blur-sm">
                        <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                        AI Generated
                    </span>
                </div>
            </div>
            <div class="p-5">
                <div class="flex items-start justify-between mb-3">
                    <h3 class="text-sm font-bold text-gray-900 group-hover:text-indigo-600 transition-colors duration-200">Man Walking in Forest</h3>
                </div>
                <p class="text-xs text-gray-600 mb-4 leading-relaxed">
                    <span class="font-medium text-indigo-600">Prompt:</span> Man walking in the forest
                </p>
            </div>
        </div>
        <div class="group bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 border border-gray-100">
            <div class="relative h-56 sm:h-64 overflow-hidden bg-gradient-to-br from-green-50 to-emerald-50">
                <img @error="handleImageError" :src="require('@/assets/img/animated_dog.png')" alt="Animated dog" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"/>
                <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                <div class="absolute top-3 right-3 transform translate-x-full group-hover:translate-x-0 transition-transform duration-300">
                    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg backdrop-blur-sm">
                        <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                        AI Generated
                    </span>
                </div>
            </div>
            <div class="p-5">
                <div class="flex items-start justify-between mb-3">
                    <h3 class="text-sm font-bold text-gray-900 group-hover:text-indigo-600 transition-colors duration-200">Create a image of a animated dog</h3>
                </div>
                <p class="text-xs text-gray-600 mb-4 leading-relaxed">
                    <span class="font-medium text-indigo-600">Prompt:</span> Create a image of a animated dog
                </p>
            </div>
        </div>

        <div class="group bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 border border-gray-100">
            <div class="relative h-56 sm:h-64 overflow-hidden bg-gradient-to-br from-green-50 to-emerald-50">
                <img @error="handleImageError" :src="require('@/assets/img/rat_in_a_trap.png')" alt="Rat in a trap" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"/>
                <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                <div class="absolute top-3 right-3 transform translate-x-full group-hover:translate-x-0 transition-transform duration-300">
                    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg backdrop-blur-sm">
                        <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                        </svg>
                        AI Generated
                    </span>
                </div>
            </div>
            <div class="p-5">
                <div class="flex items-start justify-between mb-3">
                    <h3 class="text-sm font-bold text-gray-900 group-hover:text-indigo-600 transition-colors duration-200">Rat in a trap</h3>
                </div>
                <p class="text-xs text-gray-600 mb-4 leading-relaxed">
                    <span class="font-medium text-indigo-600">Prompt:</span> Rat in a trap
                </p>
            </div>
        </div>
    </div>
</template>
<script>
export default {
  name: 'GalleryView',
  props: {
    images: {
      type: Array,
      required: false,
      default: () => []
    }
  },
    methods: {
    handleImageError(event) {
      // Create SVG as data URL
      const svgContent = `
        <svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600">
          <rect width="600" height="600" fill="#f3f4f6"/>
          <g transform="translate(300,300)">
            <circle cx="0" cy="-20" r="80" fill="#e5e7eb" stroke="#d1d5db" stroke-width="2"/>
            <path d="M-40,-40 L40,0 L-40,40 Z" fill="#9ca3af"/>
            <text x="0" y="60" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" fill="#6b7280">
              Image Not Found
            </text>
          </g>
        </svg>
      `;
      
      const svgBlob = new Blob([svgContent], { type: 'image/svg+xml' });
      const svgUrl = URL.createObjectURL(svgBlob);
      event.target.src = svgUrl;
    }
  }
}   
</script>