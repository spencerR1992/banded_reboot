from __future__ import unicode_literals

from django.db import models
from users.models import EventUser
import uuid
# Create your models here.

def getRandString():
	return str(uuid.uuid4()).replace('-','')


class Event(models.Model):
	name = models.CharField(max_length = 500)
	user = models.ForeignKey(EventUser, on_delete=models.CASCADE)
	start_datetime = models.DateTimeField()
	end_datetime = models.DateTimeField()
	hash_code = models.CharField(max_length=40, default = getRandString, unique = True, null = True)
	
	class Meta:
		ordering = ['start_datetime']