from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

# Create your models here.


'''
This is the user that creates events. 
The fields used from the User model will be email, password.  Login will be done with those. 
The EventUser will also be able to do things like customize the information about their events. 
'''
class EventUser(models.Model):
	user = models.OneToOneField(User)
	organization_name = models.CharField(max_length = 400, null=True)
