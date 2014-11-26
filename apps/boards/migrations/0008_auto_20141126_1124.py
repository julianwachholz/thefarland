# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boards', '0007_auto_20141122_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostHistory',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('reason', models.CharField(max_length=200, blank=True)),
                ('contents', models.TextField(help_text='Previous post contents.')),
                ('post', models.ForeignKey(to='boards.Post', related_name='history')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='edited_posts+')),
            ],
            options={
                'verbose_name': 'Post history',
                'verbose_name_plural': 'Post history',
                'ordering': ['created'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name_plural': 'Posts', 'ordering': ['created'], 'permissions': [('post_update', 'Can edit posts.'), ('post_delete', 'Can delete posts')], 'verbose_name': 'Post'},
        ),
        migrations.AlterModelOptions(
            name='thread',
            options={'verbose_name_plural': 'Threads', 'ordering': ['-is_pinned', '-updated'], 'permissions': [('thread_pin', 'Can pin threads.'), ('thread_lock', 'Can lock threads.')], 'verbose_name': 'Thread'},
        ),
    ]
