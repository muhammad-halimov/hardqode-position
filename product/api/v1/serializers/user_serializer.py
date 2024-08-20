import time
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers
from users.models import Subscription

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""
    is_active = serializers.SerializerMethodField()

    @staticmethod
    def get_is_active(obj):
        return obj.expired_at > timezone.now()

    class Meta:
        model = Subscription
        fields = (
            'user',
            'course',
            'is_active',
            'created_at',
            'expired_at'
        )
