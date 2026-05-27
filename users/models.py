import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


def avatar_upload_path(instance, filename):
    ext = filename.rsplit('.', 1)[-1]
    return f'avatars/avatar_{uuid.uuid4()}.{ext}'


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Навык')

    class Meta:
        ordering = ['name']
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('name', 'Admin')
        extra_fields.setdefault('surname', 'Admin')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
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
