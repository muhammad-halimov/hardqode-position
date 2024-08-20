from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver

def validate_non_negative(value):
    if value < 0:
        raise ValueError(_('Баланс не может быть отрицательным.'))


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)

    DisplayFields = ["id", "username", "email", "created", "updated"]
    SearchableFields = DisplayFields
    FilterFields = ["created", "updated"]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    balance = models.DecimalField(
        max_digits=250, decimal_places=2, default=1000,
        validators=[validate_non_negative],
        null=True, blank=True
    )

    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)

    DisplayFields = ["id", "user", "balance", "created", "updated"]
    SearchableFields = DisplayFields
    FilterFields = ["created", "updated"]

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=CustomUser)
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        Balance.objects.create(user=instance)


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь',
        null=True
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Курс',
        null=True
    )
    is_active = models.BooleanField(verbose_name='Активный ?', default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')
    expired_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата окончания подписки')

    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)

    DisplayFields = ["id", "user", "course", "is_active", "created_at", "expired_at", "created", "updated"]
    SearchableFields = DisplayFields
    FilterFields = ["created_at", "expired_at", "created", "updated"]

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.email} - {self.course.title}"
