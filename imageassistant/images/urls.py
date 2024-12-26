
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from images import views


urlpatterns = [
    path('add', views.add_image, name='add'),
    path('get/<int:image_id>/', views.get_image, name='get_image'),
    path('resize/form/<int:image_id>/', views.resize_form_html, name='resize-form'),
    path('get/upload/form/', views.get_upload_form, name='get_upload_form'),
    path('crop/tool/<int:service_id>/<int:image_id>/', views.crop_tool_content, name='crop-tool'),
    path('processed/service/<int:image_id>/', views.processed_service, name='process_image'),
    path('services/buttons/<int:image_id>/', views.get_service_buttons, name='get_service_buttons'),
    path('service/<int:service_id>/<int:image_id>/', views.service, name='service'),
    path('checkout/<int:service_id>/<int:image_id>/', views.get_checkout_content, name='checkout'),
    path('create/checkout/session/<int:service_id>/<int:image_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('create/checkout/session/<int:service_id>/<int:image_id>/<str:prompt>/', views.create_checkout_session, name='create_checkout_session'),
    path('check/checkout/status/', views.session_status, name='stripe_session_status'),
    path('get/prompt/form/<int:service_id>/<int:image_id>/', views.get_prompt_form, name='get_prompt_form'),
]