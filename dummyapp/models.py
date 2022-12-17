from django.db import models
from django.contrib.auth.models import User # new
from company.models import CompanyMeta, CompanyBranchInfo, CompanyDepartment
from authentication.models import BaseModelMixin, UserAuthentication
from django.utils.timezone import now

# class EmployeeDesignation(BaseModelMixin):
#     name = models.CharField(max_length=220, null=True, blank=True)
#     tag = models.CharField(max_length=220, null=True, blank=True)
#     company = models.ForeignKey(CompanyMeta, on_delete=models.CASCADE, null=True, blank=True)
#     company_branch = models.ForeignKey(CompanyBranchInfo, on_delete=models.SET_NULL, null=True, blank=True)
#     is_admin = models.BooleanField(default=False)
   
#     def __str__(self):
#         return self.name +"===" +str(self.id)
