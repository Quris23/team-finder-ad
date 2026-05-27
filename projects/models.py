from django.conf import settings
from django.db import models

STATUS_OPEN = 'open'
STATUS_CLOSED = 'closed'
NAME_MAX_LENGTH = 200
STATUS_MAX_LENGTH = 10


class Project(models.Model):
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Открыт'),
        (STATUS_CLOSED, 'Закрыт'),
    ]

    name = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    status = models.CharField(
        max_length=STATUS_MAX_LENGTH,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
        verbose_name='Статус',
    )
    github_url = models.URLField(blank=True, verbose_name='GitHub репозиторий')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='Владелец',
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='participated_projects',
        verbose_name='Участники',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name
