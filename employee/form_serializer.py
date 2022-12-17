from rest_framework import serializers
from employee.models import EmployeePersonalInfo
from company.models import CompanyMeta, CompanyContactInfo, CompanyBranchInfo

class EmployeePersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePersonalInfo
        fields = ['gender', 'aadhar', 'mobile_number']
