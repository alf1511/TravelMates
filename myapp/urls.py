from django.urls import path
from django.contrib.auth import views as auth_view
from myapp.views import *
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', RegisterController.as_view(), name='register'),
    path('login', auth_view.LoginView.as_view(template_name='LoginUI.html', redirect_authenticated_user=True), name='login'),
    path('logout', auth_view.LogoutView.as_view(template_name='home.html'),name='logout'),
    path('addPost', CreatePostController.as_view(),name='addPost'),
    path('posts/<str:username>/', PostsController.as_view(),name='posts'),
    path('posts/<str:username>/<int:id>/', PostController.as_view(),name='post'),
    path('posts/<str:username>/<int:id>/update', PostUpdateController.as_view(),name='postUpdate'),
    path('posts/<str:username>/<int:id>/delete', PostDeleteController.as_view(),name='postDelete'),
]