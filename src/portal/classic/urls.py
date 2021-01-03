from django.urls import path
from .views import *

urlpatterns = [
    path('minesweeper/', MinesweeperView.as_view(), name='minesweeper_game_url'),
    # path('room/<str:room_id>/', CatanRoomView.as_view(), name='catan_room_url')
    # path('room/', CatanRoomView.as_view(), name='catan_room_url')
]
