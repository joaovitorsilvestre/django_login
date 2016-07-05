from django.contrib.auth import authenticate, login, logout
from django.utils.crypto import get_random_string

from .models import Usuario

class ManagerErrors(Exception):
    def __init__(self, error):
        self.error = error
    def __str__(self):
        return self.error

class AccountsManager(object):
    def __init__(self, request):
        self.request = request

    def do_login(self, username, password):
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                try:
                    login(self.request, user)
                except:
                    raise ManagerErrors('Erro interno')
            else:
                raise ManagerErrors('Usuario inativo')
        else:
            raise ManagerErrors('Alguns dados estão incorretos')

    def do_logout(self):
        logout(self.request)

    def do_registration(self, username, password, email):
        activation_key = get_random_string(length=20)
        new_user = Usuario.objects.create_user(username=username,
                                                email=email,
                                                password=password,
                                                is_active=False,
                                                activation_key=activation_key)

        return activation_key

    def do_activation(self, key):
        try:
            user = Usuario.objects.get(activation_key=key)
            user.is_active = True
            user.save()
        except:
            raise ManagerErrors('codigo de ativação incorreto')
