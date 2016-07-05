import re

from django import forms

from .models import Usuario


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) >= 4:
            return username
        else:
            raise forms.ValidationError('Precisa ter mais que 3 caracteres')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) >= 6:
            return password
        else:
            raise forms.ValidationError('Precisa ter mais que 5 caracteres')

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'email']
        help_texts = {
            'username': None
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) >= 4:
            return username
        else:
            raise forms.ValidationError('Precisa ter mais que 3 caracteres')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) >= 6:
            return password
        else:
            raise forms.ValidationError('Precisa ter mais que 5 caracteres')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        regex = re.compile('(.+?)[@](.+?)[.](.+?)')
        if regex.match(email):
            return email
        else:
            raise forms.ValidationError('Insira um email valido')            
