from django.contrib import admin
from company.models import CompanyBranchWeeklyCalendar, CompanyDocument, CompanySector, CompanyTypeOfBusiness, CompanyMeta, CompanyBranchInfo, CompanyContactInfo, CompanyGeoLocationInfo, CompanyDepartment, WeekDay

admin.site.register(CompanyMeta)
admin.site.register(CompanyBranchInfo)
admin.site.register(CompanyContactInfo)
admin.site.register(CompanyGeoLocationInfo)
admin.site.register(CompanyDepartment)
admin.site.register(CompanyTypeOfBusiness)
admin.site.register(CompanySector)
admin.site.register(CompanyDocument)
admin.site.register(WeekDay)
admin.site.register(CompanyBranchWeeklyCalendar)




