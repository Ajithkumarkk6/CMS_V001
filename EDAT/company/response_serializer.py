from rest_framework import serializers
from employee.models import EmployeeDesignation
from company.models import CompanyMeta, CompanyContactInfo, CompanyBranchInfo, CompanyDepartment, CompanySector, CompanyTypeOfBusiness
from employee.models import EmployeeCompanyInfo, EmployeePersonalInfo


class CompanyMetaSerializer(serializers.ModelSerializer):

    phone = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    sector = serializers.SerializerMethodField()
    branch_id = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    def get_default_branch(self, obj):
        return CompanyBranchInfo.objects.filter(
            company=obj).first()

    class Meta:
        model = CompanyMeta
        fields = ['id', 'branch_id', 'display_name',
                  'phone', 'email', 'sector', 'address', 'logo']

    def get_phone(self, obj):
        employeeCompanyInfo = EmployeeCompanyInfo.objects.filter(
            company=obj, authentication__is_admin=True).first()
        return EmployeePersonalInfo.objects.get(user=employeeCompanyInfo.user).mobile_number

    def get_email(self, obj):
        employeeCompanyInfo = EmployeeCompanyInfo.objects.filter(
            company=obj, authentication__is_admin=True).first()
        return employeeCompanyInfo.user.email
        # return EmployeePersonalInfo.objects.get(user=employeeCompanyInfo.user).

    def get_sector(self, obj):
        return obj.sector.name

    def get_branch_id(self, obj):
        return self.get_default_branch(obj).id

    def get_address(self, obj):

        companyBranchInfo = CompanyBranchInfo.objects.get(
            company=obj, is_parent=True).company_contact
        return str(companyBranchInfo.communication_address) + ',' + str(companyBranchInfo.pincode)

    def get_logo(self, obj):
        return 'https://media.licdn.com/dms/image/C560BAQEdTW1Tn0GM1w/company-logo_200_200/0/1592264836081?e=2147483647&v=beta&t=pQtc-OvqfF48rTvMMXpbkiZbXh5zdboY16IbJ-Ck204'


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
        fields = ['id', 'name']


class BranchListSerializer(serializers.ModelSerializer):
    parent_id = serializers.SerializerMethodField()
    has_location = serializers.SerializerMethodField()
    geo_location_id = serializers.SerializerMethodField()
    fencing_radius = serializers.SerializerMethodField()

    class Meta:
        model = CompanyBranchInfo
        fields = ['id', 'name', 'parent_id', 'has_location',
                  'fencing_radius', 'can_update_location', 'geo_location_id']

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
