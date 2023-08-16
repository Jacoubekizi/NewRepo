from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.Register.as_view(), name='sort'),
    path('update_information_student/<int:user_id>/', views.Update_Information_Student.as_view()),
    path('get_desires/', views.GetDesires.as_view()),
 ]