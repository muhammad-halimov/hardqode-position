from django.contrib import admin
from . import models


@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = models.CustomUser.DisplayFields
    search_fields = models.CustomUser.SearchableFields
    list_filter = models.CustomUser.FilterFields


@admin.register(models.Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = models.Balance.DisplayFields
    search_fields = models.Balance.SearchableFields
    list_filter = models.Balance.FilterFields


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = models.Subscription.DisplayFields
    search_fields = models.Subscription.SearchableFields
    list_filter = models.Subscription.FilterFields
