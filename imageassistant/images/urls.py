
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from images import views

app_name = 'images'

urlpatterns = [
    path('process/service/<int:service_id>/<int:image_id>/', views.process_service, name='process_service'),
    path('service/<int:service_id>/<int:image_id>/', views.service, name='service'),
    path('checkout/<int:service_id>/<int:image_id>/', views.build_checkout_session, name='build_checkout_session'),
    path('create/checkout/session/<int:service_id>/<int:image_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('create/checkout/session/<int:service_id>/<int:image_id>/<str:prompt>/', views.create_checkout_session, name='create_checkout_session'),
    path('check/checkout/status/', views.session_status, name='stripe_session_status'),
    path('generate/image/', views.generate_image, name='generate_image'),
    path('remove/image/background/', views.remove_image_background, name='remove_image_background'),
    path('create/image/outline/', views.create_image_outline, name='create_image_outline'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search, name='search'),
    path('pricing/', views.pricing, name='pricing'),
]