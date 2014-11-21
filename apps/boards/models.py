from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from autoslug import AutoSlugField
from autoslug.settings import slugify


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

    class Meta:
        verbose_name = 'Board'
        verbose_name_plural = 'Boards'
        ordering = ['ordering']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('boards:detail', kwargs={'slug': self.slug})


def slash_slugify(value):
    slug_parts = []
    for part in value.split('/'):
        slug_parts.append(slugify(part))
    return '/'.join(slug_parts)


class Thread(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='get_slug', unique=True, slugify=slash_slugify)
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    board = models.ForeignKey(Board, related_name='threads')
    post_count = models.BigIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = 'Thread'
        verbose_name_plural = 'Threads'
        ordering = ['-is_pinned', '-updated']
        permissions = [
            ('can_pin', "Can pin threads."),
            ('can_lock', "Can lock threads."),
        ]

    def __str__(self):
        return self.name

    def get_slug(self):
        return '{}/{}'.format(self.board.slug, self.name)

    def get_absolute_url(self):
        return reverse('boards:thread', kwargs={'slug': self.slug})


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')
    thread = models.ForeignKey(Thread, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['created']

    def __str__(self):
        return 'Post in {thread_id} at {created}'.format(
            thread_id=self.thread_id,
            created=self.created
        )
