from django.shortcuts import render
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
from .models import *
# from .request_serializer import AddBrandCategorySerializer, UpdateBrandServiceSerializer, UpdateBrandBranchServiceSerializer, AddBrandServiceSerializer, GetBrandCategoriesSerializer, GetBrandBranchCategoriesSerializer, GetBrandBranchServicesSerializer, GetPredefinedCategoriesSerializer, GetPredefinedFormFieldsSerializer, GetPredefinedServicesSerializer, SubmitBrandBranchCalendarWeekSerializer, SubmitBrandMasterUomSerializer, SubmitBrandServicesSerializer
from .response_serializer import *
# from .model_helper import create_brand_branch_service, get_brand_branch_service_categories, get_brand_branch_services, get_brand_service_types, get_service_master_uom_predefined_form_fields, get_service_predefined, get_service_predefined_category
import random
from authentication.custom_api_views import * 
# GenericAPIView, GenericListAPIView, GenericCrudApiView, GenericItemDetailApiView

from .models import *
from django.apps import apps
# from django.db.models import get_model
# get_paginated_results_set


# Create your views here.


class GetCourses(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer = None
    list_serializer = CourseListSerializer
    per_page_count = -1

    def get_list_query(self):
        return Course.objects.all()

class GetCourseSections(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer = None
    list_serializer = CourseSectionListSerializer
    per_page_count = 10
    search_contains=['name']

    def get_list_query(self):
        return CourseSection.objects.filter(course__id = self.payload['course_id']).order_by('order_sequence')


class GetCourseTopics(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer = None
    list_serializer = CourseTopicListSerializer
    per_page_count = 10
    

    def get_list_query(self):
        return Topic.objects.filter(course_section_id = self.payload['course_section_id']).order_by('order_sequence')



class GetCourseTopicDetails(GenericItemDetailApiView):
    
    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer =  None
    item_serializer = GetCourseTopicDetailsSerializer
    
    def get_item_query(self):
        return Topic.objects.get(id = self.payload['topic_id'])

class GetCourseTopicTasks(GenericListAPIView):
    
    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer = None
    list_serializer = GetCourseTopicTasksSerializer
    per_page_count = 10

    def get_list_query(self):
        return Task.objects.filter(topic__id = self.payload['topic_id']).order_by('order_sequence')


class GetTaskDetails(GenericItemDetailApiView):
    
    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer =  None
    item_serializer = GetTaskDetailsSerializer

    def get_item_query(self):
        return Task.objects.get(id = self.payload['task_id'])


# class GenericCRUD(GenericItemDetailApiView):
    
#     access_rights = GenericAPIView.ACCESS_TYPE_OPEN
#     request_serializer =  None
#     item_serializer = GetTaskDetailsSerializer

#     def get_item_query(self):
#         return Task.objects.get(id = self.payload['task_id'])


class GenericCRUD(GenericDynamicModelCrudApiView):

    authentication_classes = []
    permission_classes = []
    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer = None
    base_model = None

    def get_base_model(self):
        
        if self.base_model == None:            
            x = self.payload['mq'].split("__")
            app_name = x[0]
            model_name = x[1]
            model = apps.get_model(app_name, model_name)
            self.base_model = model

class GenericBatchCRUD(GenericDynamicModelBatchCrudApiView):

    authentication_classes = []
    permission_classes = []
    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer = None
    base_model = None

    def get_base_model(self):
        if self.base_model == None:            
            x = self.payload['mq'].split("__")
            app_name = x[0]
            model_name = x[1]
            model = apps.get_model(app_name, model_name)
            self.base_model = model



# class DynamicModelSerializer(serializers.ModelSerializer):
#     def __init__(self, *args, **kwargs):
#         fields = kwargs.pop('fields', None)
#         exclude = kwargs.pop('exclude', None)
#         super().__init__(*args, **kwargs)
#         if fields is not None:
#             allowed = set(fields)
#             existing = set(self.fields)
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)
#         if exclude is not None:
#             for field_name in exclude:
#                 self.fields.pop(field_name)

# class DynamicSerializerView(generics.GenericAPIView):
#     def get_serializer_class(self):
#         model = self.kwargs['model']
#         fields = self.kwargs['fields']
#         # Create a dynamic serializer class based on the model and fields
#         class DynamicSerializer(serializers.ModelSerializer):
#             class Meta:
#                 model = model
#                 fields = fields
#         return DynamicSerializer


class GenericDynamicListApi(GenericDynamicListAPIView):
    
    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer = None
    # list_serializer = GetCourseTopicTasksSerializer

    def get_list_query(self):
        x = self.payload['mq'].split("__")
        self.per_page_count = self.payload['pc']
        app_name = x[0]
        model_name = x[1]
        model = apps.get_model(app_name, model_name)
        qp = self.payload['qp']
        self.s_fields = self.payload['s_fields']
        self.base_model = model

        # self.list_serializer = DynamicSerializerView()
        return model.objects.filter(**qp)



class GenericAttachmentCRUD(GenericDynamicModelCrudApiView):
    
    authentication_classes = []
    permission_classes = []
    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer = None
    base_model = None

    def get_base_model(self):
        if self.base_model == None:            
            x = self.payload['mq'].split("__")
            app_name = x[0]
            model_name = x[1]
            model = apps.get_model(app_name, model_name)
            self.base_model = model


