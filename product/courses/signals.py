from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import Subscription
from courses.models import Group


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.
    """
    if created:
        # Курс, на который подписался пользователь
        course = instance.course

        # Группа, которая связана с этим курсом
        group, _ = Group.objects.get_or_create(course=course)

        # Добавляем пользователя в группу
        group.participants.add(instance.user)

        # Сохраняем группу
        group.save()
