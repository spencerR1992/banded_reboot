from random import randint
from models import Ticket
import io
import pyqrcode

def createTixGroup(ticket_group):
	l = [randint(0, 999999999999999999) for x in range(ticket_group.count)]
	b = [Ticket(id = x, ticket_group = ticket_group, qr_code_svg=createTixSvg(x)) for x in l]
	Ticket.objects.bulk_create(b)

def createTixSvg(id):
	#todo make this 'something' not hardcoded
	buffer = io.BytesIO()
	pyqrcode.create("something" + str(id)).svg(buffer)
	return str(buffer.getvalue())