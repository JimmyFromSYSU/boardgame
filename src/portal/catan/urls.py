from django.urls import path
from .views import *

urlpatterns = [
    path('', CatanView.as_view(), name='catan_game_url'),
    # path('room/<str:room_id>/', CatanRoomView.as_view(), name='catan_room_url')
    path('room/', CatanRoomView.as_view(), name='catan_room_url')
]
