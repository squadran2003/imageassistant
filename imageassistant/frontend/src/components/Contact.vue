<template>
  <div class="min-h-screen bg-gray-900">
    <div class="max-w-3xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-white">Contact Us</h1>
        <p class="mt-2 text-lg text-gray-300">Have a question or feedback? We'd love to hear from you.</p>
      </div>

    <!-- Success Message -->
    <div v-if="showSuccess" class="mb-4 bg-green-100 border-l-4 border-green-500 text-green-700 p-4 rounded-md shadow-sm mb-6 animate-fade-in" role="alert">
      <div class="flex items-center">
        <svg class="h-5 w-5 mr-2 text-green-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
        </svg>
        <div>
          <strong class="font-bold">Success!</strong>
          <span class="block sm:inline"> Your message has been sent. We'll get back to you soon.</span>
        </div>
      </div>
    </div>

    <!-- General Error Message -->
    <div v-if="errors.general" class="mb-4 bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md shadow-sm mb-6" role="alert">
      <div class="flex items-center">
        <svg class="h-5 w-5 mr-2 text-red-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
        <div>
          <strong class="font-bold">Error!</strong>
          <span class="block sm:inline"> {{ errors.general }}</span>
        </div>
      </div>
    </div>

      <!-- Contact Form -->
      <div class="bg-gray-800 rounded-lg shadow-md overflow-hidden border border-gray-700">
        <div class="px-6 pb-6 py-6">
        <form @submit.prevent="submitForm" class="space-y-4">
            <!-- Name Field -->
            <div class="mb-4">
              <label class="block text-gray-200 font-medium mb-2">
                Name
                <div class="mt-1">
                  <input 
                    type="text" 
                    v-model="form.name"
                    class="w-full px-3 py-2 border border-gray-600 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 bg-gray-700 text-gray-100 placeholder-gray-400 sm:text-sm"
                    required
                    placeholder="Your full name"
                  >
                </div>
              </label>
              <div v-if="errors.name" class="mt-1 text-sm text-red-400 bg-red-900 border border-red-700 rounded-md p-2">
                {{ errors.name }}
              </div>
            </div>

            <!-- Email Field -->
            <div class="mb-4">
              <label class="block text-gray-200 font-medium mb-2">
                Email
                <div class="mt-1 relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                      <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                    </svg>
                  </div>
                  <input 
                    type="email" 
                    v-model="form.email"
                    class="w-full pl-10 pr-3 py-2 border border-gray-600 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 bg-gray-700 text-gray-100 placeholder-gray-400 sm:text-sm"
                    required
                    placeholder="your.email@example.com"
                  >
                </div>
              </label>
              <div v-if="errors.email" class="mt-1 text-sm text-red-400 bg-red-900 border border-red-700 rounded-md p-2">
                {{ errors.email }}
              </div>
            </div>

            <!-- Subject Field -->
            <div class="mb-4">
              <label class="block text-gray-200 font-medium mb-2">
                Subject
                <div class="mt-1">
                  <input 
                    type="text" 
                    v-model="form.subject"
                    class="w-full px-3 py-2 border border-gray-600 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 bg-gray-700 text-gray-100 placeholder-gray-400 sm:text-sm"
                    required
                    placeholder="What's your message about?"
                  >
                </div>
              </label>
              <div v-if="errors.subject" class="mt-1 text-sm text-red-400 bg-red-900 border border-red-700 rounded-md p-2">
                {{ errors.subject }}
              </div>
            </div>

            <!-- Message Field -->
            <div class="mb-4">
              <label class="block text-gray-200 font-medium mb-2">
                Message
                <div class="mt-1">
                  <textarea 
                    v-model="form.message"
                    rows="4" 
                    class="w-full px-3 py-2 border border-gray-600 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 bg-gray-700 text-gray-100 placeholder-gray-400 sm:text-sm"
                    required
                    placeholder="Your message"
                  ></textarea>
                </div>
              </label>
              <div v-if="errors.message" class="mt-1 text-sm text-red-400 bg-red-900 border border-red-700 rounded-md p-2">
                {{ errors.message }}
              </div>
            </div>

            <!-- Human Confirmation -->
            <div class="mb-4">
              <label class="block text-gray-200 font-medium mb-2">
                <span class="text-base">Please confirm you're human</span>
                <div class="mt-1">
                  <input 
                    type="checkbox" 
                    v-model="form.confirmHuman"
                    class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-600 bg-gray-700 rounded"
                    required
                  >
                </div>
              </label>
              <div v-if="errors.confirmHuman" class="mt-1 text-sm text-red-400 bg-red-900 border border-red-700 rounded-md p-2">
                {{ errors.confirmHuman }}
              </div>
            </div>
          
            <div class="mt-6">
              <button 
                type="submit" 
                :disabled="isSubmitting"
                class="w-full md:w-auto inline-flex justify-center items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-indigo-500 transition-colors duration-200 disabled:opacity-50"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
                </svg>
                {{ isSubmitting ? 'Sending...' : 'Send Message' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    
      <div class="mt-12 grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="bg-gray-800 p-6 rounded-lg shadow-md border border-gray-700">
          <h2 class="text-xl font-semibold text-white mb-3">Contact Information</h2>
          <div class="space-y-3 text-gray-300">
            <p class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3 text-indigo-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M2.94 6.412A2 2 0 002 8.108V16a2 2 0 002 2h12a2 2 0 002-2V8.108a2 2 0 00-.94-1.696l-6-3.75a2 2 0 00-2.12 0l-6 3.75zm2.615 2.423a1 1 0 10-1.11 1.664l5 3.333a1 1 0 001.11 0l5-3.333a1 1 0 00-1.11-1.664L10 11.798 5.555 8.835z" clip-rule="evenodd" />
              </svg>
              support@imageassistant.io
            </p>
          </div>
        </div>
        
        <div class="bg-gray-800 p-6 rounded-lg shadow-md border border-gray-700">
          <h2 class="text-xl font-semibold text-white mb-3">Support Hours</h2>
          <div class="space-y-3 text-gray-300">
            <p class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3 text-indigo-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
              </svg>
              Monday-Friday: 9:00 AM - 5:00 PM
            </p>
            <p class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3 text-indigo-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
              </svg>
              We'll respond to your message within 24 hours during business days.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { API_URL } from '../config.js';
export default {
  name: 'ContactPage',
  data() {
    return {
      form: {
        name: '',
        email: '',
        subject: '',
        message: '',
        confirmHuman: false
      },
      errors: {},
      showSuccess: false,
      isSubmitting: false,
    }
  },
  methods: {
    async submitForm() {
      this.errors = {}
      this.isSubmitting = true

      // Basic validation
      if (!this.form.name.trim()) {
        this.errors.name = 'Name is required'
      }
      if (!this.form.email.trim()) {
        this.errors.email = 'Email is required'
      }
      if (!this.form.subject.trim()) {
        this.errors.subject = 'Subject is required'
      }
      if (!this.form.message.trim()) {
        this.errors.message = 'Message is required'
      }
      if (!this.form.confirmHuman) {
        this.errors.confirmHuman = 'Please confirm you are human'
      }

      // If there are validation errors, stop submission
      if (Object.keys(this.errors).length > 0) {
        this.isSubmitting = false
        return
      }

      try {
        // Make API call to Django backend
        const response = await fetch(`${API_URL}/api/v1/contact/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.form)
        })

        const data = await response.json()

        if (response.ok) {
          // Show success message
          this.showSuccess = true
          
          // Reset form
          this.form = {
            name: '',
            email: '',
            subject: '',
            message: '',
            confirmHuman: false
          }

          // Hide success message after 5 seconds
          setTimeout(() => {
            this.showSuccess = false
          }, 5000)
        } else {
          // Handle validation errors from API
          if (data.name) this.errors.name = Array.isArray(data.name) ? data.name[0] : data.name
          if (data.email) this.errors.email = Array.isArray(data.email) ? data.email[0] : data.email
          if (data.subject) this.errors.subject = Array.isArray(data.subject) ? data.subject[0] : data.subject
          if (data.message) this.errors.message = Array.isArray(data.message) ? data.message[0] : data.message
          if (data.confirmHuman) this.errors.confirmHuman = Array.isArray(data.confirmHuman) ? data.confirmHuman[0] : data.confirmHuman
        }

      } catch (error) {
        console.error('Error submitting form:', error)
        this.errors.general = 'An error occurred while sending your message. Please try again.'
      } finally {
        this.isSubmitting = false
      }
    }
  }
}
</script>