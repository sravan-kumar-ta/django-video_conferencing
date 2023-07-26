from django.urls import path

from video_conference import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('meeting/', views.video_call, name='meeting'),
    path('join/', views.join_room, name='join_room'),
]
