
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from users import views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/<int:pk>/', views.DeleteUserView.as_view(), name='delete'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('change/password/', views.change_password, name='change-password'),
    path('reset/password/confirm/<str:uidb64>/<str:token>/', views.PasswordResetCustomConfirmView.as_view(), name='password-reset-confirm'),
    path('reset/complete/', views.PasswordResetCustomCompleteView.as_view(), name='password-reset-complete'),
    path('google/login/', views.google_login, name='google-login'),
]