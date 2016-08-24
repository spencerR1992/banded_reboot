from random import randint
from models import Ticket
import io
import pyqrcode
from django.conf import settings
import boto.ses
from django.shortcuts import render, render_to_response
from django.template.loader import render_to_string
from django.conf import settings
import requests
import json


def createTixGroup(ticket_group):
    l = [randint(0, 999999999999999) for x in range(ticket_group.count)]
    b = [Ticket(id=x, ticket_group=ticket_group, qr_code_svg=createTixSvg(x))
         for x in l]
    Ticket.objects.bulk_create(b)


def createTixSvg(id):
    buffer = io.BytesIO()
    pyqrcode.create(settings.HOSTNAME + "t/" + str(id)).svg(buffer, scale=10)
    return str(buffer.getvalue())


def createTixPng(ticket):
    try:
        data = {'svg': ticket.qr_code_svg.replace('\n', '')}
        headers = {'content-type': 'application/json'}
        url = settings.CONVERSION_ENDPOINT + 'svg-to-png'
        myd =  json.loads(requests.post(url, data=json.dumps(data), headers=headers).text)
        return myd['url']
    except Exception, e:
        print 'error creating tix'
        raise Exception


def sendTicketEmail(subject, to, tickets):
    conn = boto.ses.connect_to_region(
        settings.REGION, aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    myString = render_to_string('ticket.html', {'tickets': tickets})
    conn.send_email(
        settings.SENDER_EMAIL, subject, myString, [to], format='html')
