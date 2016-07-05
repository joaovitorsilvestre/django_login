from django.db import models
from django.contrib.auth.models import AbstractUser

def user_path(instance, filename):
    return ('image_profile_users/{}/{}'.format(instance.username, filename))

class Usuario(AbstractUser):
    activation_key = models.CharField(max_length=30)
