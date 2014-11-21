# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('minecraft', '0003_auto_20141117_0226'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogAction',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('action', models.CharField(max_length=500)),
                ('arguments', models.TextField(blank=True)),
                ('webop', models.ForeignKey(to='minecraft.WebOperator', related_name='log')),
            ],
            options={
                'verbose_name': 'Log Action',
                'verbose_name_plural': 'Log Actions',
                'ordering': ['-timestamp'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='weboperator',
            name='gamemode',
            field=models.IntegerField(default=0, choices=[(0, 'Survival'), (1, 'Creative'), (2, 'Adventure'), (3, 'Spectator')]),
            preserve_default=True,
        ),
    ]
