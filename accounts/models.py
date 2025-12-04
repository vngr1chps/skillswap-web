from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(help_text='Ваш email', blank=False, unique=True)
    telegram = models.CharField(help_text='@Ваш тег', max_length=30, blank=False, unique=True)
    skill_have = models.CharField(help_text = 'Ваши навыки', max_length=200, blank=False)
    skill_need = models.CharField(help_text = 'Какие навыки вам интересны', max_length=200, blank=False)
    bio = models.TextField(help_text='о себе' , blank=True)

    def __str__(self):
        return self.username

