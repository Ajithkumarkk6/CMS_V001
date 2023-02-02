from rest_framework import serializers
from employee.models import EmployeeDesignation
from company.models import CompanyMeta, CompanyContactInfo, CompanyBranchInfo, CompanyDepartment, CompanySector, CompanyTypeOfBusiness


class CompanyTypeOfBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyTypeOfBusiness
        fields = ['id', 'name']


class CompanySectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySector
        fields = ['id', 'name']


class DepartmentDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDepartment
        fields = ['id', 'name' ]

class BranchListSerializer(serializers.ModelSerializer):
    parent_id = serializers.SerializerMethodField()
    has_location = serializers.SerializerMethodField()
    geo_location_id = serializers.SerializerMethodField()
    fencing_radius = serializers.SerializerMethodField()
    

    class Meta:
        model = CompanyBranchInfo
        fields = ['id', 'name' , 'parent_id', 'has_location', 'fencing_radius', 'can_update_location', 'geo_location_id']

    def get_geo_location_id(self, obj):
        if obj.company_geolocation is not None:
            return obj.company_geolocation.id
        else:
            return None

    def get_fencing_radius(self, obj):
        if obj.company_geolocation is not None:
            return obj.company_geolocation.fencing_radius
        else:
            return 30


    def get_parent_id(self, obj):
        if obj.parent is not None:
            return obj.parent.id
        else:
            return None

    def get_has_location(self, obj):
        return obj.company_geolocation is not None
