# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-18 00:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TicketTraunche',
            new_name='TicketGroup',
        ),
    ]
