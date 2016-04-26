from django.db import models
from django.contrib.auth.models import AbstractUser

def user_path(instance, filename):
    return ('media_profiles/{}/{}'.format(instance.username, filename))

class Usuario(AbstractUser):

    SEXO_CHOICES= (
                    ('M', 'Male'),
                    ('F', 'Female')
                    )

    activation_key = models.CharField(max_length=30)

    name = models.CharField(max_length=50, blank=True, default='unknown')
    gender = models.CharField(max_length=10, choices= SEXO_CHOICES, default='M')
    profile_image = models.ImageField(null=True, blank=True, upload_to=user_path)
