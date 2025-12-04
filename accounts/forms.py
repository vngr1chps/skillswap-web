from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'telegram', 'skill_have',
                  'skill_need', 'bio', 'password1', 'password2')
        labels = {
            'username' : 'Никнейм',
            'email': 'Email',
            'telegram' : 'телеграмм тег',
            'skill_have': 'Ваши навыки',
            'skill_need' : 'Нужные вам навыки',
            'bio' : 'О себе',
            'password1' : 'Пароль',
            'password2' : 'Повторите пароль'
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'skill_have': forms.Textarea(attrs={'rows': 3}),
            'skill_need': forms.Textarea(attrs={'rows': 3}),
        }


class LoginForm(AuthenticationForm):
    pass