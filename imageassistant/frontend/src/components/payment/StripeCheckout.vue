<template>
  <div class="min-h-screen bg-gray-900 py-8 px-4">
    <div class="max-w-md mx-auto bg-gray-800 rounded-lg shadow-xl p-8">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-2xl font-bold text-white mb-2">Add Credits</h1>
        <p class="text-gray-400">Secure payment powered by Stripe</p>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="text-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500 mx-auto"></div>
        <p class="text-gray-300 mt-4">Loading payment system...</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="bg-red-900 border border-red-700 rounded-lg p-4 mb-6">
        <div class="flex items-center">
          <svg class="h-5 w-5 text-red-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <p class="text-red-200 font-medium">{{ error }}</p>
        </div>
      </div>

      <!-- Order Summary -->
      <div class="bg-gray-700 rounded-lg p-4 mb-6">
        <div v-if="paymentSuccessful" 
           class="bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg shadow-xl p-6 mb-6 animate-pulse">
          <div class="flex items-center">
            <svg class="h-10 w-10 text-white mr-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <div>
              <h2 class="text-xl font-bold text-white">Payment Successful!</h2>
              <p class="text-white opacity-90">Your credits have been added to your account.</p>
              <p class="text-white opacity-80 text-sm mt-2">Redirecting to homepage in a few seconds...</p>
            </div>
          </div>
        </div>
        <h3 class="text-lg font-semibold text-white mb-3">Credit Package</h3>
        <div class="space-y-2">
          <div class="flex justify-between items-center">
            <span class="text-gray-300">Credits:</span>
            <div class="flex items-center">
              <input 
                type="number" 
                v-model.number="selectedCredits" 
                class="bg-gray-700 border border-gray-600 rounded-md p-2 w-24 text-right text-white font-bold text-lg"
                min="500"
                max="10000"
                step="100"
                @input="updateAmount"
              />
              <div class="text-gray-400 text-sm ml-2">
                Minimum 500 credits
              </div>
              <div class="ml-2">
                <div class="text-green-400 text-sm">
                  {{ isBestValue ? 'Best Value!' : '' }}
                </div>
              </div>
            </div>
          </div>
          <div class="text-gray-400 text-sm mb-3">
            Use credits for AI image generation, background removal, and more
          </div>
          <div class="flex justify-between border-t border-gray-600 pt-2">
            <span class="text-gray-300 font-medium">Total:</span>
            <span class="text-white font-bold text-lg">${{ amount }}</span>
          </div>
        </div>
      </div>

      <!-- Payment Form -->
      <div v-if="STRIPE_PUBLIC_KEY">
        <form @submit.prevent="handleSubmit">
          <!-- Card Element Container -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-300 mb-2">
              Card Information
            </label>
            <div 
              id="card-element" 
              class="bg-gray-700 border border-gray-600 rounded-lg p-4 focus-within:border-indigo-500 transition-colors min-h-[50px]"
              style="min-height: 50px;"
            >
              <!-- Stripe Elements will mount here -->
            </div>
            <div v-if="!cardElementMounted && !isLoading" class="text-gray-400 text-xs mt-1">
              Initializing secure payment form...
            </div>
            <div v-if="cardError" class="text-red-400 text-sm mt-2">
              {{ cardError }}
            </div>
          </div>

          <!-- Submit Button -->
          <button 
            type="submit" 
            :disabled="isProcessingPayment || !cardComplete"
            class="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-medium py-3 px-4 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-800"
          >
            <div v-if="isProcessingPayment" class="flex items-center justify-center">
              <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Processing...
            </div>
            <div v-else class="flex items-center justify-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
              </svg>
              Pay ${{ amount || '0.00' }}
            </div>
          </button>
        </form>

        <!-- Security Notice -->
        <div class="mt-6 text-center">
          <div class="flex items-center justify-center text-gray-400 text-sm">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
            </svg>
            Secured by Stripe
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { API_URL } from '../../config.js';


export default {
  name: 'StripeCheckout',
  props: {
    user:{
      type: Object,
      required: true
    },
    onPaymentSuccess: {
      type: Function,
      default: () => {}
    },
    onPaymentError: {
      type: Function,
      default: () => {}
    },
    STRIPE_PUBLIC_KEY: {
      type: String,
      required: true
    },
    CREDIT_MULTIPLIER: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      stripePublishableKey: this.STRIPE_PUBLIC_KEY,
      cardElementMounted: false,
      cardError: null,
      isProcessingPayment: false,
      cardComplete: false,
      paymentSuccessful: false,
      selectedCredits: 500,
      amount: (500 / this.CREDIT_MULTIPLIER).toFixed(2)
    };
  },
  methods: {
    updateAmount() {
      this.amount = (this.selectedCredits / this.CREDIT_MULTIPLIER).toFixed(2);
    },
    async loadStripe() {
      try {
        if (window.Stripe) {
          this.initializeStripe();
          return;
            }

            // Create script element to load Stripe.js
            const script = document.createElement('script');
            script.src = "https://js.stripe.com/v3/";
            script.async = true;
            
            // Set up load event to initialize Stripe once script is loaded
            script.onload = () => {
              this.initializeStripe();
            };
            
            script.onerror = () => {
              this.error = "Failed to load Stripe. Please refresh the page or try again later.";
              this.isLoading = false;
            };
            
            // Add the script to the document
            document.head.appendChild(script);
          } catch (error) {
            console.error('Error loading Stripe:', error);
            this.error = "An error occurred while loading the payment system.";
            this.isLoading = false;
          }
      },
      initializeStripe() {
          try {
            // Initialize Stripe with your publishable key
            this.stripe = window.Stripe(this.STRIPE_PUBLIC_KEY);
            
            // Create Stripe Elements
            this.elements = this.stripe.elements({
              appearance: {
                theme: 'night',
                variables: {
                  colorPrimary: '#6366f1',
                  colorBackground: '#374151',
                  colorText: '#f9fafb',
                  colorDanger: '#ef4444',
                  fontFamily: 'system-ui, -apple-system, sans-serif',
                  borderRadius: '0.5rem'
                }
              }
            });
            
            // Create card element
            this.cardElement = this.elements.create('card', {
              hidePostalCode: true,
              style: {
                base: {
                  color: '#f3f4f6',
                  fontWeight: 400,
                  fontSize: '16px',
                  lineHeight: '1.5',
                  '::placeholder': {
                    color: '#9ca3af'
                  }
                },
                invalid: {
                  color: '#ef4444',
                  iconColor: '#ef4444'
                }
              }
            });
            
            // Mount the card element
            this.cardElement.mount('#card-element');
            
            // Add event listeners for card element
            this.cardElement.on('change', (event) => {
              this.cardElementMounted = true;
              this.cardComplete = event.complete;
              
              if (event.error) {
                this.cardError = event.error.message;
              } else {
                this.cardError = null;
              }
            });
            
            this.isLoading = false;
          } catch (error) {
            console.error('Error initializing Stripe:', error);
            this.error = "Failed to initialize the payment system. Please refresh and try again.";
            this.isLoading = false;
          }
    },
    async handleSubmit() {
          if (!this.cardComplete) {
            this.cardError = "Please complete your card information.";
            return;
          }
          
          this.isProcessingPayment = true;
          this.cardError = null;
          
          try {
            // Create payment intent on your server
            const response = await fetch(`${API_URL}/api/v1/stripe/payment/create-intent/`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.user.token}`
              },
              body: JSON.stringify({
                amount: this.amount
              })
            });
            
            const paymentData = await response.json();
            
            if (!response.ok) {
              throw new Error(paymentData.detail || 'Failed to create payment');
            }
            
            // Confirm the payment with Stripe
            const { paymentIntent, error } = await this.stripe.confirmCardPayment(
              paymentData.client_secret, 
              {
                payment_method: {
                  card: this.cardElement
                }
              }
            );
            
            if (error) {
              throw new Error(error.message);
            } else if (paymentIntent.status === 'succeeded') {
                  try {
                    // First, add credits to the user's account via API
                    const addCreditsResponse = await fetch(`${API_URL}/api/v1/users/add/credits/`, {
                      method: 'POST',
                      headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${this.user.token}`
                      },
                      body: JSON.stringify({
                        credits: this.selectedCredits
                      })
                    });
                    
                    if (!addCreditsResponse.ok) {
                      const errorData = await addCreditsResponse.json();
                      throw new Error(errorData.detail || 'Failed to add credits to your account');
                    }
                    
                    const creditData = await addCreditsResponse.json();
                    
                    // Then call the success callback with additional credit data
                    this.onPaymentSuccess({
                      id: paymentIntent.id,
                      amount: paymentIntent.amount / 100,
                      credits: this.selectedCredits,
                      transaction_id: creditData.transaction_id || null
                    });
                    this.paymentSuccessful = true;
                    setTimeout(() => {
                      // redirect to home
                      this.$router.push('/');
                    }, 5000);
                  } catch (error) {
                    console.error('Error adding credits:', error);
                    // The payment succeeded, but adding credits failed
                    this.cardError = "Payment was successful, but there was an issue adding credits to your account. Please contact support.";
                    this.onPaymentError(error);
                  }
            } else {
              throw new Error(`Payment status: ${paymentIntent.status}`);
            }
          } catch (error) {
            console.error('Payment error:', error);
            this.cardError = error.message || 'An error occurred during payment processing.';
            this.onPaymentError(error);
          } finally {
            this.isProcessingPayment = false;
          }
        },
  },
  mounted() {
    this.loadStripe();
  }
}
</script>