<template>
    <div class="py-12 bg-gray-900">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center">
                <h2 class="text-base font-semibold tracking-wide uppercase text-indigo-400">Features</h2>
                <p class="mt-2 text-3xl font-extrabold text-white sm:text-4xl">Everything you need for AI image generation</p>
                <p class="mt-4 max-w-2xl text-xl text-gray-300 mx-auto">
                    Create stunning visuals with simple text prompts
                </p>
            </div>

            <div class="mt-10">
                <div class="space-y-10 md:space-y-0 md:grid md:grid-cols-3 md:gap-x-8 md:gap-y-10">
                    <div class="relative bg-gray-800 p-6 rounded-lg border border-gray-700 hover:border-indigo-500 transition-colors duration-300">
                        <div class="absolute -top-4 left-6 flex items-center justify-center h-12 w-12 rounded-md bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                            </svg>
                        </div>
                        <div class="mt-4">
                            <h3 class="text-lg font-medium text-white">Generate Images</h3>
                            <p class="mt-2 text-base text-gray-300">
                                Turn your ideas into images with our advanced AI. Just describe what you want to see.
                            </p>
                        </div>
                    </div>

                    <div class="relative bg-gray-800 p-6 rounded-lg border border-gray-700 hover:border-indigo-500 transition-colors duration-300">
                        <div class="absolute -top-4 left-6 flex items-center justify-center h-12 w-12 rounded-md bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                        </div>
                        <div class="mt-4">
                            <h3 class="text-lg font-medium text-white">Image Outline</h3>
                            <p class="mt-2 text-base text-gray-300">
                                Create outlines for your images to focus on key elements. Perfect for presentations and designs.
                            </p>
                        </div>
                    </div>

                    <div class="relative bg-gray-800 p-6 rounded-lg border border-gray-700 hover:border-indigo-500 transition-colors duration-300">
                        <div class="absolute -top-4 left-6 flex items-center justify-center h-12 w-12 rounded-md bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                            </svg>
                        </div>
                        <div class="mt-4">
                            <h3 class="text-lg font-medium text-white">Edit Images</h3>
                            <p class="mt-2 text-base text-gray-300">
                                Remove backgrounds instantly. Enhanced editing and visual effects coming soon.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "FeaturesBanner",
};
</script>