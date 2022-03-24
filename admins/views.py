from django.shortcuts import render, HttpResponseRedirect

from django.contrib.auth.decorators import user_passes_test
from users.models import User
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm


@user_passes_test(lambda u: u.is_staff)
def index(request):
    context = {"title": 'GeekShop - Admin'}
    return render(request, 'admins/index.html', context)


class TitleMixin:
    title = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TitleMixin, self).get_context_data(object_list=None, **kwargs)
        context['title'] = self.title
        return context


class CommonMixin(TitleMixin, SuccessMessageMixin):
    pass


class UserAdminListView(CommonMixin, ListView):
    model = User
    template_name = 'admins/admin-users-read.html'
    title = 'GeekShop - Admin'

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserAdminListView, self).dispatch(request, *args, **kwargs)
    

class UserAdminCreateView(CommonMixin, CreateView):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegistrationForm
    success_url = reverse_lazy('admin_staff:admin_users')
    success_message = 'Пользователь успешно создан'


class UserAdminUpdateView(CommonMixin, UpdateView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admin_staff:admin_users')


@user_passes_test(lambda u: u.is_staff)
def admin_users_delete(request, pk):
    user = User.objects.get(id=pk)
    user.safe_delete()
    return HttpResponseRedirect(reverse('admin_staff:admin_users'))



# @user_passes_test(lambda u: u.is_staff)
# def admin_users(request):
#     users = User.objects.all()
#     context = {"title": 'GeekShop - Admin', 'users': users}
#     return render(request, 'admins/admin-users-read.html', context)


# @user_passes_test(lambda u: u.is_staff)
# def admin_users_create(request):
#     if request.method == 'POST':
#         form = UserAdminRegistrationForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_users'))
#     else:
#         form = UserAdminRegistrationForm()
#     context = {"title": 'GeekShop - Admin', 'form': form}
#     return render(request, 'admins/admin-users-create.html', context)
#
#
# @user_passes_test(lambda u: u.is_staff)
# def admin_users_update(request, pk):
#     selected_user = User.objects.get(id=pk)
#     if request.method == 'POST':
#         form = UserAdminProfileForm(instance=selected_user , data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_users'))
#     else:
#         form = UserAdminProfileForm(instance=selected_user)
#     context = {"title": 'GeekShop - Admin', 'form': form, 'selected_user': selected_user}
#     return render(request, 'admins/admin-users-update-delete.html', context)


