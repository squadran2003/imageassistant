
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from images import views


urlpatterns = [
    path('add', views.add_image, name='add'),
    path('get/<int:image_id>/', views.get_image, name='get_image'),
    path('resize/form/<int:image_id>/', views.resize_form_html, name='resize-form-html'),
    path('get/upload/form/', views.get_upload_form, name='get_upload_form'),
    path('processed/service/<int:image_id>/', views.processed_service, name='process_image'),
    path('services/buttons/<int:image_id>/', views.get_service_buttons, name='get_service_buttons'),
    path('service/<int:service_id>/<int:image_id>/', views.service, name='service'),
]