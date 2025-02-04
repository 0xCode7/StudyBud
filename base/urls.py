from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('room/<str:id>/', views.room, name='room'),
    path('profile/<str:id>/', views.userProfile, name='profile'),
    path('update-user/', views.updateUser, name='update-user'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:id>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:id>/', views.deleteRoom, name='delete-room'),
    path('delete-message/<str:id>/', views.deleteMessage, name='delete-message'),
    path('create-topic/', views.createTopic, name='create-topic'),
    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activityPage, name='activity'),
]