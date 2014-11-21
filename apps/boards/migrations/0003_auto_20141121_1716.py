# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('boards', '0002_auto_20141121_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='group_create',
            field=models.ForeignKey(to='auth.Group', related_name='boards_create+', blank=True, null=True, help_text='Create threads in this board.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='board',
            name='group_post',
            field=models.ForeignKey(to='auth.Group', related_name='boards_post+', blank=True, null=True, help_text='Post replies in this board.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='board',
            name='group_view',
            field=models.ForeignKey(to='auth.Group', related_name='boards_read+', blank=True, null=True, help_text='See this board.'),
            preserve_default=True,
        ),
    ]
