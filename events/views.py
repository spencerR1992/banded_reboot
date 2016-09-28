from django.shortcuts import render, redirect
from utils.datetimeUtils import localizeDatetime as lD
from utils.validationUtils import check_fields
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from models import Event
from users.models import EventUser
from random import randint
from django.conf import settings
# Create your views here.


@login_required
def eventConsole(request):
    return render(request, 'event_list.html', 
    	{"EventUser": EventUser.objects.get(user=request.user), "hostname":settings.HOSTNAME})
    EventUser.objects.get(user=request.user)
# TODO finish this view.

#async. 
@login_required
def createEvent(request):
    try:
        needed = ['name', 'date', 'timezone', 'start_time', 'end_time', 'location']
        check_fields(needed, request.POST)
        myU = EventUser.objects.get(id = request.POST['event_user_id'])
        name = request.POST['name']
        date = request.POST['date']
        timezone = request.POST['timezone']
        start_datetime = lD(date, request.POST['start_time'], timezone)
        end_datetime = lD(date, request.POST['end_time'], timezone)
        location = request.POST['location']
        Event(name=name, user=myU, start_datetime=start_datetime,
              end_datetime=end_datetime).save()
        return render(request, 'event_list.html', 
    		{"EventUser": EventUser.objects.get(user=request.user)})
    except Exception, e:
        return render(request, 'event_form_errors.html',{"error": str(e)}, status = 400)

#async, render event_console.html
@login_required
def deleteEvent(request, eventID):
    try:
        Event.objects.get(id=eventID).delete()
        return render(request, 'event_list.html', 
    		{"EventUser": EventUser.objects.get(user=request.user)})
    except Exception, e:
        return HttpResponseBadRequest(str(e), status=400)

#TODO: return the number of tix.
def ticketClaim(request, hashCode):
    try:
        return render(request, 'event_ticket_claim.html', {"event": Event.objects.get(hash_code=hashCode)})
    except Exception, e:
        #TODO return an error specific page. 
        return HttpResponseBadRequest(str(e), status=400)
