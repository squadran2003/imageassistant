<template>
  <div class="min-h-screen dark-gradient-bg">
    <!-- Navigation Slot -->
    <slot name="navigation">
      <!-- Default navigation if none provided -->
      <nav class="bg-gray-900 border-b border-gray-800 shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between h-16">
            <div class="flex items-center">
              <span class="text-xl font-bold gradient-text-dark">ImageAssistant.io</span>
            </div>
          </div>
        </div>
      </nav>
    </slot>

   

    <!-- Main Content Slot -->
    <main class="bg-gray-950 min-h-screen">
      <slot name="content">
      </slot>
    </main>
  </div>
  <FooterComponent/>
</template>

<script>
import FooterComponent from './FooterComponent.vue';
export default {
  name: 'BaseLayout',
  components: {
    FooterComponent
  },
  data() {
    return {
      // Simple boolean values for showing/hiding menus
      showServicesMenu: false,
      showUserMenu: false,
      showMobileMenu: false,
      
      // Empty array for messages
      messages: [],
      
      // Simple user object
      user: {
        isAuthenticated: true, // Change this to test different states
        credits: 150,
        showCredits: true
      }
    }
  }
}
</script>

<style scoped>
.gradient-text-dark {
  background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>