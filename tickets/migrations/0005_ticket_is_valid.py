# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-18 00:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_auto_20160817_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='is_valid',
            field=models.BooleanField(default=True),
        ),
    ]
