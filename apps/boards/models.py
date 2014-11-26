import math
from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.functional import cached_property
from autoslug import AutoSlugField
from autoslug.settings import slugify
from .managers import BoardManager


class Board(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    description = models.TextField(blank=True)
    ordering = models.IntegerField(default=0)
    thread_count = models.BigIntegerField(default=0, editable=False)
    post_count = models.BigIntegerField(default=0, editable=False)

    group_view = models.ForeignKey('auth.Group', blank=True, null=True,
                                   related_name='boards_read+',
                                   help_text="See this board.")
    group_create = models.ForeignKey('auth.Group', blank=True, null=True,
                                     related_name='boards_create+',
                                     help_text="Create threads in this board.")
    group_post = models.ForeignKey('auth.Group', blank=True, null=True,
                                   related_name='boards_post+',
                                   help_text="Post replies in this board.")

    objects = BoardManager()

    class Meta:
        verbose_name = 'Board'
        verbose_name_plural = 'Boards'
        ordering = ['ordering']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('boards:thread_list', kwargs={'board': self.slug})

    def get_create_url(self):
        return reverse('boards:thread_create', kwargs={'board': self.slug})

    def can_create_thread(self, user):
        return user.is_superuser or \
            self.group_create is None or \
            user.groups.filter(id=self.group_create_id).exists()


def slash_slugify(value):
    slug_parts = []
    for part in value.split('/'):
        slug_parts.append(slugify(part))
    return '/'.join(slug_parts)


class Thread(models.Model):
    THREADS_PER_PAGE = 10

    name = models.CharField(max_length=70, validators=[MinLengthValidator(6)])
    slug = AutoSlugField(populate_from='get_slug', unique=True, slugify=slash_slugify)
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    board = models.ForeignKey(Board, related_name='threads')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='threads')
    post_count = models.BigIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = 'Thread'
        verbose_name_plural = 'Threads'
        ordering = ['-is_pinned', '-updated']
        permissions = [
            ('thread_pin', "Can pin threads."),
            ('thread_lock', "Can lock threads."),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('boards:post_list', kwargs={'thread': self.slug})

    def get_post_url(self):
        return reverse('boards:post_create', kwargs={'thread': self.slug})

    def get_latest_url(self):
        return reverse('boards:post_latest', kwargs={'thread': self.slug})

    def get_slug(self):
        return '{}/{}'.format(self.board.slug, self.name)

    def get_last_page(self):
        return math.ceil(self.post_count / Post.POSTS_PER_PAGE)

    def can_reply(self, user):
        return user.is_superuser or \
            not self.is_locked and \
            (self.board.group_post is None or
                user.groups.filter(id=self.board.group_post_id).exists())


class Post(models.Model):
    POSTS_PER_PAGE = 10

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')
    thread = models.ForeignKey(Thread, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_modified = models.BooleanField(default=False, editable=False)
    contents = models.TextField()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['created']
        permissions = [
            ('post_update', "Can edit posts."),
            ('post_delete', "Can delete posts"),
        ]

    def __str__(self):
        return 'Post in {thread_id} at {created}'.format(
            thread_id=self.thread_id,
            created=self.created
        )

    def get_absolute_url(self):
        # XXX Not really correct, but the only usecase works fine here.
        return reverse('boards:post_latest', kwargs={
            'thread': self.thread.slug,
            'post': self.id,
        })

    @cached_property
    def latest_history(self):
        return self.history.first()

    def can_update(self, user):
        return user.is_superuser or \
            self.user is user and not self.thread.is_locked or \
            user.has_perm('boards.post_update')


class PostHistory(models.Model):
    post = models.ForeignKey(Post, related_name='history')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='edited_posts+')
    created = models.DateTimeField()
    reason = models.CharField(max_length=200, blank=True)

    contents = models.TextField(help_text="Previous post contents.")

    class Meta:
        verbose_name = 'Post history'
        verbose_name_plural = 'Post history'
        ordering = ['-created']
        permissions = [
            ('view_history', "View post history"),
        ]

    def __str__(self):
        return 'PostHistory #{} at {}'.format(self.id, self.created)
