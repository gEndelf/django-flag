# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FlaggedContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('status', models.PositiveSmallIntegerField(default=1, db_index=True)),
                ('count', models.PositiveIntegerField(default=0)),
                ('when_updated', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('creator', models.ForeignKey(related_name='flagged_content', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('moderator', models.ForeignKey(related_name='moderated_content', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='FlagInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('when_added', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(null=True, blank=True)),
                ('status', models.PositiveSmallIntegerField(default=1, db_index=True)),
                ('flagged_content', models.ForeignKey(related_name='flag_instances', to='flag.FlaggedContent')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-when_added',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='flaggedcontent',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
