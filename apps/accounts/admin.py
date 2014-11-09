from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    fieldsets = [
        (None, {'fields': ['username', 'password', 'is_verified', 'verification_code']}),
        ('Permissions', {'fields': ['is_staff', 'is_superuser', 'groups', 'user_permissions']}),
        ('Important dates', {'fields': ['last_login']}),
    ]
    list_display = ['username', 'is_verified', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'groups']
    search_fields = ['username', 'name']
    ordering = ['username']
    filter_horizontal = ['groups', 'user_permissions']
