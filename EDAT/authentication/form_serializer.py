from rest_framework import serializers
from employee.models import EmployeePersonalInfo
from company.models import CompanyMeta, CompanyContactInfo, CompanyBranchInfo


class EmployeePersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePersonalInfo
        fields = ['mobile_number']

class CompanyMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyMeta
        fields = ['brand_name', 'display_name', 'registered_name', 'is_active']

class CompanyContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyContactInfo
        fields = ['is_default', 'communication_address', 'pincode', 'country']

class CompanyBranchInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBranchInfo
        fields = ['is_default', 'communication_address', 'pincode', 'country']
