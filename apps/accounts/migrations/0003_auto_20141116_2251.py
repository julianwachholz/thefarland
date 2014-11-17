# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20141108_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_trusted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(unique=True, max_length=200, verbose_name='Minecraft username'),
            preserve_default=True,
        ),
    ]
