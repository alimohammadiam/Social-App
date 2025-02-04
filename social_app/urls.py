from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from .forms import LoginForm


app_name = 'social'


urlpatterns = [
    path('', views.profile, name='profile'),
    path('logout', views.log_out, name='logout'),
    path('login/', auth_view.LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('register/', views.register, name='register'),
    path('user/edit/', views.user_edit, name='user_edit'),

]
