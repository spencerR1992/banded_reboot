# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-05 03:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bowling', '0002_game_players'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='current_bowler',
            field=models.CharField(max_length=200, null=True),
        ),
    ]