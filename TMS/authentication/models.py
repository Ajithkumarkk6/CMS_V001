from django.db import models
from django.contrib.auth.models import User  # new
import uuid


class BaseModelMixin(models.Model):

    many_to_many_fields = ['tags']

    def get_many_to_many_class(self, name):
        return None

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class AppBaseConfig(BaseModelMixin):
    current_version_android = models.CharField(
        max_length=8, null=True, blank=True)
    minimum_support_version_android = models.CharField(
        max_length=8, null=True, blank=True)
    current_version_ios = models.CharField(max_length=8, null=True, blank=True)
    minimum_support_version_ios = models.CharField(
        max_length=8, null=True, blank=True)
    last_sync_time = models.DateTimeField(
        auto_now=False, null=True, blank=True)


class UserAuthentication(BaseModelMixin):
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    mobile_otp = models.CharField(max_length=8, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_login_action = models.BooleanField(default=False)
    is_otp_verified = models.BooleanField(default=False)
    user_registation_status = models.IntegerField(default=0)
    admin_registration_designation = models.CharField(
        max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.first_name


class UserCredentialValidation(BaseModelMixin):
    mobile_number = models.CharField(max_length=12, null=True, blank=True)
    mobile_otp = models.CharField(max_length=8, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_otp_verified = models.BooleanField(default=False)
    user_registation_status = models.IntegerField(default=0)
    admin_registration_designation = models.CharField(
        max_length=200, null=True, blank=True)

    def __str__(self):
        return self.mobile_number
