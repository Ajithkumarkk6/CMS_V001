from django.contrib.auth.models import User
from authentication.models import UserAuthentication
from rest_framework.authtoken.models import Token
from .models import *
from authentication.model_helper import create_update_model


def get_tickets():
    return Ticket.objects.filter()


def get_ticket_tags():
    return TicketTag.objects.filter()


def get_ticket_events(ticket_id):
    return TicketChannelEvent.objects.filter(ticket_id=ticket_id).order_by('-created_at')
