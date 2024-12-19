from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('room/<str:room_code>/', views.quiz_room, name='quiz_room'),  # Room page for the quiz
    path('login/', views.login, name='login'),
    path('room/', views.room, name='room'),
]