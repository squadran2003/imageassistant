<template>
    <div class="py-16 bg-gray-900">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-12">
                <div class="relative inline-block">
                    <h2 class="text-3xl font-extrabold text-white sm:text-4xl">
                        Remove Background 
                        <span class="relative">
                            <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">Instantly</span>
                            <!-- Animated underline -->
                            <div class="absolute bottom-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 transform scale-x-0 origin-left transition-transform duration-700 group-hover:scale-x-100"></div>
                            <!-- Magic wand icon -->
                            <svg class="absolute -top-2 -right-8 w-6 h-6 text-yellow-400 animate-bounce" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/>
                            </svg>
                        </span>
                    </h2>
                    <!-- Reduced sparkles - only one floating sparkle -->
                    <div class="absolute -top-4 right-1/4 w-2 h-2 bg-purple-400 rounded-full animate-ping delay-700"></div>
                </div>
                
                <p class="mt-6 max-w-3xl text-xl text-gray-300 mx-auto leading-relaxed">
                    Perfect for 
                    <span class="font-semibold text-indigo-400">product photos</span>, 
                    <span class="font-semibold text-purple-400">portraits</span>, and 
                    <span class="font-semibold text-pink-400">creative projects</span>
                    <br>
                    <span class="text-lg text-gray-400 mt-2 block">
                        ✨ No complex software • 🎯 Pixel-perfect results • ⚡ Lightning fast
                    </span>
                </p>
                
                <!-- Progress indicator -->
                <div class="mt-8 flex justify-center">
                    <div class="flex items-center space-x-2 text-sm text-gray-400">
                        <div class="flex items-center">
                            <div class="w-3 h-3 bg-green-400 rounded-full mr-2 animate-pulse"></div>
                            <span>AI Processing Active</span>
                        </div>
                        <span class="mx-2">•</span>
                        <span>99.9% Accuracy Rate</span>
                    </div>
                </div>
            </div>
            
            <!-- Before/After Comparison -->
            <div class="flex flex-col md:flex-row md:items-center md:space-x-8 lg:space-x-16">
                <!-- Left Side (Before) -->
                <div class="flex-1 mb-8 md:mb-0">
                    <div class="relative rounded-xl overflow-hidden shadow-2xl transform hover:scale-105 transition-all duration-500 border-4 border-gray-700 hover:border-gray-600">
                        <img :src="require('@/assets/img/cat_and_dog_fighting.png')" alt="Product with background" class="w-full h-auto object-cover" @error="handleImageError">
                        
                        <div class="absolute top-4 left-4 bg-red-500 bg-opacity-90 rounded-lg px-3 py-1 text-sm font-bold text-white shadow-lg">
                            ✗ Before
                        </div>
                        
                        <!-- Light gradient overlay only on hover -->
                        <div class="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent opacity-0 hover:opacity-100 transition-opacity duration-300"></div>
                    </div>
                    <p class="mt-4 text-center text-gray-300 font-semibold text-lg">Original Image with Background</p>
                </div>
                
                <!-- Animated Arrow for desktop -->
                <div class="hidden md:flex items-center justify-center">
                    <div class="relative">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-indigo-400 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                        </svg>
                        <!-- Magic sparkles around arrow -->
                        <div class="absolute -top-2 -right-2 w-4 h-4 bg-yellow-400 rounded-full animate-ping"></div>
                        <div class="absolute -bottom-2 -left-2 w-3 h-3 bg-purple-400 rounded-full animate-ping delay-300"></div>
                    </div>
                </div>
                
                <!-- Animated Arrow for mobile -->
                <div class="flex md:hidden items-center justify-center mb-8">
                    <div class="relative">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-indigo-400 animate-bounce" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                        </svg>
                        <div class="absolute -top-2 -right-2 w-4 h-4 bg-yellow-400 rounded-full animate-ping"></div>
                    </div>
                </div>
                
                <!-- Right Side (After) -->
               <div class="flex-1">
                    <div class="relative rounded-xl overflow-hidden shadow-2xl transform hover:scale-105 transition-all duration-500 border-4 border-green-500 hover:border-green-400 shadow-green-500/20">
                        <!-- Keep the checkerboard for the "after" image to show transparency -->
                        <div class="absolute inset-0 bg-gradient-to-br from-gray-800 via-gray-700 to-gray-800 checkerboard-pattern-dark"></div>
                        <img :src="require('@/assets/img/cat_and_dog_no_background.png')" alt="Product with background removed" class="w-full h-auto object-cover relative z-10" @error="handleImageError">
                        <div class="absolute top-4 left-4 bg-green-500 bg-opacity-90 rounded-lg px-3 py-1 text-sm font-bold text-white shadow-lg z-20">
                            ✓ After
                        </div>
                        <!-- Success glow effect -->
                        <div class="absolute inset-0 bg-gradient-to-t from-green-900/30 via-transparent to-transparent z-10"></div>
                        <!-- Floating sparkle effects -->
                        <div class="absolute top-8 right-8 w-2 h-2 bg-yellow-400 rounded-full animate-ping delay-500"></div>
                        <div class="absolute bottom-12 left-8 w-3 h-3 bg-blue-400 rounded-full animate-ping delay-700"></div>
                    </div>
                    <p class="mt-4 text-center text-gray-300 font-semibold text-lg">Background Magically Removed ✨</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'BackgroundRemovalExample',
    data() {
        return {
            // Data properties can be added here if needed
        };
    },
    methods: {
        handleImageError(event) {
            const svgContent = `
                <svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600">
                    <rect width="600" height="600" fill="#1f2937"/>
                    <g transform="translate(300,300)">
                        <!-- Image icon -->
                        <rect x="-40" y="-30" width="80" height="60" fill="none" stroke="#6b7280" stroke-width="3" rx="4"/>
                        <circle cx="-20" cy="-10" r="6" fill="#6b7280"/>
                        <path d="M-30,10 L-10,-10 L10,10 L30,15 L30,20 L-30,20 Z" fill="#6b7280"/>
                        
                        <!-- X mark -->
                        <g transform="translate(25,-25)">
                            <circle r="12" fill="#ef4444"/>
                            <path d="M-6,-6 L6,6 M6,-6 L-6,6" stroke="white" stroke-width="2" stroke-linecap="round"/>
                        </g>
                    </g>
                    
                    <text x="300" y="360" text-anchor="middle" font-family="system-ui, sans-serif" font-size="16" fill="#9ca3af">
                        Image Not Available
                    </text>
                </svg>
            `;
            
            event.target.src = 'data:image/svg+xml;base64,' + btoa(svgContent);
        }
    }
};
</script>

<style scoped>
.checkerboard-pattern-dark {
    background-image: 
        linear-gradient(45deg, #374151 25%, transparent 25%), 
        linear-gradient(-45deg, #374151 25%, transparent 25%), 
        linear-gradient(45deg, transparent 75%, #374151 75%), 
        linear-gradient(-45deg, transparent 75%, #374151 75%);
    background-size: 20px 20px;
    background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
}


</style>