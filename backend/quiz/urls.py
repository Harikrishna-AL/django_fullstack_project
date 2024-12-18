from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('room/<str:room_code>/', views.quiz_room, name='quiz_room'),  # Room page for the quiz
    path('login/', views.login_view, name='login_view'),
    path('room/', views.room, name='room'),
    path('api/login/', views.LoginView.as_view(), name='login_api'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/quiz-stats/<str:room_code>/', views.DashboardView.as_view(), name='quiz_stats'),

]