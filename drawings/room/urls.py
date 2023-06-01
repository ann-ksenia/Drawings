from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChooseRoom, name='ChooseRoom'),
    path('create-room/', views.CreateRoom, name = 'CreateRoom'),
    path('join-room/', views.JoinRoom, name = 'JoinRoom'),
    path('<str:room_name>/', views.ShowRoom, name = 'Room'),
]
