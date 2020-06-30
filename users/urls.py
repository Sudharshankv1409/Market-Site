from django.urls import path
from . import views
app_name = 'users'

urlpatterns = [
    path('login/',views.LoginView.as_view(),name = 'login'),
    path('logout/',views.LogoutView.as_view(),name ='logout'),
    path('register/',views.RegisterView.as_view(),name ='register'),
    path('verify/', views.EmailVerifyView.as_view(), name='verify'),
    path('forgotpassword/',views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('changepassword/',views.ChangePasswordView.as_view(), name='change_password'),
]
