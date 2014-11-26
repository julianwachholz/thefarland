# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0008_auto_20141126_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_modified',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
