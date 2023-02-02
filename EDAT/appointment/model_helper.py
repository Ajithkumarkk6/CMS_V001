from django.contrib.auth.models import User
from authentication.models import UserAuthentication
from rest_framework.authtoken.models import Token
from providerservice.models import BrandBranchCategory, BrandBranchServices, BrandCategory, ServiceMasterUomFormFieldServiceMapping, ServiceType, PredefinedCategory, PredefinedServices
from authentication.model_helper import create_update_model

def get_brand_service_types():
        return ServiceType.objects.filter(is_active = True)


def get_service_predefined_category(service_type_id):
        return PredefinedCategory.objects.filter(service_type__id = service_type_id, is_active = True)

def get_service_predefined(id):
        return PredefinedServices.objects.filter(category__id = id, is_active = True)

def get_service_master_uom_predefined_form_fields(service_type_id):
        return ServiceMasterUomFormFieldServiceMapping.objects.filter(service_type__id = service_type_id, is_active = True).order_by('display_order')


def get_brand_branch_service_categories(branch_id):
        print("branch_idbranch_id", branch_id)
        return BrandBranchCategory.objects.filter(brand_branch__id = branch_id, is_active=True)
        # .order_by('display_order')

def get_brand_branch_services(brand_meta_ids):
        return BrandBranchServices.objects.filter(brand_branch_category__id__in = brand_meta_ids, is_active = True)


def create_brand_branch_service(companyBranchInfo, brandServices, payload):

        brandBranchCategory = BrandBranchCategory.objects.get(brand_branch = companyBranchInfo, brand_category=brandServices.brand_category)

        brandBranchServicesForm = {}
        brandBranchServicesForm['brand_service'] = brandServices
        brandBranchServicesForm['brand_branch_category'] = brandBranchCategory
        brandBranchServicesForm['brand_branch'] = companyBranchInfo
        brandBranchServicesForm['is_active'] = True

        if brandServices.brand_category.is_independent_slot:
                brandBranchServicesForm['service_time'] =payload['service_time'] 
                brandBranchServicesForm['service_price'] = payload['service_price']
        
        brandBranchServicesForm['is_display'] = True
        brandBranchServicesForm['is_display_price'] = payload['is_display_price']

        create_update_model(model_class=BrandBranchServices, data=brandBranchServicesForm)