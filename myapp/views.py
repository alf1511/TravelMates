from django.http import Http404
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import views as auth_view
from django.views import View

# Create your views here.
def index(request):
    context = {}
    return render(request, 'home.html', context)

class RegisterController(View):
    form_class = CreateUserForm
    initial = {'key': 'value'}
    template_name = 'RegisterUI.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        form = self.form_class(initial = self.initial)
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was successfully created')
            return redirect('index')
        return render(request, self.template_name, {'form':form})

class CreatePostController(View):
    form_class = CreatePostForm
    initial = {'key': 'value'}
    template_name = 'AddPostUI.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index')
        form = self.form_class(initial = self.initial)
        return render(request, self.template_name, {'form':form, 'test': len(kwargs)})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = User.objects.get(pk=request.user.id)
            obj.save()
            messages.success(request, f'Post was successfully added')
            return redirect('/posts/'+request.user.username)
        return render(request, self.template_name, {'form':form})

class PostsController(View):
    initial = {'key': 'value'}
    template_name = 'PostsUI.html'

    def get(self, request, *args, **kwargs):
        if kwargs['username'] != request.user.username:
            raise Http404
        data = Post.objects.filter(user = request.user.id)
        return render(request, self.template_name, {'data': data})

class PostController(View):
    initial = {'key': 'value'}
    template_name = 'PostUI.html'

    def get(self, request, *args, **kwargs):
        p = Post.objects.get(id=kwargs['id'])
        if str(kwargs['username']) != str(p.user):
            raise Http404
        return render(request, self.template_name, {'data': p})

class PostUpdateController(View):
    form_class = CreatePostForm
    initial = {'key': 'value'}
    template_name = 'AddPostUI.html'

    def get(self, request, *args, **kwargs):
        p = Post.objects.get(id=kwargs['id'])
        if str(kwargs['username']) != str(p.user):
            raise Http404
        form = CreatePostForm(instance=p)
        return render(request, self.template_name, {'form':form, 'test': len(kwargs)})

    def post(self, request, *args, **kwargs):
        p = Post.objects.get(id=kwargs['id'])
        form = self.form_class(request.POST, request.FILES, instance=p)
        if form.is_valid():
            form.save()
            messages.success(request, f'Post was successfully updated')
            return redirect('/posts/'+request.user.username)
        return render(request, self.template_name, {'form':form })

class PostDeleteController(View):
    initial = {'key': 'value'}
    template_name = 'PostsUI.html'

    def post(self, request, *args, **kwargs):
        p = Post.objects.get(id=kwargs['id'])
        if str(kwargs['username']) != str(p.user):
            raise Http404
        r = Post.objects.filter(id=kwargs['id'])
        r.delete()
        messages.success(request, f'Post was successfully deleted')
        return redirect('/posts/'+kwargs['username'])