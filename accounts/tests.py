from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from .models import Usuario
from .manager import AccountsManager, ManagerErrors

class ManagerTestCase(TestCase):
    def setUp(self):
        self.userActive = Usuario.objects.create_user(username='test',
                                                password='testando',
                                                email='test@gmail.com',
                                                is_active=True,
                                                activation_key='key')
        self.client = Client()

        self.loginRight = {'username': 'test', 'password': 'testando'}
        self.loginWrong = {'username': 'wrong', 'password': 'wrongg'}

        self.registerRight = {'username': 'lol', 'password': 'loool', 'email':'lol@gmail.com'}
        self.registerWrong = {'username': 'test', 'password': 'testando', 'email':'test@gmail.com'}

    def test_view_login(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)

        response = self.client.post(reverse('login'), self.loginRight)
        self.assertEquals(response.status_code, 302)

        response = self.client.post(reverse('login'), self.loginWrong)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_view_register(self):
        response = self.client.get(reverse('register'))
        self.assertEquals(response.status_code, 200)

        response = self.client.post(reverse('register'), self.registerRight)
        self.assertEquals(response.status_code, 200)

        response = self.client.post(reverse('register'), self.registerWrong)
        self.assertTemplateUsed(response, 'accounts/register.html')
