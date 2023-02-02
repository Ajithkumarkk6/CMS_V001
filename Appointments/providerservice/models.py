from email.policy import default
from django.db import models
from django.contrib.auth.models import User # new
from company.models import CompanyMeta, CompanyBranchInfo, CompanyDepartment, CompanySector
from authentication.models import BaseModelMixin, UserAuthentication
from django.utils.timezone import now

'''all available service types'''
class ServiceType(BaseModelMixin):
    service_sector = models.ForeignKey(CompanySector, on_delete=models.SET_NULL, null=True, blank=True)
    photo = models.ImageField(upload_to='providerservice', null=True, blank=True)
    name = models.CharField(max_length=220, null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)

    def __str__(self):
        return self.name +"==="+str(self.id)

class FormFieldType(BaseModelMixin):    

    name = models.CharField(max_length=220, null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)

    def __str__(self):
        return self.name +"==="+str(self.id)

'''company service type mapping'''
class ServiceMasterUomFormField(BaseModelMixin):

    name = models.CharField(max_length=220, null=True, blank=True)
    photo = models.ImageField(upload_to='providerservice', null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)
    description = models.CharField(max_length=10, null=True, blank=True)
    is_display = models.BooleanField(default=False)
    is_manditory = models.BooleanField(default=False)
    field_type = models.ForeignKey(FormFieldType, on_delete=models.SET_NULL, null=True, blank=True)
    support_data = models.JSONField(default={}, null=True, blank=True)

    def __str__(self):
        return self.name +"==="+str(self.id)

class ServiceMasterUomFormFieldServiceMapping(BaseModelMixin):

    display_order = models.IntegerField(default=-1)
    service_type = models.ForeignKey(ServiceType, on_delete=models.SET_NULL, null=True, blank=True)
    master_uom = models.ForeignKey(ServiceMasterUomFormField, on_delete=models.SET_NULL, null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)
    description = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.display_order) +"==="+ self.master_uom.name+"==="+str(self.service_type.name)



'''company service type mapping'''
class BrandServiceMasterUomFormField(BaseModelMixin):
    
    name = models.CharField(max_length=220, null=True, blank=True)
    photo = models.ImageField(upload_to='providerservice', null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)
    description = models.CharField(max_length=10, null=True, blank=True)
    is_display = models.BooleanField(default=False)
    is_manditory = models.BooleanField(default=False)
    brand = models.ForeignKey(CompanyMeta, on_delete=models.CASCADE, null=True, blank=True)
    meta_reference = models.ForeignKey(ServiceMasterUomFormFieldServiceMapping, on_delete=models.CASCADE, null=True, blank=True)
    field_type = models.ForeignKey(FormFieldType, on_delete=models.SET_NULL, null=True, blank=True)
    support_data = models.JSONField(default={}, null=True, blank=True)

    def __str__(self):
        return self.name +"==="+str(self.id)

class BrandServiceMasterUomFormFieldServiceMapping(BaseModelMixin):
    
    display_order = models.IntegerField(default=-1)
    master_uom = models.ForeignKey(BrandServiceMasterUomFormField, on_delete=models.SET_NULL, null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)
    description = models.CharField(max_length=10, null=True, blank=True)
    brand = models.ForeignKey(CompanyMeta, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.display_order) +"==="+ self.master_uom.name+"==="
        # +str(self.service_type.name)




'''company service type mapping'''
class BrandServiceConfig(BaseModelMixin):

    name = models.CharField(max_length=220, null=True, blank=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(CompanyMeta, on_delete=models.CASCADE, null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)
    description = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name +"==="+str(self.id)



class PredefinedCategory(BaseModelMixin):
    name = models.CharField(max_length=30, null=True, blank=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, null=True, blank=True)
    display_name = models.CharField(max_length=30, null=True, blank=True)
    code = models.CharField(max_length=10, null=True, blank=True)
    photo = models.ImageField(upload_to='providerservicepredefined', null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    is_parent = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_independent_slot = models.BooleanField(default=True)

    def __str__(self):
        return self.name +"==="+str(self.id)

class PredefinedServices(BaseModelMixin):

    name = models.CharField(max_length=30, null=True, blank=True)
    display_name = models.CharField(max_length=30, null=True, blank=True)
    code = models.CharField(max_length=10, null=True, blank=True)
    photo = models.ImageField(upload_to='providerservicepredefined', null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    is_parent = models.BooleanField(max_length=10, null=True, blank=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(PredefinedCategory, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_display = models.BooleanField(default=True)

    def __str__(self):
        return self.name +"==="+str(self.id)

class BrandCategory(BaseModelMixin):

    brand = models.ForeignKey(CompanyMeta, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, null=True, blank=True)
    display_name = models.CharField(max_length=30, null=True, blank=True)
    code = models.CharField(max_length=10, null=True, blank=True)
    meta_reference = models.ForeignKey(PredefinedCategory, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to='providerservice', null=True, blank=True)
    description = models.CharField(max_length=10, null=True, blank=True)
    is_parent = models.BooleanField(max_length=10, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_independent_slot = models.BooleanField(default=True)
    service_time = models.IntegerField(default=30)
    service_price = models.IntegerField(default=30)

    def __str__(self):
        return self.name +"==="+str(self.id)+ "==="+str(self.is_parent)

class BrandBranchCategory(BaseModelMixin):

    name = models.CharField(max_length=30, null=True, blank=True)
    brand_category = models.ForeignKey(BrandCategory, on_delete=models.CASCADE, null=True, blank=True)
    brand_branch = models.ForeignKey(CompanyBranchInfo, on_delete=models.CASCADE, null=True, blank=True)
    display_name = models.CharField(max_length=30, null=True, blank=True)
    code = models.CharField(max_length=10, null=True, blank=True)
    photo = models.ImageField(upload_to='providerservice', null=True, blank=True)
    description = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    service_time = models.IntegerField(default=30)
    service_price = models.IntegerField(default=30)

    def __str__(self):
        return self.name +"==="+str(self.id)+ "==="


class BrandServices(BaseModelMixin):

    brand = models.ForeignKey(CompanyMeta, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    brand_category = models.ForeignKey(BrandCategory, on_delete=models.CASCADE, null=True, blank=True)
    display_name = models.CharField(max_length=30, null=True, blank=True)
    code = models.CharField(max_length=10, null=True, blank=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, null=True, blank=True)
    meta_reference = models.ForeignKey(PredefinedServices, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to='providerservice', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    service_time = models.IntegerField(default=30)
    service_price = models.IntegerField(default=30)
    is_display = models.BooleanField(default=True)
    is_display_price = models.BooleanField(default=True)

    def __str__(self):
        return self.name +"==="+str(self.id)


class BrandBranchServices(BaseModelMixin):

    brand_service = models.ForeignKey(BrandServices, on_delete=models.CASCADE, null=True, blank=True)
    brand_branch_category = models.ForeignKey(BrandBranchCategory, on_delete=models.CASCADE, null=True, blank=True)
    brand_branch = models.ForeignKey(CompanyBranchInfo, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    service_time = models.IntegerField(default=30)
    service_price = models.IntegerField(default=30)
    is_display = models.BooleanField(default=True)
    is_display_price = models.BooleanField(default=True)

    def __str__(self):
        return self.brand_service.name + "===" + str(self.id)


# class BrandBranchProducts(BaseModelMixin):

#     brand = models.ForeignKey(CompanyMeta, on_delete=models.CASCADE, null=True, blank=True)
#     branch = models.ForeignKey(CompanyBranchInfo, on_delete=models.CASCADE, null=True, blank=True)
#     name = models.CharField(max_length=30, null=True, blank=True)
#     display_name = models.CharField(max_length=30, null=True, blank=True)
#     code = models.CharField(max_length=10, null=True, blank=True)
#     price = models.IntegerField(default=-1)
#     is_active = models.BooleanField(default=True)
#     is_display = models.BooleanField(default=True)
#     is_display_price = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name +"==="+str(self.id)


