from __future__ import unicode_literals

from django.db import models
from users.models import EventUser

# Create your models here.


class Event(models.Model):
	name = models.CharField(max_length = 500)
	user = models.ForeignKey(EventUser, on_delete=models.CASCADE)
	start_datetime = models.DateTimeField()
	end_datetime = models.DateTimeField()
	
	class Meta:
		ordering = ['start_datetime']