from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from login_django import settings

def Home(request):
    active = request.user.is_authenticated()

    if active == True:
        name_user = request.user.name
    else:
        name_user = 'lol'

    if active == True:
        return render(request, 'home/home.html', {'active':True, 'name_user': name_user})
    else:
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
                return render(request, 'home/home.html', {'fail':True, 'active':False, 'name_user': name_user})

    return render(request, 'home/home.html', {'active':active, 'name_user': name_user})
