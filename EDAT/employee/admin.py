from django.contrib import admin
from .models import EmployeeDocumentGroup, EmployeeDocumentLocker, EmployeePersonalInfo, EmployeeFacePhoto, EmployeeDocument, EmployeeCompanyInfo, EmployeeFinancialInfo, EmployeeDesignation,AnonymousComplaintTicket


class AUserAuthentication(admin.ModelAdmin):
    search_fields = ['id', 'user__first_name', 'user__email']

class AEmployeePersonalInfo(admin.ModelAdmin):
    search_fields = ['id', 'user__first_name', 'user__email', 'mobile_number']


admin.site.register(EmployeePersonalInfo, AEmployeePersonalInfo)
admin.site.register(EmployeeCompanyInfo, AUserAuthentication)
admin.site.register(EmployeeFinancialInfo, AUserAuthentication)
admin.site.register(EmployeeDesignation)
admin.site.register(EmployeeFacePhoto)
admin.site.register(EmployeeDocument)
admin.site.register(EmployeeDocumentLocker)
admin.site.register(EmployeeDocumentGroup)
admin.site.register(AnonymousComplaintTicket)







