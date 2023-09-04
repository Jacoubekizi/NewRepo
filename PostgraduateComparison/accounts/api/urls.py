from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/student/', views.StudentSignupView.as_view()),
    path('verify_email/', views.VerifyEamil.as_view(), name='email-verify'),
    path('login/', views.UserLoginApiView.as_view(), name='auth-login-token'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('change_password/<int:user_pk>/', views.Change_Password.as_view(), name='auth_change_password'),
    path('update_profile/<int:user_pk>/', views.UpdateUser.as_view(), name='auth_update_profile'),
    path('request-reset-email/', views.RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', views.PasswordTokenCheckAPI.as_view(), name='reset-password'),
    path('password-reset-complate/', views.SetNewPassword.as_view(), name='password-reset-complate'),
]