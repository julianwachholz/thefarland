# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0005_thread_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='name',
            field=models.CharField(max_length=70),
            preserve_default=True,
        ),
    ]
