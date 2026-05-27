from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager
from .utils import avatar_upload_path

SKILL_NAME_MAX_LENGTH = 100
USER_NAME_MAX_LENGTH = 100
PHONE_MAX_LENGTH = 20


class Skill(models.Model):
    name = models.CharField(
        max_length=SKILL_NAME_MAX_LENGTH, unique=True, verbose_name='Навык'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=USER_NAME_MAX_LENGTH, verbose_name='Имя')
    surname = models.CharField(max_length=USER_NAME_MAX_LENGTH, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=PHONE_MAX_LENGTH, blank=True, verbose_name='Телефон')
    github_url = models.URLField(blank=True, verbose_name='GitHub')
    avatar = models.ImageField(
        upload_to=avatar_upload_path, blank=True, null=True, verbose_name='Аватар'
    )
    about = models.TextField(blank=True, verbose_name='О себе')
    skills = models.ManyToManyField(
        Skill, blank=True, related_name='users', verbose_name='Навыки'
    )
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.name} {self.surname}'
