from django.urls import path
from django.contrib.auth import views as auth_view
from myapp.views import RegisterController
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', RegisterController.as_view(), name='register'),
    path('login', auth_view.LoginView.as_view(template_name='LoginUI.html'), name='login'),
    path('logout', auth_view.LogoutView.as_view(template_name='home.html'), name='logout'),
]