# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-19 01:04
from __future__ import unicode_literals

from django.db import migrations, models
import events.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20160818_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='hash_code',
            field=models.CharField(default=events.models.getRandString, max_length=40, null=True, unique=True),
        ),
    ]
