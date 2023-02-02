from rest_framework import serializers
from employee.models import EmployeeDesignation
from company.models import VehicleTypes, CompanyContactInfo, CompanyBranchInfo, CompanyDepartment, CompanySector, CompanyTypeOfBusiness


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

class GetVehiclelistSerializer(serializers.ModelSerializer):

    # vehicle_type = serializers.SerializerMethodField()
    # free_time_in_mins = serializers.SerializerMethodField()
    # free_time_in_mins_price = serializers.SerializerMethodField()
    # min_time_in_min = serializers.SerializerMethodField()
    # min_time_in_min_price = serializers.SerializerMethodField()
    # fixed_time_in_min = serializers.SerializerMethodField()
    # free_time_in_mins_price = serializers.SerializerMethodField()
    # fixed_time_in_min_price = serializers.SerializerMethodField()

    class Meta:
        model = VehicleTypes
        fields = ['id', 'vehicle_type' , 'free_time_in_mins', 'free_time_in_mins_price', 'min_time_in_min', 'min_time_in_min_price', 'fixed_time_in_min', 'fixed_time_in_min_price']

    # vehicle_type = serializers.CharField(required=True)
    # free_time_in_mins = serializers.CharField(required=False)
    # free_time_in_mins_price = serializers.CharField(required=False)
    # min_time_in_min = serializers.CharField(required=False)
    # min_time_in_min_price = serializers.CharField(required=True)
    # fixed_time_in_min = serializers.CharField(required=False)
    # fixed_time_in_min_price = serializers.CharField(required=False)
    
