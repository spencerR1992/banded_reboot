from django.shortcuts import render
from models import TicketGroup, Ticket
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from events.models import Event
from utils import createTixGroup, createTixPng, sendTicketEmail
from django.conf import settings
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

#TODO add a max number of claimable tickets. 
def claimTix(request):
    try:
        tixGroup = int(request.POST['ticket_group_id'])
        numTix = int(request.POST['num_tix'])
        email = request.POST['email']
        tix = Ticket.objects.filter(ticket_group = tixGroup, claimed=False)
        if tix.count() < int(numTix):
            return render(request, "ticket_form_errors.html", {'error': "Not enough tickets are left :/"}, status=400)
        elif ((email =='') or (email == None)):
            return render(request, "ticket_form_errors.html", {'error': "please provide a valid email"}, status=400)
        else:
            tix = tix[:numTix]
            for ticket in tix:
                tixurl = settings.BUCKET_ENDPOINT + createTixPng(ticket)
                ticket.qr_code_url = tixurl
                ticket.claimed = False # TODO: change to true
                ticket.claimed_by = email
                ticket.save()
            sendTicketEmail("Your tickets to the show! change this eventually!", email, tix)
            return render(request, 'ticket_success.html', {'email': email})
    except Exception, e:
        print str(e)
        print 'damn'
        return 'damn'



