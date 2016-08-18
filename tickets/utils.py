from random import randint
from models import Ticket


def createTixGroup(ticket_group):
	b = [Ticket(id = randint(0,999999999999999999), ticket_group = ticket_group) for x in range(ticket_group.count)]
	Ticket.objects.bulk_create(b)


