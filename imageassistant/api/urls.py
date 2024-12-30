from rest_framework import routers
from django.urls import path, include
from .views import ImageListUpdate, TestServiceView


urlpatterns = [
    path('update/processed/image/<int:image_id>/', ImageListUpdate.as_view(), name='update-processed-image'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('test/service/', TestServiceView.as_view(), name='test-service')
]