from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    fieldsets = [
        (None, {'fields': ['username', 'password', 'is_verified', 'verification_code', 'is_trusted']}),
        ('Permissions', {'fields': ['groups', 'user_permissions', 'is_staff', 'is_superuser']}),
        ('Important dates', {'fields': ['last_login']}),
    ]
    list_display = ['username', 'is_verified', 'is_trusted', 'is_staff', 'last_login']
    list_filter = ['is_staff', 'is_superuser', 'is_verified', 'is_trusted', 'groups']
    search_fields = ['username', 'name']
    ordering = ['username']
    filter_horizontal = ['groups', 'user_permissions']
