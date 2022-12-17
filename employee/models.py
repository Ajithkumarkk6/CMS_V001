from django.db import models
from django.contrib.auth.models import User # new
from company.models import CompanyMeta, CompanyBranchInfo, CompanyDepartment
from authentication.models import BaseModelMixin, UserAuthentication
from django.utils.timezone import now

class EmployeeDesignation(BaseModelMixin):
    name = models.CharField(max_length=220, null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)
    company = models.ForeignKey(CompanyMeta, on_delete=models.CASCADE, null=True, blank=True)
    company_branch = models.ForeignKey(CompanyBranchInfo, on_delete=models.SET_NULL, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
   
    def __str__(self):
        return self.name +"===" +str(self.id)

class EmployeePersonalInfo(BaseModelMixin):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=5)
    aadhar = models.CharField(max_length=130, null=True, blank=True)
    dob = models.DateField(auto_now=False, null=True, blank=True)
    blood_group = models.CharField(max_length=70, null=True, blank=True)
    mobile_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    attachment_profile = models.ImageField(upload_to='employee', null=True, blank=True)
    attached_users = models.JSONField(default=[])

    def __str__(self):
        return self.user.first_name +"==="+ self.mobile_number+"==="+str(self.id)


class EmployeeDocument(BaseModelMixin):

    title = models.CharField(max_length=220, null=True, blank=True)
    photo = models.ImageField(upload_to='employee_document', null=True, blank=True)
    time_stamp = models.DateTimeField(default=now, editable=True)

    def __str__(self):
        title = str(self.id)+"==="+str(self.time_stamp) 
        return title

class EmployeeFacePhoto(BaseModelMixin):
    tag = models.CharField(max_length=100, null=True, blank=True)
    photos = models.ManyToManyField(EmployeeDocument)

class EmployeeDocumentGroup(BaseModelMixin):
    name = models.CharField(max_length=100, null=True, blank=True)


class EmployeeDocumentLocker(BaseModelMixin):
    title = models.CharField(max_length=100, null=True, blank=True)
    group = models.ForeignKey(EmployeeDocumentGroup, on_delete=models.SET_NULL, null=True, blank=True)
    photos = models.ManyToManyField(EmployeeDocument)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.title) + "==="+ str(self.id) 

class EmployeeFinancialInfo(BaseModelMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pan = models.CharField(max_length=30, null=True, blank=True)


class EmployeeCompanyInfo(BaseModelMixin):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=30, null=True, blank=True)
    designation =  models.ForeignKey(EmployeeDesignation, on_delete=models.SET_NULL, null=True, blank=True)
    department =  models.ForeignKey(CompanyDepartment, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(CompanyMeta, on_delete=models.CASCADE, null=True, blank=True)
    company_branch = models.ForeignKey(CompanyBranchInfo, on_delete=models.CASCADE, null=True, blank=True)
    date_of_joining = models.DateField(auto_now=False, null=True, blank=True)
    employment_type = models.CharField(max_length=40, null=True, blank=True)
    authentication = models.ForeignKey(UserAuthentication, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.user.first_name + "==="+ self.company.brand_name + "===="+str(self.id)
        # str(self.id) 
        # +"==="+ str(self.company_branch.name)

