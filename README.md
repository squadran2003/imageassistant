# AI Image Manipulation App

## Overview

This web application allows users to perform various image manipulation tasks, creating images from prompts, removing backgrounds, enhancing images and many more. The application features a modern architecture with a Django REST API backend and Vue.js frontend.

## Architecture

### Backend (Django)
- **Framework**: Django 4.2+ with Django REST Framework
- **Database**: PostgreSQL with custom user model
- **Authentication**: JWT tokens with Google OAuth integration
- **Task Queue**: Celery with Redis broker
- **Cloud Services**: AWS S3 for storage, AWS Lambda for processing
- **Payment Processing**: Stripe integration
- **Security**: CORS configuration, honeypot protection, feature flags

### Frontend (Vue.js)
- **Framework**: Vue 3 with Vue Router
- **Styling**: Tailwind CSS
- **Development Server**: Runs on port 5000
- **API Communication**: RESTful API calls to Django backend
- **Authentication**: JWT token-based with automatic refresh

### Infrastructure
- **Containerization**: Docker with Docker Compose
- **Message Broker**: Redis for Celery task queue
- **File Storage**: AWS S3 for production, local filesystem for development
- **Deployment**: Docker containers with separate services

## Features

### Core Functionality
- **AI Image Generation**: Create images from text prompts using Stability AI
- **Image Processing**: 
  - Remove Background
  - Grayscale conversion
  - Image resizing
  - Image enhancement
  - Thumbnail generation
  - Image cropping
  - Avatar creation
- **Asynchronous Processing**: Background task processing with Celery
- **Credit System**: Token-based pricing (1$ = 50 credits)

### User Management
- **Authentication**: Email-based with Google OAuth support
- **User Accounts**: Custom user model with profile management
- **Credit System**: Integrated billing with Stripe
- **Feature Flags**: Dynamic feature toggles per user
- **Security**: Account banning system, honeypot protection

### Technical Features
- **Real-time Processing**: Status polling for long-running tasks
- **Cloud Integration**: AWS S3 storage with Lambda processing
- **Responsive Design**: Mobile-friendly interface
- **API-First**: RESTful API design with comprehensive endpoints

## Getting Started

### Prerequisites

To run this application, you only need to have **Docker** and **Docker Compose** installed on your machine.

### Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/image-manipulation-app.git
    cd image-manipulation-app
    ```

2. **Create a `.env` file in /imageassistant/**:

    Copy the `.env.example` file to `.env` and fill in your environment-specific configurations. 

    **Required Environment Variables:**
    ```env
    # Django Configuration
    SECRET_KEY=your-secure-secret-key-here
    ALLOWED_HOSTS=127.0.0.1,localhost
    DJANGO_SETTINGS_MODULE=config.settings
    
    # Database Configuration
    DB_NAME=your_database_name
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_HOST=172.17.0.1
    
    # Redis Configuration
    REDIS_URL=redis://redis-imageassistant:6379/1
    CELERY_BROKER_URL=redis://redis-imageassistant:6379/0
    CELERY_RESULT_BACKEND=redis://redis-imageassistant:6379/0
    
    # External Services (Optional - for production features)
    STRIPE_SECRET_KEY=your_stripe_secret_key
    STRIPE_PRICE_ID=your_stripe_price_id
    STABILITY_AI_KEY=your_stability_ai_key
    GOOGLE_CLIENT_ID=your_google_client_id
    
    # Email Configuration (Optional)
    MAILERSEND_SMTP_HOST=smtp.mailersend.net
    MAILERSEND_SMTP_PORT=587
    MAILERSEND_SMTP_USERNAME=your_smtp_username
    MAILERSEND_SMTP_PASSWORD=your_smtp_password
    DEFAULT_FROM_EMAIL=noreply@yourdomain.com
    
    # AWS Configuration (Production only)
    AWS_STORAGE_BUCKET_NAME=your_s3_bucket_name
    CLOUDFRONT_DOMAIN=your_cloudfront_domain
    ```
    
    **Security Note**: Never commit the `.env` file to version control. Ensure all sensitive keys are kept secure.

3. **Build and start the application**:

    ```bash
    docker-compose up --build
    ```

    This command will build the Docker images and start the following services:
    - **Django Backend**: API server on port 8084
    - **Vue.js Frontend**: Development server on port 5000
    - **PostgreSQL**: Database server
    - **Redis**: Message broker for Celery
    - **Celery Worker**: Background task processing

4. **Access the application**:
   - **Frontend (Vue.js)**: `http://localhost:5000`
   - **Backend API**: `http://localhost:8084`
   - **Django Admin**: `http://localhost:8084/admin`

## API Documentation

### Authentication Endpoints
- `POST /api/v1/custom/token/obtain/` - Login with email/password
- `POST /api/v1/google/login/` - Google OAuth login
- `POST /api/v1/users/signup/` - User registration
- `GET /api/v1/user/info/` - Get user profile and credits

### Image Processing Endpoints
- `POST /api/v1/create/image/from/prompt/` - Generate image from text prompt
- `GET /api/v1/image/status/<id>/` - Check image processing status
- `PUT /api/v1/update/processed/image/<id>/` - Update processed image

### Utility Endpoints
- `GET /api/v1/public/config/` - Get public configuration (Google Client ID, etc.)
- `POST /api/v1/users/change/password/` - Request password reset
- `POST /api/v1/users/password/reset/confirm/` - Confirm password reset

### Authentication
All protected endpoints require JWT token in Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Development Setup

### Frontend Development
```bash
cd imageassistant/frontend
npm install
npm run serve
```

### Backend Development
```bash
cd imageassistant
python manage.py runserver 8084
```

### Running Celery Worker
```bash
celery -A config worker --loglevel=info
```

## Vue.js Frontend Integration

### Build Process and Django Integration

The Vue.js frontend is configured to build and integrate seamlessly with Django for production deployment. This section documents the setup required to make Django serve the Vue.js Single Page Application (SPA).

#### Frontend Build Configuration

**1. Vue.js Build Setup (`imageassistant/frontend/vue.config.js`)**:
```javascript
const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  outputDir: 'dist',
  publicPath: '/static/',
  
  chainWebpack: config => {
    config
      .plugin('html')
      .tap(args => {
        args[0].title = "ImageAssistant - AI Image Generation Tool | Create Stunning AI Art";
        return args;
      });
  }
})
```

**2. Tailwind CSS Configuration (`imageassistant/frontend/tailwind.config.js`)**:
```javascript
module.exports = {
  content: [
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "./public/index.html",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**3. PostCSS Configuration (`imageassistant/frontend/postcss.config.js`)**:
```javascript
module.exports = {
  plugins: {
    'tailwindcss': {},
    'autoprefixer': {}
  }
}
```

**4. Build Script (`imageassistant/frontend/build-script.js`)**:
The build process includes a post-build script that moves files to Django's expected locations:
- `index.html` → `../templates/index.html` (Django template)
- Static assets → `../assets/` (Django static files)

```javascript
// Post-build script moves built files to Django structure:
// - CSS files to assets/css/
// - JS files to assets/js/
// - Images and other assets to assets/
```

#### Build Commands

**Development Build**:
```bash
cd imageassistant/frontend
npm run serve    # Development server with hot reload
```

**Production Build**:
```bash
cd imageassistant/frontend
npm run build    # Builds and moves files to Django structure
```

The build process:
1. Builds Vue.js application to `dist/` directory
2. Moves `index.html` to Django's `templates/` directory  
3. Moves all static assets to Django's `assets/` directory
4. Django's `collectstatic` command picks up these assets

### SPA Routing Configuration

#### The Problem
Single Page Applications (SPAs) handle routing client-side, but when users refresh the browser or access URLs directly, the server needs to know how to handle these routes. Without proper configuration, Django returns 404 errors for Vue.js routes like `/users/login` or `/images/create`.

#### The Solution
Configure Django with a catch-all URL pattern that serves the Vue.js `index.html` for any frontend route while preserving API and admin functionality.

**Django URL Configuration (`config/urls.py`)**:
```python
from django.urls import path, include, re_path
from config.views import base

urlpatterns = [
    path('', base, name='base'),
    path('admin/', admin.site.urls),
    path('api/v1/', include(('api.urls', 'api'), namespace='api')),
    # ... other Django routes ...
    
    # Catch-all pattern for Vue.js SPA routes - MUST BE LAST
    re_path(r'^(?!api/|admin/|static/|media/|sitemap\.xml|robots\.txt|health/).*$', 
            base, name='spa_catchall'),
]
```

**Django View (`config/views.py`)**:
```python
def base(request):
    return render(request, 'index.html', {'index_page': True})
```

#### How It Works
1. **Specific Routes First**: Django processes API routes (`api/`), admin routes (`admin/`), static files (`static/`) normally
2. **Catch-All Pattern**: The regex `^(?!api/|admin/|static/|media/|sitemap\.xml|robots\.txt|health/).*$` matches any URL that doesn't start with excluded patterns
3. **Vue Router Takes Over**: Once `index.html` loads in the browser, Vue Router handles client-side routing

#### Benefits
- ✅ **Browser refresh works** on any Vue.js route (`/users/login`, `/images/create`, etc.)
- ✅ **Direct URL access works** (users can bookmark and share Vue.js routes)
- ✅ **API routes preserved** (`/api/v1/...` routes work normally)
- ✅ **Admin panel works** (`/admin/` routes work normally)
- ✅ **Static files served** (`/static/` routes work normally)

### API URL Configuration

The frontend automatically detects the correct API base URL:

**Runtime API Configuration (`frontend/src/config.js`)**:
```javascript
export const API_CONFIG = {
  getBaseUrl() {
    // Development: use environment variable if available
    if (process.env.NODE_ENV === 'development' && process.env.VUE_APP_API_URL) {
      return process.env.VUE_APP_API_URL;
    }
    
    // Production: use same origin as current page
    // Works when Django serves the Vue.js frontend
    return window.location.origin;
  }
};

export const API_URL = API_CONFIG.getBaseUrl();
```

This configuration ensures:
- **Development**: Uses `VUE_APP_API_URL` environment variable (e.g., `http://localhost:8084`)
- **Production**: Uses same origin as the current page (automatic)

## Production Deployment

### AWS Setup (Production)

1. **AWS S3**: 
   - Create an S3 bucket for image storage
   - Configure bucket policies for public read access
   - Set up CloudFront distribution for CDN

2. **AWS Lambda**:
   - Deploy image processing functions
   - Configure triggers from Django backend

3. **Environment Variables**:
   - Set production environment variables
   - Use AWS Secrets Manager for sensitive data

### Security Considerations
- All API endpoints use CSRF protection
- JWT tokens have configurable expiration
- Honeypot fields prevent automated signups
- Google OAuth integration for secure authentication
- Feature flag system for controlled rollouts
- Account banning system for abuse prevention

## Usage

### For End Users
1. **Registration**: Create account or login with Google
2. **Credits**: Each user receives 100 credits upon signup
3. **Image Generation**: Use text prompts to create AI images
4. **Image Processing**: Upload and process existing images
5. **Account Management**: View credits and manage profile

### For Developers
- RESTful API with comprehensive documentation
- JWT-based authentication
- Asynchronous task processing
- Feature flag system for A/B testing
- Comprehensive logging and error handling

## Troubleshooting

### Frontend Build Issues

**Problem**: Build fails with Tailwind CSS errors
```bash
ERROR: Loading PostCSS "@tailwindcss/postcss" plugin failed
```

**Solution**: Ensure you have the correct dependencies and configuration:
1. Check `package.json` has `tailwindcss`, `autoprefixer`, `postcss`
2. Verify `postcss.config.js` uses `'tailwindcss'` (not `'@tailwindcss/postcss'`)
3. Ensure `tailwind.config.js` has correct content paths

**Problem**: CSS styles don't work after build

**Solution**: 
1. Check that Tailwind CSS is properly configured with content paths
2. Verify the build script correctly moves CSS files to `assets/css/`
3. Ensure Django's `STATICFILES_DIRS` includes the `assets/` directory

### SPA Routing Issues

**Problem**: Browser refresh returns 404 on Vue.js routes

**Solution**: Ensure the catch-all URL pattern is configured correctly:
1. Add `re_path` import: `from django.urls import path, include, re_path`
2. Add catch-all pattern as the **last** URL pattern in `urlpatterns`
3. Ensure the regex excludes all Django routes (API, admin, static, media)

**Problem**: API calls fail with wrong URLs

**Solution**: Check the API configuration:
1. Verify `frontend/src/config.js` exists and exports `API_URL`
2. For development, set `VUE_APP_API_URL=http://localhost:8084` in `.env`
3. Ensure all Vue components import and use `API_URL` instead of `process.env.VUE_APP_API_URL`

### Docker and Development Issues

**Problem**: Frontend changes not reflecting in Django-served version

**Solution**:
1. Rebuild the frontend: `cd imageassistant/frontend && npm run build`
2. Restart Django server to pick up new template and static files
3. Clear browser cache (Ctrl+F5 or Cmd+Shift+R)

**Problem**: Static files not loading (CSS/JS 404 errors)

**Solution**:
1. Run Django's `collectstatic`: `python manage.py collectstatic --noinput`
2. Check that `STATICFILES_DIRS` includes the correct paths
3. Verify the Vue.js build script moved files to the correct locations

### Common Configuration Mistakes

1. **Wrong publicPath**: Vue.js `publicPath` should be `/static/` to match Django's `STATIC_URL`
2. **Missing catch-all pattern**: Django URLs must include the SPA catch-all pattern as the last entry
3. **Incorrect API URL**: Frontend should use runtime detection, not build-time environment variables
4. **File permissions**: Ensure Django can read the built template and static files

### Debugging Tips

1. **Check build output**: Verify files are created in correct locations after `npm run build`
2. **Django debug**: Set `DEBUG = True` to see detailed error messages
3. **Network tab**: Use browser developer tools to check failed API calls or static file requests
4. **Django logs**: Check Django console output for URL routing issues

## Contributing

Contributions are welcome! If you have suggestions or improvements, please feel free to submit a pull request or open an issue.

## License

This software is proprietary and confidential


