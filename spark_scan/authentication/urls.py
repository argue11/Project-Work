from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('register/', views.RegisterView.as_view(), name='register'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    # path('new-password/', views.NewPasswordView.as_view(), name='new-password'),
    
    # # Generic OTP endpoints (can be used by any app)
    # path('send-otp/', views.SendOTPView.as_view(), name='send-otp'),
    # path('verify-otp/', views.VerifyOTPView.as_view(), name='verify-otp'),
]