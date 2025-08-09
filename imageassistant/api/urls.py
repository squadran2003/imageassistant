from rest_framework import routers
from django.urls import path, include
from .views import (
    AddCreditsView, CreateImageFromPromptView, CustomTokenObtainView, GoogleLoginView, ImageListUpdate, ImageStatusView, 
    PublicConfigView, SignUpView, UserInformationView,
    ChangePasswordView, PasswordRestConfirmView, RemoveBackgroundView, CreateGrayscaleView, CreateOutlineView,
    UserImagesView, ContactView,
    StripePaymentIntentView
)
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('update/processed/image/<int:image_id>/', ImageListUpdate.as_view(), name='update-processed-image'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('custom/token/obtain/', CustomTokenObtainView.as_view(), name='custom_token_obtain'),
    path('user/info/', UserInformationView.as_view(), name='user-information'),
    path('users/signup/', SignUpView.as_view(), name='signup'),
    path('users/change/password/', ChangePasswordView.as_view(), name='change-password'),
    path('users/password/reset/confirm/', PasswordRestConfirmView.as_view(), name='password-reset-confirm'),
    path('users/add/credits/', AddCreditsView.as_view(), name='add-credits'),
    path('google/login/', GoogleLoginView.as_view(), name='google-login'),
    path('public/config/', PublicConfigView.as_view(), name='public_config'),
    path('create/image/from/prompt/', CreateImageFromPromptView.as_view(), name='create-image-from-prompt'),
    path('image/status/<int:image_id>/', ImageStatusView.as_view(), name='image-status'),
    path('remove/background/', RemoveBackgroundView.as_view(), name='remove-background'),
    path('create/grayscale/', CreateGrayscaleView.as_view(), name='create-grayscale'),
    path('create/outline/', CreateOutlineView.as_view(), name='create-outline'),
    path('user/images/', UserImagesView.as_view(), name='user-images'),
    path('contact/', ContactView.as_view(), name='contact-api'),
    path('stripe/payment/create-intent/', StripePaymentIntentView.as_view(), name='stripe-payment-intent'),
]