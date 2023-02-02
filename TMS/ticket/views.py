from django.shortcuts import render
from mmap import PAGESIZE
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from authentication.model_helper import create_update_model_response, create_update_model, check_if_exist, ValidateRequest, get_paginated_results_set, get_user_company_from_request
from authentication.response_serializer import get_validation_failure_response, get_success_response
from company.models import CompanyBranchInfo, CompanyBranchWeeklyCalendar, CompanyMeta, WeekDay
import random
from authentication.custom_api_views import GenericAPIView, GenericListAPIView, GenericCrudApiView
# get_paginated_results_set
from .models import Ticket, TicketAttachment, TicketAttachmentMessage, TicketChannelEvent, TicketTag
from authentication.model_helper import create_update_model
from .response_serializer import *
from .model_helper import *


class RaiseNewTicket(GenericCrudApiView):

    base_model = Ticket

    def proceed_post(self, request):

        data = request.data
        print("11111111111",data)
        ticketForm = data
        employee_company_info = self.get_employee_company_info()
        ticketForm['created_by_id'] = employee_company_info.id
        

        ticket_response = create_update_model(
            Ticket, ticketForm, api_instance=self)
        print("333333333333333333",ticketForm)
            

        if ticket_response['status'] == True:

            ticket_id = ticket_response['ids'][0]
            ticketChannelEventForm = {}
            ticketChannelEventForm['ticket_id'] = ticket_id
            ticketChannelEventForm['event_type'] = TicketChannelEvent.TICKET_STATUS
            ticketChannelEventForm['ticket_status'] = Ticket.RAISED

            ticketChannelEventResponse = create_update_model(
                TicketChannelEvent, ticketChannelEventForm, api_instance=self)
            print("dfsdfdsf", ticketChannelEventResponse)

        
            return Response(get_success_response("Ticket Raised Successfully", None, {}))

        return Response(get_validation_failure_response([], "Invalid Request"))


class AddTicketEvent(GenericCrudApiView):

    base_model = Ticket

    def proceed_post(self, request):

        data = request.data

        ticket_id = data['id']

        ticketForm = {}
        ticketForm['id'] = ticket_id
        # data
        employee_company_info = self.get_employee_company_info()
        # ticketForm['event_by_id'] = employee_company_info.id

        ticket_response = create_update_model(
            Ticket, ticketForm, api_instance=self)

        ticketChannelEventForm = {}
        ticketChannelEventForm['ticket_id'] = ticket_id
        ticketChannelEventForm['event_by_id'] = employee_company_info.id

        if 'message' in data:
            ticketChannelEventForm['message'] = data['message']
            ticketChannelEventForm['event_type'] = TicketChannelEvent.TEXT_MESSAGE
        

        ticketChannelEventResponse = create_update_model(
            TicketChannelEvent, ticketChannelEventForm, api_instance=self)
        print("dfsdfdsf", ticketChannelEventResponse)

        # ticketChannelEventForm['ticket_status'] = Ticket.RAISED

        #     ticketChannelEventResponse = create_update_model(
        #         TicketChannelEvent, ticketChannelEventForm, api_instance=self)

        # if ticket_response['status'] == True:

        #     ticket_id = ticket_response['ids'][0]
        #     ticketChannelEventForm = {}
        #     ticketChannelEventForm['ticket_id'] = ticket_id
        #     ticketChannelEventForm['event_type'] = TicketChannelEvent.TICKET_STATUS
        #     ticketChannelEventForm['ticket_status'] = Ticket.RAISED

        #     ticketChannelEventResponse = create_update_model(
        #         TicketChannelEvent, ticketChannelEventForm, api_instance=self)
        #     print("dfsdfdsf", ticketChannelEventResponse)

        # #
        return Response(get_success_response("Details updated successfully", None, {}))

        return Response(get_validation_failure_response([], "Invalid Request"))


class Index(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data

        return Response(get_success_response(None, None, {}))


class GetTickets(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer = None
    list_serializer = GetTicketsSerializer
    per_page_count = 10

    def get_list_query(self):
        return get_tickets()


class GetTicketTags(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer = None
    list_serializer = GetTicketTagsSerializer
    per_page_count = 10

    def get_list_query(self):
        return get_ticket_tags()


class GetTicketEvents(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer = None
    list_serializer = GetTicketEventsSerializer
    per_page_count = 10

    def get_list_query(self):
        return get_ticket_events(self.payload['ticket_id'])
