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
    path('ticket', views.ticket, name='ticket'),

    path('password-reset/', auth_view.PasswordResetView.as_view(success_url='done'), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(
        success_url='password-reset/complete/'), name='password_reset_confirm'),
    path('password-reset/complete/', auth_view.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('password-change/', auth_view.PasswordChangeView.as_view(success_url='done'), name='password_change'),
    path('password-change/done/', auth_view.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('posts/', views.post_list, name='post_list'),
    path('posts/post/<slug:tag_slug/>', views.post_list, name='post_list_by_tag'),
    path('posts/create-post', views.create_post, name='create_post'),


]
