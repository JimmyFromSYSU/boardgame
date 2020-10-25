from django.shortcuts import render
from django.views.generic import View

class CatanView(View):
    def get(self, request):
        return render(request, 'catan/catan.html', context={'title': 'Catan'})
