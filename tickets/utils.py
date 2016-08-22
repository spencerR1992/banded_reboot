from random import randint
from models import Ticket
import io
import pyqrcode
from django.conf import settings
import boto.ses
from django.shortcuts import render, render_to_response
from django.template.loader import render_to_string


def createTixGroup(ticket_group):
    l = [randint(0, 999999999999999) for x in range(ticket_group.count)]
    b = [Ticket(id=x, ticket_group=ticket_group, qr_code_svg=createTixSvg(x))
         for x in l]
    Ticket.objects.bulk_create(b)


def createTixSvg(id):
    # todo make this 'something' not hardcoded
    buffer = io.BytesIO()
    pyqrcode.create(settings.HOSTNAME + "t/" + str(id)).svg(buffer)
    return str(buffer.getvalue())


def sendTicketEmail(subject, to):
    conn = boto.ses.connect_to_region(
        settings.REGION, aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    ticket = Ticket.objects.order_by('?').first()
    myString = render_to_string('ticket.html', {'ticket': ticket})
    conn.send_email(settings.SENDER_EMAIL, subject, myString, [to], format='html')