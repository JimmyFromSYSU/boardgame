from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


class CatanView(View):
    def get(self, request):
        return render(request, 'catan/catan.html', context={'title': 'Catan'})


class CatanRoomView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    # redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'catan/catan_room.html', context={'title': 'Catan Room'})
