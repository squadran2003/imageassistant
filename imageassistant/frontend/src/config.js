// Configuration for API endpoints
export const API_CONFIG = {
  getBaseUrl() {
    // For development, use environment variable if available
    if (process.env.NODE_ENV === 'development' && process.env.VUE_APP_API_URL) {
      return process.env.VUE_APP_API_URL;
    }
    
    // For production, use the same origin as the current page
    // This works when Django serves the Vue.js frontend
    return window.location.origin;
  }
};

export const API_URL = API_CONFIG.getBaseUrl();