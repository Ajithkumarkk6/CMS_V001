from django.contrib import admin
from .models import BrandBranchCategory, BrandBranchServices, BrandServiceMasterUomFormField, BrandServiceMasterUomFormFieldServiceMapping, ServiceType, FormFieldType, ServiceMasterUomFormField, BrandServiceConfig, PredefinedCategory, PredefinedServices, BrandCategory, BrandServices, ServiceMasterUomFormFieldServiceMapping

admin.site.register(ServiceType)
admin.site.register(ServiceMasterUomFormField)
admin.site.register(ServiceMasterUomFormFieldServiceMapping)
admin.site.register(FormFieldType)
admin.site.register(BrandServiceConfig)
admin.site.register(PredefinedCategory)
admin.site.register(PredefinedServices)
admin.site.register(BrandCategory)
admin.site.register(BrandServices)
admin.site.register(BrandBranchCategory)
admin.site.register(BrandBranchServices)
admin.site.register(BrandServiceMasterUomFormField)
admin.site.register(BrandServiceMasterUomFormFieldServiceMapping)






