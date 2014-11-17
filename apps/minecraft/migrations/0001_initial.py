# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WebOperator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='op')),
            ],
            options={
                'verbose_name': 'Web Operator',
                'permissions': [('gamemode_spectator', 'User can change to spectator mode.'), ('player_kick', 'Can kick players.'), ('player_ban', 'Can ban players.'), ('player_banip', 'Can ban players by IP.')],
                'verbose_name_plural': 'Web Operators',
                'ordering': ['user'],
            },
            bases=(models.Model,),
        ),
    ]
