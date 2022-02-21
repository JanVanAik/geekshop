from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.contrib import messages
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'title': 'Geekshop - Авторизация', 'form': form}
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поздравляем, регистрация прошла успешно!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm
    context = {'title': 'Geekshop - Регистрация', 'form': form}
    return render(request, 'users/registration.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def profile(request):
    form = UserProfileForm(instance=request.user)
    context = {
        'title': 'GeekShop - Профиль',
        'form': form,
    }
    return render(request, 'users/profile.html', context)