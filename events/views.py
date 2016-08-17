from django.shortcuts import render, redirect
from utils.datetimeUtils import localizeDatetime as lD
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from models import Event
from users.models import EventUser
# Create your views here.


@login_required
def eventConsole(request):
    return render(request, 'event_list.html', 
    	{"EventUser": EventUser.objects.get(user=request.user)})
    EventUser.objects.get(user=request.user)
# TODO finish this view.

#async. 
@login_required
def createEvent(request):
    try:
    	print request.POST
        myU = EventUser.objects.get(user=request.user)
        name = request.POST['name']
        date = request.POST['date']
        timezone = request.POST['timezone']
        start_datetime = lD(date, request.POST['start_time'], timezone)
        end_datetime = lD(date, request.POST['end_time'], timezone)
        Event(name=name, user=myU, start_datetime=start_datetime,
              end_datetime=end_datetime).save()
        return render(request, 'event_list.html', 
    		{"EventUser": EventUser.objects.get(user=request.user)})
    except Exception, e:
        return HttpResponseBadRequest(str(e), status=400)

#async, render event_console.html
@login_required
def deleteEvent(request, eventID):
    try:
        Event.objects.get(id=eventID).delete()
        return render(request, 'event_list.html', 
    		{"EventUser": EventUser.objects.get(user=request.user)})
    except Exception, e:
        return HttpResponseBadRequest(str(e), status=400)
