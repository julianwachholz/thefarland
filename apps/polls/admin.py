from django.contrib import admin
from .models import Poll, Choice, Vote


class ChoiceInline(admin.TabularInline):
    model = Choice


class VoteInline(admin.TabularInline):
    model = Vote
    raw_id_fields = ['user']
    readonly_fields = ['choice']


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline, VoteInline]
