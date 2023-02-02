from email.policy import default
from django.db import models
from django.contrib.auth.models import User # new
from company.models import CompanyMeta, CompanyBranchInfo, CompanyDepartment, CompanySector
from authentication.models import BaseModelMixin, UserAuthentication
from django.utils.timezone import now
from employee.models import EmployeeCompanyInfo
from .appointment_values import *
from providerservice.models import BrandBranchServices, ServiceMasterUomFormField
from employee.models import EmployeePersonalInfo

'''cart bucket'''
class CartBucket(BaseModelMixin):

    bucket_id = models.CharField(max_length=220, null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)

    def __str__(self):
        return self.name +"==="+str(self.id)


class AppointmentStatus(BaseModelMixin):

    name = models.CharField(max_length=200, unique=False)
    code = models.CharField(max_length=200, unique=True)
    sub_text = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to='profile_pics', blank=True)
    status_note = models.CharField(max_length=200, unique=False)
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True)

    def __str__(self):
            return str(self.name)

class Appointment(BaseModelMixin):

    brand = models.ForeignKey(CompanyMeta, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(CompanyBranchInfo, on_delete=models.CASCADE, null=True, blank=True)
    appointment_id = models.CharField(max_length=15, unique=True)
    appointment_status = models.ForeignKey(AppointmentStatus, on_delete=models.SET_NULL, null=True, blank=True)
    user_customer = models.ForeignKey(EmployeeCompanyInfo,  related_name='user_customer', on_delete=models.CASCADE)
    schedule_requested_time = models.DateTimeField(blank=True, null=True)
    checked_in_time = models.DateTimeField(blank=True, null=True)
    process_initiated_time = models.DateTimeField(blank=True, null=True)
    process_completed_time = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(default='', null=True, blank=True)
    status_note = models.CharField(max_length=200, default='', null=True)
    appointment_accepted = models.BooleanField(default=False)
    appointment_rejected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_status_title(self):

        status = get_string_value_by_user(KEY_D_PENDING_APPROVAL)

        if self.appointment_status and hasattr(self.appointment_status, 'code'):
            appointment_status = self.appointment_status.code

            if appointment_status == APPOINTMENT_STATUS_AGENT_APPROVED:
                status = get_string_value_by_user(KEY_D_APPOINTMENT_APPROVED)
            elif appointment_status == APPOINTMENT_STATUS_INITIATED:
                status = get_string_value_by_user(KEY_D_PENDING_APPROVAL)
            elif appointment_status == APPOINTMENT_STATUS_AGENT_REJECTED_NO_SLOT:
                status = get_string_value_by_user(KEY_D_APPOINTMENT_REJECTED)
            elif appointment_status == APPOINTMENT_STATUS_AGENT_REJECTED_OTHERS:
                status = get_string_value_by_user(KEY_D_APPOINTMENT_REJECTED)
            elif appointment_status == APPOINTMENT_STATUS_NO_SHOW:
                status = get_string_value_by_user(KEY_D_BOOKING_NO_SHOW)
            elif appointment_status == APPOINTMENT_STATUS_ONGOING:
                status = get_string_value_by_user(KEY_D_ONGOING)
            elif appointment_status == APPOINTMENT_STATUS_COMPLETED:
                status = get_string_value_by_user(KEY_D_COMPLETED)
            elif appointment_status == APPOINTMENT_STATUS_CANCELLED:
                status = get_string_value_by_user(KEY_D_APPOINTMENT_STATUS_CANCELLED)

        return status

    def get_status_text(self):

        status = get_string_value_by_user(KEY_D_PENDING_APPROVAL)
        if self.appointment_status and hasattr(self.appointment_status, 'code'):
            appointment_status = self.appointment_status.code

            if appointment_status == APPOINTMENT_STATUS_AGENT_APPROVED:
                status = get_string_value_by_user(KEY_D_SHOW_THE_QR_CODE_CHECK_IN)
            elif appointment_status == APPOINTMENT_STATUS_INITIATED:
                status = get_string_value_by_user(KEY_D_AGENT_APPROVE)
            elif appointment_status == APPOINTMENT_STATUS_AGENT_REJECTED_NO_SLOT:
                status = get_string_value_by_user(KEY_D_NO_SLOT_AVAILABLE)
            elif appointment_status == APPOINTMENT_STATUS_AGENT_REJECTED_OTHERS:
                status = get_string_value_by_user(KEY_D_NOT_OPERATING_REQUESTED_TIME)
            elif appointment_status == APPOINTMENT_STATUS_NO_SHOW:
                status = get_string_value_by_user(KEY_D_BOOKING_NO_SHOW)
            elif appointment_status == APPOINTMENT_STATUS_ONGOING:
                status = get_string_value_by_user(KEY_D_APPOINTMENT_MARKED_AS_ONGOING)
            elif appointment_status == APPOINTMENT_STATUS_COMPLETED:
                status = get_string_value_by_user(KEY_D_BOOKING_MARKED_AS_COMPLETED)
            elif appointment_status == APPOINTMENT_STATUS_CANCELLED:
                status = get_string_value_by_user(KEY_D_APPOINTMENT_STATUS_CANCELLED)

        return status


    def __str__(self):
        return str(self.appointment_id) +"==="+ str(self.appointment_status)+"==="+str(self.id) +"==="+str(self.branch.id)


class AppointmentItem(BaseModelMixin):

    appointment_item_id = models.CharField(max_length=15, unique=True)
    brand_branch = models.ForeignKey(CompanyBranchInfo, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(BrandBranchServices, on_delete=models.CASCADE, null=True, blank=True)
    item_price = models.FloatField(max_length=5, default=1.0)
    status_note = models.CharField(max_length=200, unique=False)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    base_user = models.ForeignKey(EmployeePersonalInfo, related_name='measurement_unit', on_delete=models.CASCADE, default="", unique=False)
    order_user_info = models.JSONField(default=[])

    def __str__(self):
        return str(self.appointment_item_id)

