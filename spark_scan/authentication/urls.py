from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    #Authentication URLs
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
     # Officer/Operator Registration URLs
    path('register/officer/', views.OfficerRegisterView.as_view(), name='register-officer'),
    path('register/operator/', views.OperatorRegisterView.as_view(), name='register-operator'),
    
    # Password Management URLs
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('new-password/', views.NewPasswordView.as_view(), name='new-password'),
]