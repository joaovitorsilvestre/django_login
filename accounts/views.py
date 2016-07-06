from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import LoginForm, RegisterForm
from .models import Usuario
from .manager import AccountsManager, ManagerErrors

def Login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        manager = AccountsManager(request)
        try:
            manager.do_login(username=username, password=password)
        except Exception as erro:
            return render(request, 'accounts/login.html', {'form': form, 'erro':erro})
        else:
            return HttpResponseRedirect('/home')

    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'form': form})

def Logout(request):
    manager = AccountsManager(request=request)
    manager.do_logout()
    return HttpResponseRedirect('/home')

def Register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')

        try:
            manager = AccountsManager(request)
            key = manager.do_registration(username=username, password=password, email=email)
        except Exception as erro:
            return render(request, 'accounts/register.html', {"erro":erro})
        else:
            return HttpResponse("conta criada com sucesso, key: {0} click <a href='/accounts/activate/{0}'>aqui</a> para ativar a conta".format(key))

    return render(request, 'accounts/register.html', {'form':form})

def Activate(request, key):
    try:
        manager = AccountsManager(request)
        manager.do_activation(key)
    except Exception as erro:
        return render(request, 'accounts/activate.html', {'erro':erro})
    else:
        return render(request, 'accounts/activate.html')
