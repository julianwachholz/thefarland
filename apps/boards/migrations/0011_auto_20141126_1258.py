# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0010_auto_20141126_1219'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='posthistory',
            options={'verbose_name_plural': 'Post history', 'verbose_name': 'Post history', 'permissions': [('view_history', 'View post history')], 'ordering': ['-created']},
        ),
        migrations.AlterField(
            model_name='posthistory',
            name='created',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
