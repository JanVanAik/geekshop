from django.shortcuts import render


def index(request):
    context = {"title": 'GeekShop - Админ-панель'}
    return render(request, 'admins/index.html', context)