from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import views as auth_view
from django.views import View

# Create your views here.
def index(request):
    context = {}
    return render(request, 'home.html', context)

# def register(request):
#     form = ''
#     if request.method == 'POST':
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Hi {username}, your account was successfully created')
#             return redirect('index')
#     else:
#         form = CreateUserForm()

#     context = {'form': form}
#     return render(request, 'RegisterUI.html', context)
class RegisterController(View):
    form_class = CreateUserForm
    initial = {'key': 'value'}
    template_name = 'RegisterUI.html'

    def get(self, request, *args, **kwargs):
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
