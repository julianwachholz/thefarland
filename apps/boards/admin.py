from django.contrib import admin
from .models import Board, Thread, Post


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['name', 'thread_count', 'post_count']


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['name', 'board', 'created', 'updated', 'post_count']
    list_filter = ['board']
    date_hierarchy = 'created'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['created', 'user', 'thread']
    date_hierarchy = 'created'