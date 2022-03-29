from django.urls import path
from users.views import UserLoginView, UserLogoutView, UserRegistrationView, UserProfileView, verify
from django.contrib.auth.decorators import login_required

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    # path('profile/', profile, name='profile'),

    path('verify/<str:email>/<str:activate_key>/', verify, name='verify')
]