from django.shortcuts import render
from web.forms.accounts import RegisterModelForm


def register(request):
    form = RegisterModelForm()
    return render(request, 'web/register.html', {'form': form})

