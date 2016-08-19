from django.shortcuts import render
from django.template.context import RequestContext
from users.models import EventUser
import settings


'''
Holders for testing endpoints. This will eventually only be home to the '/' 
view.

'''


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', 
        	{"EventUser": EventUser.objects.get(user=request.user), "hostname":settings.HOSTNAME})
    else:
        return render(request, 'home.html')


def styleSheet(request):
    return render(request, 'style_sheet.html')
