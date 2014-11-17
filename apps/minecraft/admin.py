from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from .models import WebOperator


@admin.register(WebOperator)
class WebOperatorAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user', 'user__username']
    ordering = ['user__username']
