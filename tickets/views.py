from django.shortcuts import render
from models import TicketGroup, Ticket
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from events.models import Event
from utils import createTixGroup
# Create your views here.

@login_required
def createTix(request):
    try:
    	name = request.POST['name']
    	description = request.POST['description']
    	count = int(request.POST['count'])
    	event = Event.objects.get(id = request.POST['event_id'])
    	t = TicketGroup(name=name, count=count, description=description, event = event)
    	t.save()
    	createTixGroup(t)
    	return render(request, 'event_list_item.html', {'event': event})
    except Exception, e:
    	return HttpResponseBadRequest(str(e), status=400)

@login_required
def deleteTixGroup(request, ticketGroupID):
	try:
		t = TicketGroup.objects.get(id = ticketGroupID)
		e = t.event 
		t.delete()
		return render(request, 'event_list_item.html', {'event': e})
	except Exception, e:
		return HttpResponseBadRequest(str(e), status=400)



