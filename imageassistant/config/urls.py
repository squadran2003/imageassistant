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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.http import HttpResponse
from config.views import (
    base, faq, stripe_success_return, upload_content, StaticViewSitemap,
    contact, health_check, privacy_policy, terms_and_conditions
)
from django.contrib.sitemaps.views import sitemap


sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', base, name='base'),
    path('dashboard/', base, name='dashboard'),
    path('faq/', faq, name='faq'),
    path('admin/', admin.site.urls),
    path('contact/', contact, name='contact'),
    path('upload/content/', upload_content, name='upload_content'),
    path('images/', include(('images.urls', 'images'), namespace='images')),
    path('users/', include(('users.urls', 'users'), namespace='custom_users')),
    path('stripe/return/', stripe_success_return, name='stripe_success_return'),
    path('stripe/checkout/', stripe_success_return, name='stripe_checkout'),
    path('api/v1/', include(('api.urls', 'api'), namespace='api')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    path('health/', health_check, name='health_check'),
    path('privacy-policy/', privacy_policy, name='privacy-policy'),
    path('terms-conditions/', terms_and_conditions, name='terms-conditions'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
