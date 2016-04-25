from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from login_django import settings
from accounts.models import Usuario
from django.utils.crypto import get_random_string

def Login(request):
    next = request.GET.get('next', '/home/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password) # ele tenta autenticar o usuario, se não conseguir ele retorna None

        if user is not None:   # se o user NÃO retornar None então ele executa
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                return HttpResponse('Inactive user')
        else:
            return render(request, 'accounts/login.html', {'fail':True, 'redirect_to':next})

    return render(request, 'accounts/login.html', {'redirect_to':next})

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login')

def Register(request):
    next = request.GET.get('next', '/register/compĺete/')

    try:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            name = request.POST['name']

            user = Usuario.objects.create_user(username, email, password) # cria o usuario

            if user.is_active == True:                               # se o usuario ativar então ele já pode
                ## hora de salvar as fields customizadas, pos não podem ser adicionadas ao usuario durante a criação dele
                ## e para editar tem q fazer um rapido login e deslogar, para poder alterar o campo aqui ainda na criação
                user = authenticate(username=username, password=password)
                login(request, user)
                request.user.name = name
                request.user.is_active = False #faz o usuario novo ser inativo, somente após a verificação no email se tornara True
                request.user.activation_key = get_random_string(length=20)
                request.user.save()
                logout(request)

                return HttpResponseRedirect('/accounts/login')       # redirecionar para a tela de logi
    except:
        return render(request, 'accounts/register.html', {'fail':True})

    return render(request, 'accounts/register.html', {'redirect_to': next})

def Activate(request, key):
    user_key = Usuario.objects.get(activation_key=key) # aqui ele procura por alguma conta que tenha a key

    for item in Usuario.objects.all():      #
        if item.activation_key == key:
            item.is_active = True
            item.save()
            break

    return render(request, 'accounts/activate.html',{'user_key':user_key})
