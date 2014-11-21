from django.db.models import F, Count
from django.utils import timezone


def thread_post_save(instance, **kwargs):
    from .models import Board
    thread_count = instance.board.threads.count()
    Board.objects.filter(pk=instance.board_id) \
         .update(thread_count=thread_count)


def post_post_save(instance, **kwargs):
    from .models import Board, Thread, Post
    thread = instance.thread
    thread_post_count = thread.posts.count()
    board_post_count = Post.objects.filter(thread__board=thread.board) \
                           .aggregate(num=Count('pk'))['num']
    Thread.objects.filter(pk=instance.thread_id) \
          .update(post_count=thread_post_count, updated=timezone.now())
    Board.objects.filter(pk=thread.board_id) \
         .update(post_count=board_post_count)


def thread_post_delete(instance, **kwargs):
    from .models import Board, Post
    thread_count = instance.board.threads.count()
    post_count = Post.objects.filter(thread__board=instance.board) \
                     .aggregate(num=Count('pk'))['num']
    Board.objects.filter(pk=instance.board_id)\
         .update(thread_count=thread_count,
                 post_count=post_count)
