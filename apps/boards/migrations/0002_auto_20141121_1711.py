# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='thread',
            options={'ordering': ['-is_pinned', '-updated'], 'verbose_name': 'Thread', 'verbose_name_plural': 'Threads', 'permissions': [('can_pin', 'Can pin threads.'), ('can_lock', 'Can lock threads.')]},
        ),
        migrations.AddField(
            model_name='board',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='board',
            name='group_post',
            field=models.ForeignKey(null=True, blank=True, to='auth.Group', help_text='Required group to post in this board.', related_name='boards_write+'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='board',
            name='group_view',
            field=models.ForeignKey(null=True, blank=True, to='auth.Group', help_text='Required group to see this board.', related_name='boards_read+'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thread',
            name='is_locked',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='thread',
            name='is_pinned',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
