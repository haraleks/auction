from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .user_models import UserProfile

User = get_user_model()


class Auction(models.Model):
    name = models.CharField(
        'Название аукциона',
        blank=False,
        null=False,
        max_length=200
    )
    description = models.CharField(
        'Описание аукциона',
        blank=False,
        null=False,
        max_length=500
    )
    date_start = models.DateTimeField(
        'Дата начала аукциона',
        blank=True,
        null=True
    )
    date_end = models.DateTimeField(
        'Дата завершения аукциона',
        blank=True,
        null=True
    )
    rate_start = models.IntegerField(
        'Начальная ставка',
        default=0
    )
    is_active = models.BooleanField(
        'Активный аукцион',
        default=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_now=True)
    deleted_at = models.DateTimeField('Удален', null=True, default=None, blank=True)

    class Meta:
        verbose_name = 'Аукцион'
        verbose_name_plural = 'Аукционы'
        default_permissions = []

    def check_finish(self):
        """Check finished auction"""
        date_now = timezone.now()
        if self.date_end is None:
            return self.is_active
        if self.date_end <= date_now:
            self.is_active = False
            self.save()
        return self.is_active


class RateMember(models.Model):
    """Rate mamber"""
    member = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        related_query_name='rate_member',
        related_name='rate_member',
        null=True,
        blank=True
    )
    rate = models.IntegerField(
        'Cтавка участника',
        default=0
    )

    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_now=True)
    deleted_at = models.DateTimeField('Удален', null=True, default=None, blank=True)

    class Meta:
        verbose_name = 'Ставка'
        verbose_name_plural = 'Ставки'
        default_permissions = []
