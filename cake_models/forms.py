from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import User, Profile

class RegistrationUserForm(UserCreationForm):
    phone = forms.CharField(
        required=True,
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control cake__textinput',
            'placeholder': 'Номер телефона'
        })
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control cake__textinput',
            'placeholder': 'Введите пароль'
        })
    )

    password2 = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control cake__textinput',
            'placeholder': 'Повторите пароль'
        })
    )

    class Meta:
        model = User
        fields = ('phone', 'password1', 'password2')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).exists():
            raise ValidationError("Пользователь с таким номером телефона уже существует.")
        return phone


class LoginUserForm(AuthenticationForm):
    phone = forms.CharField(
        required=True,
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control cake__textinput',
            'placeholder': 'Номер телефона'
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control cake__textinput',
            'placeholder': 'Введите пароль'
        })
    )

    class Meta:
        model = User
        fields = ('phone', 'password')


class ProfileUserForm(forms.ModelForm):
    name = forms.TextInput(attrs={
        'v-model': 'Name',
        'class': 'form-control my-2 cake__textinput'
    })
    email = forms.EmailInput(attrs={
        'v-model': 'Email',
        'class': 'form-control my-2 cake__textinput'
    })
    class Meta:
        model = Profile
        fields = ('name', 'email')