from rest_framework import serializers
from .models import TicketTag, TicketAttachmentMessage, Ticket, TicketAttachment, TicketChannelEvent
from company.response_serializer import CompanyMetaSerializer
from employee.models import EmployeePersonalInfo


class GetTicketTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketTag
        fields = ['id', 'name']


class GetTicketsSerializer(serializers.ModelSerializer):

    by_user = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    raised_by_company = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'by_user', 'tags',
                  'raised_by_company', 'ticket_status']

    def get_by_user(self, obj):
        if obj.created_by is not None:
            user_details = {'id': obj.created_by.id,
                            'name': obj.created_by.user.first_name}
            user_details['phone'] = EmployeePersonalInfo.objects.get(
                user=obj.created_by.user).mobile_number
            user_details['email'] = obj.created_by.user.email
            return user_details
        else:
            return None

    def get_tags(self, obj):
        return GetTicketTagsSerializer(obj.tags.all(), many=True).data

    def get_raised_by_company(self, obj):
        return CompanyMetaSerializer(obj.brand_branch.company).data


class GetTicketEventsSerializer(serializers.ModelSerializer):

    by_user = serializers.SerializerMethodField()
    tagged_users = serializers.SerializerMethodField()
    attachments=serializers.SerializerMethodField()

    class Meta:
        model = TicketChannelEvent
        fields = ['id', 'by_user', 'event_type',
                  'message', 'created_at', 'tagged_users','attachments']

    def get_by_user(self, obj):
        if obj.event_by is not None:
            return {'id': obj.event_by.id, 'name': obj.event_by.user.first_name}
        else:
            return None
    

    def get_tagged_users(self, obj):
        users = []
        for eu in obj.tagged_users.all():
            users.append({'id': eu.id, 'name': eu.user.first_name})
        return users
    def get_attachments(self, obj):
        attachments= []
        if obj.attachments is not None:
            for att in obj.attachments.attachments.all():
                attachments.append({'id':att.id,'name':att.name,'attachment_file':att.attachment.url})
                return attachments
        else:
            return None
