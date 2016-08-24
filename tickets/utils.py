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
    # todo make this 'something' not hardcoded
    buffer = io.BytesIO()
    pyqrcode.create(settings.HOSTNAME + "t/" + str(id)).svg(buffer)
    return str(buffer.getvalue())


def createTixPng(id):
    try:
        myt = Ticket.objects.get(id=id)
        data = {}
        data = {'svg': myt.qr_code_svg.replace('\n', '')}
        headers = {'content-type': 'application/json'}
        url = settings.CONVERSION_ENDPOINT + 'svg-to-png'
        return requests.post(url, data=json.dumps(data), headers=headers)
    except Exception, e:
        raise str(e)


import requests

url = "http://localhost:8000/convert"

payload = "{\"svg\": \"<svg viewBox='0 0 105 93' xmlns='http://www.w3.org/2000/svg'><path d='M66,0h39v93zM38,0h-38v93zM52,35l25,58h-16l-8-18h-18z' fill='#ED1C24'/></svg>\"}"
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "e60fd999-3258-b10c-691c-8385acb2056c"
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)


def sendTicketEmail(subject, to):
    conn = boto.ses.connect_to_region(
        settings.REGION, aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    ticket = Ticket.objects.order_by('?').first()
    myString = render_to_string('ticket.html', {'ticket': ticket})
    conn.send_email(
        settings.SENDER_EMAIL, subject, myString, [to], format='html')
