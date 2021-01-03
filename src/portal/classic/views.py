from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


# LoginRequiredMixin
class MinesweeperView(View):
    def get(self, request):

        return render(
            request,
            'classic/minesweeper.html',
            context={'title': 'Minesweeper'}
        )
