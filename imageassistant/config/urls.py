"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from config.views import (
    base, StaticViewSitemap,
    health_check,
)
from django.contrib.sitemaps.views import sitemap
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', base, name='base'),
    path('admin/', admin.site.urls),
    path('api/v1/token/obtain/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include(('api.urls', 'api'), namespace='api')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    path('health/', health_check, name='health_check'),
    # Catch-all pattern for Vue.js SPA routes - must be last
    # This will catch any URL that doesn't match above patterns  
    re_path(r'^(?!api/|admin/?|static/|media/|sitemap\.xml|robots\.txt|health/).*$', base, name='spa_catchall'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
