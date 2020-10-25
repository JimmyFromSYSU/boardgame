from django.urls import path
from .views import *

urlpatterns = [
    path('', CatanView.as_view(), name='catan_game_url')
]
