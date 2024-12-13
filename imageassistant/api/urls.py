from rest_framework import routers
from django.urls import path, include
from .views import ImageListUpdate, test


urlpatterns = [
    path('update/processed/image/<int:image_id>/', ImageListUpdate.as_view(), name='update-processed-image'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]