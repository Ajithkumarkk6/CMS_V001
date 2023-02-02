from email.policy import default
from django.db import models
from authentication import constants
from authentication.models import BaseModelMixin
from authentication.constants import DEFAULT_RADIUS
from django.contrib.auth.models import User # new
# from .models import EmployeeCompanyInfo
from django.utils.timezone import now

class CompanySector(BaseModelMixin):
    name = models.CharField(max_length=220, null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)

    def __str__(self):
        return self.name +"==="+str(self.id)


class CompanyTypeOfBusiness(BaseModelMixin):
    name = models.CharField(max_length=220, null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)

    def __str__(self):
        return self.name +"==="+str(self.id)


# class CompanyTypeOfBusiness(BaseModelMixin):
#     name = models.CharField(max_length=220, null=True, blank=True)
#     tag = models.CharField(max_length=220, null=True, blank=True)

#     def __str__(self):
#         return self.name +"==="+str(self.id)




class CompanyMeta(BaseModelMixin):
    brand_name = models.CharField(max_length=200, null=True, blank=True)
    display_name = models.CharField(max_length=200, null=True, blank=True)
    code = models.CharField(max_length=30, null=True, blank=True)
    registered_name = models.CharField(max_length=200, null=True, blank=True)
    business_type = models.CharField(max_length=20, null=True, blank=True)
    pan = models.CharField(max_length=30, null=True, blank=True)
    gst = models.CharField(max_length=30, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    sector = models.ForeignKey(CompanySector, on_delete=models.SET_NULL, null=True, blank=True)
    type_of_business = models.ForeignKey(CompanyTypeOfBusiness, on_delete=models.SET_NULL, null=True, blank=True)
    attachment_gst = models.ImageField(upload_to='companymeta', null=True, blank=True)
    attachment_logo = models.ImageField(upload_to='companymeta', null=True, blank=True)
    attachment_pan = models.ImageField(upload_to='companymeta', null=True, blank=True)
    details = models.CharField(max_length=220, null=True, blank=True)

    def __str__(self):
        return self.brand_name +"==="+str(self.id)

class CompanyContactInfo(BaseModelMixin):
    is_default = models.BooleanField(default=True)
    address_id = models.CharField(max_length=30, null=True, blank=True)
    address_line_01 = models.CharField(max_length=70, null=True, blank=True)
    address_line_02 = models.CharField(max_length=70, null=True, blank=True)
    mobile_number_01 = models.CharField(max_length=20, null=True, blank=True)
    mobile_number_02 = models.CharField(max_length=20, null=True, blank=True)
    communication_address = models.CharField(max_length=220, null=True, blank=True)
    billing_address = models.CharField(max_length=220, null=True, blank=True)
    city = models.CharField(max_length=70, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    google_place_link = models.CharField(max_length=220, null=True, blank=True)


class CompanyGeoLocationInfo(BaseModelMixin):
    location_latitude = models.CharField(max_length=70, null=True, blank=True)
    location_longitude = models.CharField(max_length=70, null=True, blank=True)
    fencing_radius = models.IntegerField(default=DEFAULT_RADIUS, null=True, blank=True)



class CompanyBranchInfo(BaseModelMixin):
    company = models.ForeignKey(CompanyMeta, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    branch_id = models.CharField(max_length=30, null=True, blank=True)
    display_name = models.CharField(max_length=30, null=True, blank=True)
    code = models.CharField(max_length=10, null=True, blank=True)
    is_parent = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    can_update_location = models.BooleanField(default=False)
    company_contact = models.ForeignKey(CompanyContactInfo, unique=True, on_delete=models.SET_NULL, null=True, blank=True)
    company_geolocation = models.ForeignKey(CompanyGeoLocationInfo, unique=True, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        title =  str(self.display_name) +"===" + str(self.is_parent) + "==="+str(self.id)
        if self.parent is not None:
            title = title + "===" + self.parent.display_name
        return title


class WeekDay(BaseModelMixin):
    is_working = models.BooleanField(default=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    day_code = models.IntegerField(default=constants.DAY_NONE)

class CompanyBranchWeeklyCalendar(BaseModelMixin):
    company = models.ForeignKey(CompanyMeta, on_delete=models.CASCADE, null=True, blank=True)
    company_branch = models.ForeignKey(CompanyBranchInfo, on_delete=models.SET_NULL, null=True, blank=True)
    day_mon = models.ForeignKey(WeekDay, related_name='monday', on_delete=models.SET_NULL, null=True, blank=True)
    day_tue = models.ForeignKey(WeekDay, related_name='tuesday', on_delete=models.SET_NULL, null=True, blank=True)
    day_wed = models.ForeignKey(WeekDay, related_name='wednesday', on_delete=models.SET_NULL, null=True, blank=True)
    day_thu = models.ForeignKey(WeekDay, related_name='thursday', on_delete=models.SET_NULL, null=True, blank=True)
    day_fri = models.ForeignKey(WeekDay, related_name='friday', on_delete=models.SET_NULL, null=True, blank=True)
    day_sat = models.ForeignKey(WeekDay, related_name='saturday', on_delete=models.SET_NULL, null=True, blank=True)
    day_sun = models.ForeignKey(WeekDay, related_name='sunday', on_delete=models.SET_NULL, null=True, blank=True)

class CompanyDepartment(BaseModelMixin):

    name = models.CharField(max_length=220, null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)
    company = models.ForeignKey(CompanyMeta, on_delete=models.CASCADE, null=True, blank=True)
    company_branch = models.ForeignKey(CompanyBranchInfo, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name + "==="+str(self.id)

class CompanyDocument(BaseModelMixin):

    title = models.CharField(max_length=220, null=True, blank=True)
    photo = models.ImageField(upload_to='company_document', null=True, blank=True)
    time_stamp = models.DateTimeField(default=now, editable=True)

    def __str__(self):
        title =  "==="
        return title


class VehicleTypes(BaseModelMixin):
    vehicle_type = models.CharField(max_length=50, null=True, blank=True)
    free_time_in_mins = models.CharField(max_length=12, null=True, blank=True)
    free_time_in_mins_price = models.CharField(max_length=12, null=True, blank=True)
    min_time_in_min = models.CharField(max_length=12, null=True, blank=True)
    min_time_in_min_price = models.CharField(max_length=12, null=True, blank=True)
    fixed_time_in_min = models.CharField(max_length=12, null=True, blank=True)
    fixed_time_in_min_price = models.CharField(max_length=12, null=True, blank=True)
    company_branch = models.ForeignKey(CompanyBranchInfo, on_delete=models.SET_NULL, null=True, blank=True)

class VehicleDetails(BaseModelMixin):
    vehicle_type = models.ForeignKey(VehicleTypes, on_delete=models.CASCADE, null=True, blank=True)
    vehicle_number = models.CharField(max_length=40, null=True, blank=True)
    base_price = models.CharField(max_length=10, null=True, blank=True)
    entry_time = models.DateTimeField(null=True, blank=True)
    exit_time = models.DateTimeField(null=True, blank=True)
    company = models.ForeignKey(CompanyMeta, on_delete=models.CASCADE, null=True, blank=True)
    company_branch = models.ForeignKey(CompanyBranchInfo, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_id = models.CharField(max_length=10, null=True, blank=True)
    total_time = models.CharField(max_length=10, null=True, blank=True)
    total_price = models.CharField(max_length=10, null=True, blank=True)
    payment_mode = models.CharField(max_length=10, null=True, blank=True)
    is_complete = models.BooleanField(default=False)
