from django.shortcuts import render
from mmap import PAGESIZE
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from authentication.model_helper import create_update_model_response, create_update_model, check_if_exist, ValidateRequest, get_paginated_results_set, get_user_company_from_request
from authentication.response_serializer import get_validation_failure_response, get_success_response
from company.models import CompanyBranchInfo, CompanyBranchWeeklyCalendar, CompanyMeta, WeekDay
from providerservice.models import BrandBranchCategory, BrandBranchServices, BrandCategory, BrandServiceMasterUomFormField, BrandServiceMasterUomFormFieldServiceMapping, BrandServices, FormFieldType, PredefinedCategory, PredefinedServices, ServiceType
from providerservice.request_serializer import AddBrandCategorySerializer,UpdateBrandServiceSerializer, UpdateBrandBranchServiceSerializer, AddBrandServiceSerializer, GetBrandBranchCategoriesSerializer, GetBrandBranchServicesSerializer, GetPredefinedCategoriesSerializer, GetPredefinedFormFieldsSerializer, GetPredefinedServicesSerializer, SubmitBrandBranchCalendarWeekSerializer, SubmitBrandMasterUomSerializer, SubmitBrandServicesSerializer
from providerservice.response_serializer import BrandBranchCategorySerializer, BrandBranchServicesSerializer, ServiceMasterUomFormFieldServiceMappingSerializer, ServiceTypeSerializer, PredefinedCategorySerializer, PredefinedProductSerializer
from .model_helper import create_brand_branch_service, get_brand_branch_service_categories, get_brand_branch_services, get_brand_service_types, get_service_master_uom_predefined_form_fields, get_service_predefined, get_service_predefined_category
import random
from authentication.custom_api_views import GenericAPIView, GenericListAPIView, GenericCrudApiView
# get_paginated_results_set

class Index(APIView):
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        return Response(get_success_response(None, None, {}))

class GetSectorServiceTypes(GenericAPIView):
    
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data

        return Response(get_success_response(message=None, details=serializer.data))

