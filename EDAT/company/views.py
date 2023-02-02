from traceback import format_exception
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from company.model_helper import get_all_companies, get_all_branchs, get_brand_sectors, get_departments, get_type_of_business
from .request_serializer import AddFenceAdminSerializer, EnableBranchFenceSerializer, AddDepartmentSerializer, AddBranchSerializer, AddBranchLocationSerializer, GetStoreDetailsSerializer, UpdateBranchLocationSerializer
from company.models import CompanyBranchWeeklyCalendar, CompanyDepartment, CompanyMeta, CompanyContactInfo, CompanyBranchInfo, CompanyGeoLocationInfo
import random
from authentication.model_helper import get_attachment, get_user_from_request, get_user_company_from_request, check_if_exist
from company.response_serializer import CompanyMetaSerializer, CompanyTypeOfBusinessSerializer, CompanySectorSerializer, DepartmentDropdownSerializer, BranchListSerializer
from authentication.response_serializer import get_validation_failure_response, get_success_response
from employee.models import EmployeeCompanyInfo, EmployeePersonalInfo
from django.db.models import Q
import random
from authentication.custom_api_views import GenericAPIView, GenericListAPIView, GenericCrudApiView


class GetAllBranches(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        print("12345678", data)
        request_info = get_user_company_from_request(request)
        if request_info['company_info'] is not None:
            # and request_info['is_admin']
            branchQ = get_all_branchs(request_info['company_info'].company.id)
            if 'q' in data and branchQ.count() > 0:
                branchQ = branchQ.filter(Q(name__istartswith=data['q']) | Q(
                    display_name__icontains=data['q']))
            serializer = BranchListSerializer(branchQ, many=True)
            list_data = serializer.data
            res = get_success_response()
            res["details"] = list_data
            return Response(res)
        else:
            return Response(get_validation_failure_response(None, 'Invalid user'))


class GetDepartments(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        request_info = get_user_company_from_request(request)
        if request_info['company_info'] is not None:
            departmentsQ = get_departments(
                request_info['company_info'].company.id)

            if 'q' in data and departmentsQ.count() > 0:
                departmentsQ = departmentsQ.filter(name__icontains=data['q'])

                # departmentsQ = departmentsQ.filter(name__istartswith = data['q'])

            serializer = DepartmentDropdownSerializer(departmentsQ, many=True)
            res = get_success_response()
            res["details"] = serializer.data
            return Response(res)
        else:
            return Response(get_validation_failure_response(None, 'Invalid user'))


class GetBrandSectors(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        departmentsQ = get_brand_sectors()

        if 'q' in data and departmentsQ.count() > 0:
            departmentsQ = departmentsQ.filter(name__icontains=data['q'])

            # departmentsQ = departmentsQ.filter(name__istartswith = data['q'])

        serializer = CompanySectorSerializer(departmentsQ, many=True)
        res = get_success_response()
        res["details"] = serializer.data
        return Response(res)


class GetTypeOfBusiness(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        request_info = get_user_company_from_request(request)
        departmentsQ = get_type_of_business()

        print(departmentsQ.count())
        if 'q' in data and departmentsQ.count() > 0:
            departmentsQ = departmentsQ.filter(name__icontains=data['q'])

            # departmentsQ = departmentsQ.filter(name__istartswith = data['q'])

        serializer = CompanyTypeOfBusinessSerializer(departmentsQ, many=True)
        res = get_success_response()
        res["details"] = serializer.data
        return Response(res)


class AddDepartment(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        request_info = get_user_company_from_request(request)
        validation = AddDepartmentSerializer(data=data)
        if validation.is_valid() and request_info['company_info'] is not None and request_info['is_admin']:

            if CompanyBranchInfo.objects.get(id=request_info['company_branch']['id']).is_parent:
                if check_if_exist(CompanyDepartment, {"name": data['name'], "company": request_info['company_info'].company}) == False:
                    form_employee_designation = {}
                    form_employee_designation['name'] = data['name']
                    employeeDesignation = CompanyDepartment(**data)
                    employeeDesignation.company_branch = request_info['company_info'].company_branch
                    employeeDesignation.company = request_info['company_info'].company

                    tag = random.randint(100000, 999999)
                    employeeDesignation.tag = tag
                    employeeDesignation.save()

                    return Response(get_success_response("Department added successfully"))
                else:
                    return Response(get_validation_failure_response(None, "Department already exist"))
            else:
                return Response(get_validation_failure_response(None, "Please Contact Admin to Add Department"))
        else:
            return Response(get_validation_failure_response(validation.errors))


class UpdateBranchLocation(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):

        data = request.data
        user = get_user_company_from_request(request)
        validation = UpdateBranchLocationSerializer(data=data)
        if validation.is_valid() and user['company_info'] is not None:
            form_company_geolocation = {}
            form_company_geolocation = data

            try:
                company_geolocation = CompanyGeoLocationInfo.objects.get(
                    id=data['id'])

                response_message = "Branch Location Updated Successfully"

                if 'fencing_radius' in data:
                    response_message = "Fencing radius updated Successfully"

                serializer = UpdateBranchLocationSerializer(data=data)
                if serializer.is_valid():
                    serializer.update(company_geolocation, data)
                    return Response(get_success_response(response_message))
                else:
                    return Response(get_validation_failure_response(validation.errors))
            except:
                return Response(get_validation_failure_response(None, "Invalid Branch details"))
        else:
            return Response(get_validation_failure_response(validation.errors))


class AddBranchLocation(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):

        data = request.data
        user = get_user_company_from_request(request)
        validation = AddBranchLocationSerializer(data=data)
        if validation.is_valid() and user['company_info'] is not None:

            if user['company_info'].company_branch.company_geolocation is None:

                form_company_geolocation = {}
                form_company_geolocation = data
                company_geolocation = CompanyGeoLocationInfo(
                    **form_company_geolocation, is_active=True)
                company_geolocation.save()

                company_branch = user['company_info'].company_branch
                company_branch.company_geolocation_id = company_geolocation.id
                company_branch.can_update_location = False
                company_branch.save()

                return Response(get_success_response("Branch Location Created Successfully"))
            else:
                print("datadata")
                print(data)
                company_branch = user['company_info'].company_branch
                company_branch.can_update_location = False
                company_branch.save()
                company_geolocation = user['company_info'].company_branch.company_geolocation
                company_geolocation.location_latitude = data['location_latitude']
                company_geolocation.location_longitude = data['location_longitude']
                company_geolocation.save()
                return Response(get_success_response("Branch Location Updated Successfully"))

        else:
            print(validation.errors)
            return Response(get_validation_failure_response(validation.errors))


class Index(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        res = {}
        res["success"] = False
        res["details"] = "Bad Request"
        return HttpResponse(res)

    def get(self, request, format=None):
        res = {}
        res["success"] = False
        res["details"] = "Bad Request"
        return HttpResponse(res)


class AddBranch(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):

        data = request.data
        request_info = get_user_company_from_request(request)
        validation = AddBranchSerializer(data=data)
        print(data)
        if validation.is_valid() and request_info['company_info'] is not None:
            if check_if_exist(CompanyBranchInfo, {"name": data['name'], "company": request_info['company_info'].company}) == False:
                # adding company contact
                form_company_contact = {}
                form_company_contact['is_default'] = False
                form_company_contact['communication_address'] = data['communication_address']
                form_company_contact['billing_address'] = data['communication_address']
                form_company_contact['pincode'] = data['pincode']
                form_company_contact['country'] = 'IN'

                company_contact = CompanyContactInfo.objects.create(
                    **form_company_contact)

                # adding company branch
                form_company_branch = {}
                form_company_branch['name'] = data['name']
                form_company_branch['display_name'] = data['display_name']
                form_company_branch['is_parent'] = False
                form_company_branch['is_active'] = True

                company_branch = CompanyBranchInfo(
                    company_contact=company_contact, **form_company_branch)
                company_branch.company = request_info['company_info'].company
                company_branch.parent_id = data['parent']
                company_branch.save()
                response = get_success_response("Branch Created Successfully")
                print(response)
                return Response(response)
            else:
                return Response(get_validation_failure_response(None, "Branch already exist"))
        else:
            response = get_validation_failure_response(validation.errors)
            print(response)
            return Response(response)


class GetCustomerHomeContent(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        response_data = {}

        response_data['base_content'] = {'footer': [{'order': 1, 'text': 'Products'}, {
            'order': 2, 'text': 'Bookings'}, {'order': 3, 'text': 'Store'}]}
        return Response(get_success_response(message=None, details=response_data))


class GetStoreDetails(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        request_info = get_user_company_from_request(request)
        validation = GetStoreDetailsSerializer(data=data)
        print(data)
        if validation.is_valid() and request_info['company_info'] is not None:

            response_data = {}

            week_days = []

            companyContactInfo = CompanyBranchInfo.objects.get(
                id=data['branch_id'])

            companyBranchWeeklyCalendar = CompanyBranchWeeklyCalendar.objects.filter(
                company_branch__id=data['branch_id']).first()

            week_days.append({"day": 1, "is_working": companyBranchWeeklyCalendar.day_mon.is_working,
                             "start_time": companyBranchWeeklyCalendar.day_mon.start_time, "end_time": companyBranchWeeklyCalendar.day_mon.end_time})
            week_days.append({"day": 2, "is_working": companyBranchWeeklyCalendar.day_tue.is_working,
                             "start_time": companyBranchWeeklyCalendar.day_tue.start_time, "end_time": companyBranchWeeklyCalendar.day_tue.end_time})
            week_days.append({"day": 3, "is_working": companyBranchWeeklyCalendar.day_wed.is_working,
                             "start_time": companyBranchWeeklyCalendar.day_wed.start_time, "end_time": companyBranchWeeklyCalendar.day_wed.end_time})
            week_days.append({"day": 4, "is_working": companyBranchWeeklyCalendar.day_thu.is_working,
                             "start_time": companyBranchWeeklyCalendar.day_thu.start_time, "end_time": companyBranchWeeklyCalendar.day_thu.end_time})
            week_days.append({"day": 5, "is_working": companyBranchWeeklyCalendar.day_fri.is_working,
                             "start_time": companyBranchWeeklyCalendar.day_fri.start_time, "end_time": companyBranchWeeklyCalendar.day_fri.end_time})
            week_days.append({"day": 6, "is_working": companyBranchWeeklyCalendar.day_sat.is_working,
                             "start_time": companyBranchWeeklyCalendar.day_sat.start_time, "end_time": companyBranchWeeklyCalendar.day_sat.end_time})
            week_days.append({"day": 7, "is_working": companyBranchWeeklyCalendar.day_sun.is_working,
                             "start_time": companyBranchWeeklyCalendar.day_sun.start_time, "end_time": companyBranchWeeklyCalendar.day_sun.end_time})

            response_data['week_days'] = week_days
            response_data['address_details'] = {
                "name": companyContactInfo.company_contact.communication_address, "place_id": companyContactInfo.company_contact.google_place_link}

            contact_number = []
            contact_number.append(
                companyContactInfo.company_contact.mobile_number_01)

            if companyContactInfo.company_contact.mobile_number_02 is not None:
                contact_number.append(
                    companyContactInfo.company_contact.mobile_number_02)

            response_data['contact_number'] = contact_number

            return Response(get_success_response(message=None, details=response_data))
        else:
            return Response(get_validation_failure_response(validation.errors, "Invalid Request"))


# ====================================

class GetAssociatedCompanies(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_OPEN
    request_serializer = None
    list_serializer = CompanyMetaSerializer
    per_page_count = 10

    def get_list_query(self):
        return get_all_companies()
        

class GetTaskDetails(APIView):
    
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = {
        "tasks": [
            {
                "question": "Aravind goes to nearby hotel got buy dinner for him, where first he checks whether the hotel have both idli and sambar and there are atleast 5 idlys available then buys idli and samber for him if both are available. if either idli or sambar is not available, then he checks if dosa and chuttny are available and checks if atlease 2 dosa is there, if available then he buys dosa and chuttny, if chuttny or dosa is not available then he gets back without purchasing anything",
                "sample_io": [
                    {
                        "i": [
                            {
                                "idly_available": "True"
                            },
                            {
                                "sambar_available": "False"
                            },
                            {
                                "dosa_available": "True"
                            }
                        ],
                        "o": [
                            "purchase idly sambar",
                            "purchase idly sambar"
                        ]
                    }
                ],
                "rules": [
                    {
                        "title": "Get Age of the person",
                        "child": [
                            {
                                "title": "Get Age of the person",
                                "child2:": [
                                    {
                                        "title": "Get Age of the person",
                                        "child": []
                                    },
                                    {
                                        "title": "Get Name of the person",
                                        "child": []
                                    }
                                ]
                            },
                            {
                                "title": "Get Name of the person",
                                "child": []
                            }
                        ]
                    },
                    {
                        "title": "Get Name of the person",
                        "child": []
                    }
                ]
            }
        ]
    }        

        return Response(get_success_response(message=None, details=data))
