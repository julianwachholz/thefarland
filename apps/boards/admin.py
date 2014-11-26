from django.contrib import admin
from .models import Board, Thread, Post, PostHistory


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['name', 'thread_count', 'post_count']
    readonly_fields = ['slug', 'thread_count', 'post_count']


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['name', 'board', 'is_pinned', 'is_locked', 'created', 'updated', 'post_count']
    list_filter = ['board', 'is_pinned', 'is_locked']
    date_hierarchy = 'created'
    readonly_fields = ['slug', 'post_count']
    raw_id_fields = ['user']


class PostHistoryInline(admin.TabularInline):
    model = PostHistory
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['created', 'user', 'thread']
    ordering = ['-created']
    date_hierarchy = 'created'
    readonly_fields = ['created', 'updated', 'is_modified']
    raw_id_fields = ['user', 'thread']

    inlines = [PostHistoryInline]
