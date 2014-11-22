# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0006_auto_20141122_1359'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='content',
            new_name='contents',
        ),
        migrations.AlterField(
            model_name='thread',
            name='name',
            field=models.CharField(validators=[django.core.validators.MinLengthValidator(6)], max_length=70),
            preserve_default=True,
        ),
    ]
