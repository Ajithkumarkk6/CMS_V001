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
from providerservice.request_serializer import AddBrandCategorySerializer,UpdateBrandServiceSerializer, UpdateBrandBranchServiceSerializer, AddBrandServiceSerializer, GetBrandCategoriesSerializer, GetBrandBranchCategoriesSerializer, GetBrandBranchServicesSerializer, GetPredefinedCategoriesSerializer, GetPredefinedFormFieldsSerializer, GetPredefinedServicesSerializer, SubmitBrandBranchCalendarWeekSerializer, SubmitBrandMasterUomSerializer, SubmitBrandServicesSerializer
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

class GetSectorServiceTypes(GenericListAPIView):
    
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        serviceTypes = get_brand_service_types()
        
        if 'q' in data and serviceTypes.count()>0:
            serviceTypes = serviceTypes.filter(name__icontains = data['q'])

        serializer = ServiceTypeSerializer(serviceTypes, many=True)

        return Response(get_success_response(message=None, details=serializer.data))

class AddBrandCategory(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data        

        validateRequest  = ValidateRequest(request=request, request_serializer=AddBrandCategorySerializer)
        if not validateRequest.is_admin():
            return Response(get_validation_failure_response(None, validateRequest.errors_formatted()))

        employeeCompanyInfo = validateRequest.employee_company_info()


        if 'id' in data:
            update_model_response = create_update_model(BrandCategory, data, unique_fields=['name'], unique_q_extra_pram={"brand__id":employeeCompanyInfo.company.id})
            if update_model_response['status'] == True:
                    return Response(get_success_response(message="Category Details Updated Successfully"))
            else:
                return Response(get_validation_failure_response(None,error_message = update_model_response['error'] ))

                # return Response(get_validation_failure_response(None,error_message="Category details not updated" ))
                    
        q =  {"name":data['name']}        
        if (check_if_exist(BrandCategory, q)) == True: 
            return  Response(get_validation_failure_response(None,error_message="Category with name exist already " ))

        '''
        creating brand category
        '''
        brandCategoryForm = {}

        brandCategoryForm['brand_id'] = employeeCompanyInfo.company.id
        brandCategoryForm['name'] = data['name']
        brandCategoryForm['description'] = data['description']
        brandCategoryForm['is_parent'] = data['is_parent']
        brandCategoryForm['description'] = data['description']
        brandCategoryForm['is_active'] = True

        is_independent_slot = data['is_independent_slot']
        
        if 'parent_id' in data and data['parent_id'] is not None:
            parentBrandCategory = BrandCategory.objects.get(id=data['parent_id'])
            is_independent_slot = parentBrandCategory.is_independent_slot
            brandCategoryForm['parent'] = parentBrandCategory
            brandCategoryForm['is_parent'] = False

        brandCategoryForm['code'] = random.randint(1000,9999)

        if is_independent_slot == False:
            brandCategoryForm['service_time'] = data['service_time'] 
            brandCategoryForm['service_price'] = data['service_price']
        
        brandCategory = BrandCategory.objects.create(**brandCategoryForm)


        '''
        creating brand branch category
        '''
        companyBranchInfos = CompanyBranchInfo.objects.filter(company = employeeCompanyInfo.company)
        
        for companyBranchInfo in companyBranchInfos:

            brandBranchCategoryForm = {}

            brandBranchCategoryForm['display_name'] = brandBranchCategoryForm['name'] = data['name']
            brandBranchCategoryForm['description'] = data['description']
            brandBranchCategoryForm['code'] = random.randint(1000,9999)
            brandBranchCategoryForm['brand_branch'] = companyBranchInfo
            brandBranchCategoryForm['is_active'] = True
            brandBranchCategoryForm['brand_category'] = brandCategory
            
            if brandCategory.is_independent_slot == False:
                brandBranchCategoryForm['service_time'] = data['service_time'] 
                brandBranchCategoryForm['service_price'] = data['service_price']
            brandBranchCategory = BrandBranchCategory.objects.create(**brandBranchCategoryForm)

        return Response(get_success_response(message="Category created successfully", ))


class AddBrandService(GenericAPIView):

    authentication_classes = []
    permission_classes = []
    access_rights = GenericAPIView.ACCESS_TYPE_ADMIN
    request_serializer =  AddBrandServiceSerializer

    def proceed_post(self, request):

        employeeCompanyInfo = self.get_employee_company_info()

        '''
        creating brand service
        '''
        brandServiceForm = {}

        brandServiceForm['brand_id'] = employeeCompanyInfo.company.id
        brandServiceForm['display_name'] = brandServiceForm['name'] = self.payload['name']

        brandCategory = BrandCategory.objects.get(id=self.payload['category_id'])
        
        brandServiceForm['brand_category'] = brandCategory
        brandServiceForm['code'] = random.randint(1000,9999)

        if brandCategory.is_independent_slot:
            brandServiceForm['service_time'] = self.payload['service_time'] 
            brandServiceForm['service_price'] = self.payload['service_price']
        
        brandServiceForm['is_display'] = True
        brandServiceForm['is_display_price'] = self.payload['is_display_price']

        brandServices = create_update_model(model_class=BrandServices, data=brandServiceForm)

        '''
        creating brand branch service
        '''

        # employeeCompanyInfo.company
        companyBranchInfos = CompanyBranchInfo.objects.filter(company = employeeCompanyInfo.company)
        
        for companyBranchInfo in companyBranchInfos:

            create_brand_branch_service_payload = {}
            if brandCategory.is_independent_slot:
                create_brand_branch_service_payload['service_time'] = self.payload['service_time'] 
                create_brand_branch_service_payload['service_price'] = self.payload['service_price']
            create_brand_branch_service_payload['is_display_price'] = self.payload['is_display_price']

            create_brand_branch_service(companyBranchInfo, brandServices, create_brand_branch_service_payload)

        return Response(get_success_response(message=None, ))

class UpdateBrandBranchService(GenericCrudApiView):
    
    authentication_classes = []
    permission_classes = []
    access_rights = GenericAPIView.ACCESS_TYPE_ADMIN
    request_serializer =  UpdateBrandBranchServiceSerializer
    base_model = BrandBranchServices

class UpdateBrandService(GenericCrudApiView):
    
    authentication_classes = []
    permission_classes = []
    access_rights = GenericAPIView.ACCESS_TYPE_ADMIN
    request_serializer =  UpdateBrandServiceSerializer
    base_model = BrandServices



class GetPredefinedCategories(GenericListAPIView):
    
    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer =  None
    list_serializer = PredefinedCategorySerializer

    def get_list_query(self):
            return get_service_predefined_category(self.payload['service_type_id'])

class GetMasterUomPredefinedFormFields(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer =  None
    list_serializer = ServiceMasterUomFormFieldServiceMappingSerializer

    def get_list_query(self):
            return get_service_master_uom_predefined_form_fields(self.payload['service_type_id'])

class GetPredefinedServices(APIView):
    
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        
        validation = GetPredefinedServicesSerializer(data=data)
        if validation.is_valid():
            service_ids = data['service_ids']
            response_data = []     
            for service_id in service_ids:
                predefinedCategorys = get_service_predefined(service_id)
                serializer = PredefinedProductSerializer(predefinedCategorys, many=True)
                response_data.append({"id":service_id, "data":serializer.data})
            return Response(get_success_response(message=None, details=response_data))

        return Response(get_validation_failure_response(validation.errors, "Invalid Request"))


class SubmitBrandMasterUom(APIView):
    
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        response_data = {}
        validation = SubmitBrandMasterUomSerializer(data=data)
        
        if validation.is_valid():
            companyMeta = CompanyMeta.objects.get(id= data['brand_id'])

            for uom in data['uoms']:
                uom
                brandServiceMasterUomFormFieldForm = {}
                if 'reference_id' in uom:
                    brandServiceMasterUomFormFieldForm['meta_reference_id'] = uom['reference_id']
   
                brandServiceMasterUomFormFieldForm['brand'] = companyMeta
                brandServiceMasterUomFormFieldForm['name'] = uom['uom_name']
                brandServiceMasterUomFormFieldForm['is_display'] = uom['is_display']
                brandServiceMasterUomFormFieldForm['is_manditory'] = uom['is_manditory']
                brandServiceMasterUomFormFieldForm['support_data'] = uom['uom_support_data']
                try:                    
                    brandServiceMasterUomFormFieldForm['field_type'] = FormFieldType.objects.get(tag = uom['uom_field_type']) 
                except:
                    brandServiceMasterUomFormFieldForm['field_type'] = FormFieldType.objects.get(tag = 'TEXT') 

                brandServiceMasterUomFormFieldForm['is_display'] = uom['is_display']
                brandServiceMasterUomFormField = BrandServiceMasterUomFormField.objects.create(**brandServiceMasterUomFormFieldForm)

                brandServiceMasterUomFormFieldServiceMappingForm = {}
                brandServiceMasterUomFormFieldServiceMappingForm['display_order'] = uom['display_order']
                brandServiceMasterUomFormFieldServiceMappingForm['master_uom'] = brandServiceMasterUomFormField
                brandServiceMasterUomFormFieldForm['brand'] = companyMeta
                
                BrandServiceMasterUomFormFieldServiceMapping.objects.create(**brandServiceMasterUomFormFieldServiceMappingForm)
            return Response(get_success_response(message=None, details={"UOM added successfully"}))

        else:
            return Response(get_validation_failure_response(validation.errors, "Invalid Request"))




class SubmitBrandServices(APIView):
    
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        response_data = {}
        validation = SubmitBrandServicesSerializer(data=data)
        print("datadatadatadata", data)
        if validation.is_valid():
            companyMeta = CompanyMeta.objects.get(id= data['brand_id'])
            serviceType = ServiceType.objects.get(id=data['service_type_id'])
            companyBranchInfo = CompanyBranchInfo.objects.filter(company= companyMeta).first()

            if 'place_id' in data:
                companyBranchInfo.company_contact.google_place_link = data['place_id'] 
                companyBranchInfo.save()

            service_categorys = data['service_category']
            
            brand_branch_category_mapping_ids = []

            ''' adding parent service categories '''
            for service_category in service_categorys:
                if service_category['is_parent'] == True:
                    brandCategoryForm = {}

                    if 'reference_id' in service_category:
                        try:
                            predefinedCategory = PredefinedCategory(id = service_category['reference_id'])
                            brandCategoryForm['meta_reference'] = predefinedCategory 
                        except:
                            pass

                    brandCategoryForm['id'] = service_category['id']
                    brandCategoryForm['display_name'] = brandCategoryForm['name'] = service_category['name']
                    brandCategoryForm['brand'] = companyMeta
                    brandCategoryForm['is_parent'] = True
                    brandCategoryForm['is_independent_slot'] = service_category['is_independent_slot']
                    brandCategoryForm['service_type'] = serviceType

                    if brandCategoryForm['is_independent_slot'] == False:
                        brandCategoryForm['service_time'] = service_category['service_time']
                        brandCategoryForm['service_price'] = service_category['service_price']

                    brandCategory = BrandCategory.objects.create(**brandCategoryForm)
                    brandCategoryForm['brand_category'] = brandCategory                    
                    del brandCategoryForm['brand']
                    del brandCategoryForm['service_type']
                    del brandCategoryForm['is_parent']
                    del brandCategoryForm['is_independent_slot']

                    
                    if 'meta_reference' in brandCategoryForm: 
                        del brandCategoryForm['meta_reference']

                    if 'id' in brandCategoryForm: 
                        del brandCategoryForm['id']

                    # brand_branch_category_ids = 
                    brandBranchCategory = BrandBranchCategory.objects.create(**brandCategoryForm)
                    brand_branch_category_mapping_ids.append({"brand_category_id":brandCategory.id,"brand_branch_category_id": brandBranchCategory.id})

            ''' adding child service categories '''
            for service_category in service_categorys:
                if service_category['is_parent'] == False:
                    brandCategoryForm = {}

                    if 'reference_id' in service_category:
                        try:
                            predefinedCategory = PredefinedCategory(id = service_category['reference_id'])
                            brandCategoryForm['meta_reference'] = predefinedCategory 
                        except:
                            pass

                    brandCategoryForm['id'] = service_category['id']
                    brandCategoryForm['display_name'] = brandCategoryForm['name'] = service_category['name']
                    brandCategoryForm['brand'] = companyMeta
                    brandCategoryForm['is_parent'] = False

                    parentBrandCategory = BrandCategory.objects.get(id=service_category['parent_id'])
                    brandCategoryForm['parent'] = parentBrandCategory

                    brandCategoryForm['is_independent_slot'] = parentBrandCategory.is_independent_slot
                    brandCategoryForm['service_type'] = serviceType

                    if brandCategoryForm['is_independent_slot'] == False:
                        brandCategoryForm['service_time'] = service_category['service_time']
                        brandCategoryForm['service_price'] = service_category['service_price']

                    brandCategory = BrandCategory.objects.create(**brandCategoryForm)                    
                    brandCategoryForm['brand_category'] = brandCategory        
                    del brandCategoryForm['brand']
                    del brandCategoryForm['service_type']
                    del brandCategoryForm['is_parent']
                    del brandCategoryForm['is_independent_slot']
                    del brandCategoryForm['parent']

                    if 'meta_reference' in brandCategoryForm: 
                        del brandCategoryForm['meta_reference']

                    if 'id' in brandCategoryForm: 
                        del brandCategoryForm['id']

                    brandCategoryForm['brand_branch'] = companyBranchInfo 
                    brandBranchCategory = BrandBranchCategory.objects.create(**brandCategoryForm)
                    brand_branch_category_mapping_ids.append({"brand_category_id":brandCategory.id,"brand_branch_category_id": brandBranchCategory.id})


            ''' adding brand services '''


            brand_services = data['service']

            for brand_service in brand_services:
                
                brandServicesForm = {}
                if 'reference_id' in brand_service:
                    try:
                        predefinedServices = PredefinedServices(id = brand_service['reference_id'])
                        brandServicesForm['meta_reference'] = predefinedServices 
                    except:
                        pass

                # brandServicesForm['display_order'] = brand_service['display_order'] 
                brandServicesForm['name'] = brandServicesForm['display_name'] = brand_service['name'] 
                brandServicesForm['service_time'] = brand_service['service_time'] 
                brandServicesForm['service_price'] = brand_service['service_price'] 
                brandServicesForm['is_display_price'] = brand_service['is_display_price'] 
                brandServicesForm['is_display'] = True 
                brandServicesForm['service_type'] = serviceType
                brandServicesForm['brand'] = companyMeta
                brandServicesForm['brand_category_id'] = brand_service['service_category_id']
                    
                brandServices = BrandServices.objects.create(**brandServicesForm)
                brandServicesForm['brand_service'] = brandServices
                del brandServicesForm['brand']
                del brandServicesForm['service_type']
                del brandServicesForm['brand_category_id']
                if 'meta_reference' in brandServicesForm: 
                    del brandServicesForm['meta_reference']
                if 'id' in brandCategoryForm: 
                    del brandCategoryForm['id']

                # brand_branch_category_mapping_ids.append({"brand_category_id":brandCategory.id,"brand_branch_category_id": brandBranchCategory.id})

                for brand_branch_category_mapping_id in brand_branch_category_mapping_ids:
                    if brand_branch_category_mapping_id['brand_category_id'] == brand_service['service_category_id']:
                        brandServicesForm['brand_branch_category_id'] = brand_branch_category_mapping_id['brand_branch_category_id']

                BrandBranchServices.objects.create(**brandServicesForm)
                return Response(get_success_response(message="Details added succesfully", details=[]))



        # else:
        return Response(get_validation_failure_response(validation.errors, "Invalid Request"))




class SubmitBrandBranchCalendarWeek(APIView):
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data

        print("reached----------------------", data)        
        validation = SubmitBrandBranchCalendarWeekSerializer(data=data)
        request_info = get_user_company_from_request(request)

        print("request_inforequest_info", request_info)

        if validation.is_valid():
            

            companyBranchWeeklyCalendarForm = {}
            companyBranchWeeklyCalendarForm

            def createWeekDay(obj_data):
                week_calendar_data = obj_data
                del week_calendar_data['day']
                weekDay = WeekDay.objects.create(**week_calendar_data)
                return weekDay


            for week_calendar in data['week_calendar']:
                if week_calendar['day'] == 1:
                    companyBranchWeeklyCalendarForm['day_mon'] = createWeekDay(week_calendar)
                elif week_calendar['day'] == 2:
                    companyBranchWeeklyCalendarForm['day_tue'] = createWeekDay(week_calendar)
                elif week_calendar['day'] == 3:
                    companyBranchWeeklyCalendarForm['day_wed'] = createWeekDay(week_calendar)
                elif week_calendar['day'] == 4:
                    companyBranchWeeklyCalendarForm['day_thu'] = createWeekDay(week_calendar)
                elif week_calendar['day'] == 5:
                    companyBranchWeeklyCalendarForm['day_fri'] = createWeekDay(week_calendar)
                elif week_calendar['day'] == 6:
                    companyBranchWeeklyCalendarForm['day_sat'] = createWeekDay(week_calendar)
                elif week_calendar['day'] == 7:
                    companyBranchWeeklyCalendarForm['day_sun'] = createWeekDay(week_calendar)

            companyBranchWeeklyCalendarForm['company_branch_id'] = request_info['company_branch']['id']
            CompanyBranchWeeklyCalendar.objects.create(**companyBranchWeeklyCalendarForm)

            return Response(get_success_response(message=None, details={}))
        else:
            return Response(get_validation_failure_response(validation.errors, "Invalid Request"))




class GetBrandCategories(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer =  GetBrandCategoriesSerializer
    list_serializer = BrandBranchCategorySerializer
    per_page_count = 10

    def get_list_query(self):
        return get_brand_branch_service_categories(self.payload['branch_id'])



class GetBrandBranchCategories(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer =  GetBrandBranchCategoriesSerializer
    list_serializer = BrandBranchCategorySerializer
    per_page_count = 10

    def get_list_query(self):
        return get_brand_branch_service_categories(self.payload['branch_id'])
        
class GetBrandBranchCategories(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer =  GetBrandBranchCategoriesSerializer
    list_serializer = BrandBranchCategorySerializer
    per_page_count = 10

    def get_list_query(self):
        return get_brand_branch_service_categories(self.payload['branch_id'])

class GetBrandBranchServices(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer =  GetBrandBranchServicesSerializer
    list_serializer = BrandBranchServicesSerializer
    per_page_count = 10

    def get_list_query(self):
        return get_brand_branch_services(self.payload['brand_meta_ids'])
