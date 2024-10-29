from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from . import forms


def login_view(request):
    form = forms.LoginForm(request.session.get('data_form'))
    if 'data_form' in request.session:
        del(request.session['data_form'])
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        request.session['data_form'] = request.POST
        if form.is_valid():
            user = authenticate(
                request, 
                username=form.cleaned_data['username'], 
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                if (not User.objects.filter(username=form.cleaned_data['username']).exists()):
                    form.add_error('username', 'Usuário não encontrado !')
                else: 
                    form.add_error('password', 'Senha incorreta !')
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