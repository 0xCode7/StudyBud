from django.urls import path
from . import views

urlpatterns = [
    path('routes/', views.getRoutes, name='api-routes'),
    path('rooms/', views.getRooms, name='api-rooms'),
    path('rooms/<str:pk>/', views.getRoom, name='api-room'),

]