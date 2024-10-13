from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views

# create your urls here.
urlpatterns = [
    path('', views.home, name='home'),
    # path('profile/<str:username>/', views.Profile, name='profile'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    
    # password change urls
	path('password-change/', PasswordChangeView.as_view(), name='password_change'),     
	path('password-change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='auth/password-change/password_change_done.html'), name='password_change_done'),
 
    # reset functionality
    # password reset url
 	path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password-reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password-reset/password_reset_complete.html'), name='password_reset_complete'),
    
    # robots.txt
    path('robots.txt', robots_txt, name='robots_txt'),

]