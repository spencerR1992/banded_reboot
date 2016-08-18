from __future__ import unicode_literals

from django.db import models
from events.models import Event

# Create your models here.

class TicketGroup(models.Model):
	event = models.ForeignKey(Event, null = True)
	name = models.CharField(max_length = 500)
	count = models.IntegerField()
	description = models.TextField(null = True)

class Ticket(models.Model):
	ticket_group = models.ForeignKey(TicketGroup, null = True, on_delete=models.CASCADE)
	id = models.BigIntegerField(primary_key=True)
	check_in_time = models.DateTimeField(null = True)
	claimed = models.BooleanField(default = False)
	is_valid = models.BooleanField(default = True)
	claimed_by = models.EmailField(null = True)
	qr_code_svg = models.CharField(max_length = 4000, null = True)