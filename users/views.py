from django.shortcuts import render

from users.forms import UserLoginForm


def login(request):
    form = UserLoginForm()
    context = {'title': 'Geekshop - Авторизация', 'form': form}
    return render(request, 'users/login.html', context)


def registration(request):
    context = {'title': 'Geekshop - Регистрация'}
    return render(request, 'users/registration.html', context)
