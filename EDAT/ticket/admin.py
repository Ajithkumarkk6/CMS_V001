from django.contrib import admin
from .models import TicketTag, TicketAttachment, Ticket, TicketAttachmentMessage, TicketChannelEvent

admin.site.register(TicketTag)
admin.site.register(TicketAttachment)
admin.site.register(Ticket)
admin.site.register(TicketAttachmentMessage)
admin.site.register(TicketChannelEvent)
