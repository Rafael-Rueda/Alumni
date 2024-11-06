import re

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from apps.Authors.models import CustomUser

from . import forms


def login_view(request):
    form = forms.LoginForm(request.session.get('data_form'))
    
    if 'data_form' in request.session:
        del(request.session['data_form'])
    
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        request.session['data_form'] = request.POST

        if form.is_valid():
            login_input = form.cleaned_data['login']
            password = form.cleaned_data['password']

            # Check if the login input is an email
            if re.match(r"[^@]+@[^@]+\.[^@]+", login_input):
                # Try authenticating with email
                try:
                    username = CustomUser.objects.get(email=login_input).username
                    user = authenticate(request, username=username, password=password)
                except CustomUser.DoesNotExist:
                    user = None
            else:
                # If not an email, authenticate with username
                user = authenticate(request, username=login_input, password=password)

            if user is not None:
                login(request, user)
                return redirect('/posts')
            else:
                if not CustomUser.objects.filter(username=login_input).exists() and not CustomUser.objects.filter(email=login_input).exists():
                    form.add_error('login', 'Usuário ou e-mail não encontrado!')
                else:
                    form.add_error('password', 'Senha incorreta!')
                
                return render(request, 'authors/pages/login.html', {'form': form})
    
    return render(request, 'authors/pages/login.html', {'form': form})
def register_view(request):
    form = forms.RegisterForm(request.session.get('data_form'))
    if 'data_form' in request.session:
        del(request.session['data_form'])

    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        request.session['data_form'] = request.POST
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            del(request.session['data_form'])
            return redirect('authors:login')

    return render(request, 'authors/pages/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('authors:login')