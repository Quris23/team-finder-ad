from django import forms
from django.contrib.auth import authenticate

from .models import User

ABOUT_TEXTAREA_ROWS = 4


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': ''}),
        label='Пароль',
    )

    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'password']
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'email': 'Email',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    def __init__(self, *args, **kwargs):
        self._user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            self._user_cache = authenticate(email=email, password=password)
            if self._user_cache is None:
                raise forms.ValidationError('Неверный email или пароль.')
        return cleaned_data

    def get_user(self):
        return self._user_cache


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'about', 'phone', 'github_url']
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'avatar': 'Аватар',
            'about': 'О себе',
            'phone': 'Телефон',
            'github_url': 'GitHub',
        }
        widgets = {
            'about': forms.Textarea(attrs={'rows': ABOUT_TEXTAREA_ROWS}),
        }
