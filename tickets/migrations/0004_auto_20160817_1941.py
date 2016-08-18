# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-18 00:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_remove_ticketgroup_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='claimed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.TicketGroup'),
        ),
    ]
