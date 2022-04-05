from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.core.mail import send_mail

from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from baskets.models import Basket


class TitleMixin():
    title = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TitleMixin, self).get_context_data(object_list=None, **kwargs)
        context['title'] = self.title
        return context


class CommonMixin(TitleMixin):
    pass


class UserLoginView(CommonMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'GeekShop - Авторизация'

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse('products:index'))


class UserRegistrationView(CommonMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    title = 'GeekShop - Регистрация'
    register_form_class = UserRegistrationForm

    def send_verification(self, user):
        verify_link = reverse('users:verify', args=[user.email, user.activation_key])
        subject = f'Для подтверждения верификации пользователя {user.username} пройдите по ссылке'
        message = f' Для подтверждения верификации пользователя на портале {settings.DOMAIN_NAME} пройдите по ссылке ' \
                  f'пройдите по ссылке {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def post(self, request, *args, **kwargs):
        register_form = self.register_form_class(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            self.send_verification(user)
            return HttpResponseRedirect(reverse('users:login'))


class UserLogoutView(LogoutView):
    pass


class UserProfileView(CommonMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'GeekShop - Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context

# class UserProfileView(CommonMixin, UpdateView):
#     model = User
#     form_class = UserProfileForm
#     template_name = 'users/profile.html'
#     title = 'GeekShop - Личный кабинет'
#
#     def post(self, request, *args, **kwargs):
#         edit_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
#         profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
#         if edit_form.is_valid() and profile_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect('users:profile')
#
#     def get_success_url(self):
#         return reverse_lazy('users:profile', args=(self.object.id,))
#
#     def get_context_data(self, request, **kwargs):
#         edit_form = UserProfileForm(request.POST, request.FILES, instance = request.user)
#         profile_form =


def verify(request, email, activate_key):
    try:
        user = User.objects.get(email=email)
        if user and user.activation_key == activate_key and user.is_activation_key_expired:
            user.activation_key = ''
            user.activation_key_expires = None
            user.is_active = True
            user.save(update_fields=['activation_key', 'activation_key_expires', 'is_active'])
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse('products:index'))

    except Exception as e:
        pass

# @login_required()
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         form = UserProfileForm(instance=request.user)
#     context = {
#         'title': 'GeekShop - Профиль',
#         'form': form,
#         'baskets': Basket.objects.filter(user=request.user),
#     }
#     return render(request, 'users/profile.html', context)
#

