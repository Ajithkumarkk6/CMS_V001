from email.policy import default
from django.db import models
from django.contrib.auth.models import User  # new
from company.models import CompanyMeta, CompanyBranchInfo, CompanyDepartment, CompanySector
from authentication.models import BaseModelMixin, UserAuthentication
from django.utils.timezone import now
from employee.models import EmployeeCompanyInfo, EmployeePersonalInfo


class TicketTag(BaseModelMixin):
    name = models.CharField(max_length=210, null=True, blank=True)
    description = models.CharField(max_length=210, null=True, blank=True)


class TicketAttachment(BaseModelMixin):
    name = models.CharField(max_length=210, null=True, blank=True)
    attachment = models.FileField(
        upload_to='ticket', null=True, blank=True)


class Ticket(BaseModelMixin):

    many_to_many_fields = ['tags']

    def get_many_to_many_class(self, name):
        if name == 'tags':
            return TicketTag
        return None

    RAISED = 'RAI'
    IN_PROGRESS = 'INP'
    CANCELLED = 'CAN'
    CLOSED = 'CLS'
    ON_HOLD = 'ONH'
    REJECTED = 'REJ'

    TICKET_STATUS_CHOICES = [
        (RAISED, 'Raised'),
        (IN_PROGRESS, 'In Progress'),
        (CANCELLED, 'Cancel'),
        (CLOSED, 'Close'),
        (ON_HOLD, 'On Hold'),
        (REJECTED, 'Reject')
    ]
    ticket_status = models.CharField(
        max_length=5,
        choices=TICKET_STATUS_CHOICES,
        default=RAISED,
    )

    # def is_upperclass(self):
    #     return self.year_in_school in {self.JUNIOR, self.SENIOR}

    title = models.CharField(max_length=210, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    brand_branch = models.ForeignKey(
        CompanyBranchInfo, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    reference_number = models.CharField(max_length=50, null=True, blank=True)
    photo = models.ImageField(
        upload_to='ticket', null=True, blank=True)
    tags = models.ManyToManyField(TicketTag, blank=True)
    created_by = models.ForeignKey(
        EmployeeCompanyInfo, related_name='ticket_created_by', on_delete=models.CASCADE, null=True, blank=True)
    assigned_to = models.ForeignKey(
        EmployeeCompanyInfo, related_name='ticket_assigned_to', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title + "==="+str(self.id) + "==="


class TicketAttachmentMessage(BaseModelMixin):

    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=210, null=True, blank=True)
    attachments = models.ManyToManyField(TicketAttachment)


class TicketChannelEvent(BaseModelMixin):

    TICKET_STATUS = 'EVS'
    TEXT_MESSAGE = 'TEM'
    TAGGED_USER = 'TGU'
    MESSAGE_ATTACHMENT = 'MEA'

    EVENT_TYPE_CHOICES = [
        (TEXT_MESSAGE, 'Text Message'),
        (TICKET_STATUS, 'Ticket Status Change'),
        (TAGGED_USER, 'Tagged User to Ticket'),
        (MESSAGE_ATTACHMENT, 'Attached File to Ticket')
    ]

    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, null=True, blank=True)

    event_type = models.CharField(
        max_length=5,
        choices=EVENT_TYPE_CHOICES,
        default=TICKET_STATUS,
    )
    ticket_status = models.CharField(
        max_length=5,
        choices=Ticket.TICKET_STATUS_CHOICES,
        default=Ticket.RAISED,
    )
    message = models.TextField(null=True, blank=True)
    attachments = models.ManyToManyField(TicketAttachmentMessage, blank=True)
    assigned_to = models.ForeignKey(
        EmployeeCompanyInfo, related_name='assigned_to', on_delete=models.CASCADE, null=True, blank=True)
    tagged_users = models.ManyToManyField(
        EmployeeCompanyInfo, related_name='tagged_users', blank=True)
    event_by = models.ForeignKey(
        EmployeeCompanyInfo, related_name='event_by', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        title = str(self.ticket.title) + "==="
        #     str(self.is_parent) + "==="+str(self.id)
        # if self.parent is not None:
        #     title = title + "===" + self.parent.display_name
        return title
