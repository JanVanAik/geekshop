from django.urls import path
from admins.views import index, UserAdminListView, UserAdminCreateView, UserAdminUpdateView, admin_users_delete

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UserAdminListView.as_view(), name='admin_users'),
    path('users-create/', UserAdminCreateView.as_view(), name='admin_users_create'),
    path('users-update/<int:pk>/', UserAdminUpdateView.as_view(), name='admin_users_update'),
    path('users-delete/<int:pk>/', admin_users_delete, name='admin_users_delete'),
]