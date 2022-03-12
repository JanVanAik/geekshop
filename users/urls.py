from django.urls import path
from users.views import login, logout, profile, UserRegistrationView

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
]