# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-28 03:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20160818_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.CharField(max_length=400, null=True),
        ),
    ]
