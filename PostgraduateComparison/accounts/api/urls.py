from django.urls import path
from . import views
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/student/', views.StudentSignupView.as_view()),
    path('login/', views.UserLoginApiView.as_view(), name='auth-token'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]