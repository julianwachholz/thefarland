# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('ordering', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Choices',
                'ordering': ['ordering', 'name'],
                'verbose_name': 'Choice',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'Polls',
                'ordering': ['-created'],
                'verbose_name': 'Poll',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('choice', models.ForeignKey(to='polls.Choice', related_name='votes')),
                ('poll', models.ForeignKey(to='polls.Poll', related_name='votes')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='poll_votes+')),
            ],
            options={
                'verbose_name_plural': 'Votes',
                'verbose_name': 'Vote',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('poll', 'user')]),
        ),
        migrations.AddField(
            model_name='choice',
            name='poll',
            field=models.ForeignKey(to='polls.Poll', related_name='choices'),
            preserve_default=True,
        ),
    ]
