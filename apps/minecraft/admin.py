from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from .models import WebOperator, LogAction


class LogActionInline(admin.TabularInline):
    model = LogAction
    extra = 0


@admin.register(WebOperator)
class WebOperatorAdmin(admin.ModelAdmin):
    list_display = ['user', 'gamemode', 'get_coords']
    search_fields = ['user', 'user__username']
    ordering = ['user__username']
    inlines = [LogActionInline]


@admin.register(LogAction)
class LogActionAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'webop', 'action', 'arguments']
    search_fields = ['webop', 'action', 'arguments']
    date_hierarchy = 'timestamp'
