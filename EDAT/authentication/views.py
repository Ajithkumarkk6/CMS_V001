import csv
import os
import random
from datetime import datetime
from traceback import format_exception

import pytz
from authentication.conversion_utils import get_email_from_user_name
from company.models import (CompanyBranchInfo, CompanyContactInfo,
                            CompanyDepartment, CompanyGeoLocationInfo,
                            CompanyMeta)
from django.contrib.auth.models import User
# import StringIO
# import xlsxwriter
from django.http import HttpResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.utils import timezone
from employee.models import (EmployeeCompanyInfo, EmployeeDesignation,
                             EmployeeFinancialInfo, EmployeePersonalInfo)
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from quantatm import settings

from authentication.date_utils import get_current_time_aware, get_start_end_date_today
from authentication.message_utils import (send_company_login_OTP,
                                          send_company_registration_OTP,
                                          send_company_registration_successful,
                                          send_employee_registration)
from authentication.model_helper import (check_if_exist, get_attachment,
                                         get_user_company_from_request,
                                         get_user_from_request)
from authentication.models import AppBaseConfig, UserAuthentication, UserCredentialValidation
from authentication.utils import get_current_start_end_time

from .constants import (DEFAULT_DESIGNATIONS, DEFAULT_RADIUS,
                        REGISTATION_REGISTER_COMPANY)
from .form_serializer import (CompanyBranchInfoSerializer,
                              CompanyContactInfoSerializer,
                              CompanyMetaSerializer,
                              EmployeePersonalInfoSerializer)
from .model_helper import (ValidateRequest, get_active_user, get_user_by_id,
                           get_user_company_from_request,
                           get_user_company_from_user, get_user_from_request,
                           get_user_token, getuser_by_email, getuser_by_mobile,
                           getuser_from_params, set_mobile_otp, set_mobile_otp_registation, set_mobile_otp_registation_customer,
                           username_exists)
from .request_serializer import (GetBusinessPlaceDetailsSerializer, GetBusinessPlacesSerializer, OtpLoginSerializer, OtpRegisterSerializer, RegisterCompanySerializer, RegisterCustomerSerializer,
                                 RegisterUserSerializer,
                                 ResetPasswordSerializer,
                                 SubmitRegistationOtpSerializer,
                                 ValidateResendOtpSerializer,
                                 ValidateUserEmailSerializer,
                                 ValidateUserMobileSerializer,
                                 ValidateUserSerializer,
                                 AttachUserAccountsSerializer)
from .response_serializer import (get_success_response,
                                  get_validation_failure_response)

from ticket.models import Ticket
import requests
from requests.exceptions import HTTPError
import json


# import io
# import xlsxwriter

# http://localhost:8001/authentication/uploadRdwds


class DeleteUserPage(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):

        data = request.query_params

        if 'mobile' in data:
            user = getuser_by_mobile(data['mobile'])
            if user is not None:
                print(user.first_name)
                user.delete()
                return Response({"Status": str(user.first_name) + ' deleted successfully'})
            else:
                return Response({"Status": 'User Not Exist'})
        return Response({"Status": 'Mobile Number field missing'})


class DeleteCompany(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        company_id = "8d70dce5-30ab-4a02-ad02-ebeae4c23175"
        employeeCompanyInfos = EmployeeCompanyInfo.objects.filter(
            company__id=company_id)
        for e in employeeCompanyInfos:
            e.user.delete()
        companyMeta = CompanyMeta.objects.get(id=company_id)
        companyMeta.delete()
        return Response({"token": ''})


class GetToken(APIView):
    authentication_classes = []
    permission_classes = []

    # authentication_classes = [authentication.TokenAuthentication]
    def post(self, request):
        # send_company_registration_successful("Azhar", "+919080349072")
        # send_company_registration_OTP("Azhar", "+919080349072", 1234)
        send_company_login_OTP("Azhar", "9080349072", '1234')
        return Response({"token": get_user_token(request.data['username'])})


class Test(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        return Response({"success": True})

class RegisterAdmin(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        print(data)

        validateRequest = ValidateRequest(
            request=request, request_serializer=RegisterUserSerializer)
        if not validateRequest.is_valid_open_request():
            return Response(get_validation_failure_response(None, validateRequest.errors_formatted()))

        validation = RegisterUserSerializer(data=request.data)
        if validation.is_valid():

            if username_exists(data['email']):
                return Response(get_validation_failure_response(validation.errors, 'User with email already exist'))

            validation = EmployeePersonalInfoSerializer(data=request.data)

            '''check if user with same mobile already exist'''
            if validation.is_valid() == False:
                return Response(get_validation_failure_response(validation.errors, 'User with mobile number already exist'))

            # if EmployeePersonalInfo.objects.filter(mobile_number=data['mobile_number']).count()>0:
            #     return Response(get_validation_failure_response(validation.errors, 'User with mobile number already exist'))

            user = User(
                username=data['email'], email=data['email'], password=data['email']+'@123')
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()

            data_employee = {}
            data_employee['gender'] = data['gender']
            data_employee['mobile_number'] = data['mobile_number']

            employeePersonalInfo = EmployeePersonalInfo.objects.create(
                user=user, **data_employee)
            employeePersonalInfo.save()

            userAuthentication = UserAuthentication.objects.create(user=user)
            userAuthentication.admin_registration_designation = "Business Owner"
            #  data['designation']
            userAuthentication.is_admin = True
            userAuthentication.is_active = True
            userAuthentication.save()

            set_mobile_otp(userAuthentication, is_login=False)

            token = get_user_token(user.username)
            response = {"success": True, "token": token,
                        "message": "Admin registered Successfully"}

            return Response(get_success_response("Admin registered Successfully", details=response))
        else:
            print("validationvalidation02")
            print("validationvalidation", validation.errors)
            return Response(get_validation_failure_response(validation.errors))


class RegisterCustomer(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        print(data)

        validateRequest = ValidateRequest(
            request=request, request_serializer=RegisterCustomerSerializer)
        if not validateRequest.is_valid_open_request():
            return Response(get_validation_failure_response(None, validateRequest.errors_formatted()))

        validation = RegisterCustomerSerializer(data=request.data)
        if validation.is_valid():

            # if username_exists(data['email']):
            #     return Response(get_validation_failure_response(validation.errors, 'User with email already exist'))

            validation = EmployeePersonalInfoSerializer(data=request.data)

            '''check if user with same mobile already exist'''
            if validation.is_valid() == False:
                return Response(get_validation_failure_response(validation.errors, 'User with mobile number already exist'))

            if 'email' not in data:
                data['email'] = get_email_from_user_name(data['first_name'])

            user = User(
                username=data['email'], email=data['email'], password=data['email']+'@123')
            user.first_name = data['first_name']

            if 'last_name' in data:
                user.last_name = data['last_name']

            user.save()

            data_employee = {}
            if 'gender' in data:
                data_employee['gender'] = data['gender']
            data_employee['mobile_number'] = data['mobile_number']

            employeePersonalInfo = EmployeePersonalInfo.objects.create(
                user=user, **data_employee)
            employeePersonalInfo.save()

            userAuthentication = UserAuthentication.objects.create(user=user)
            userAuthentication.admin_registration_designation = "Business Owner"
            #  data['designation']
            userAuthentication.is_admin = False
            userAuthentication.is_active = True
            userAuthentication.save()

            if 'branch_code' in data:
                try:
                    companyBranchInfo = CompanyBranchInfo.objects.get(
                        code=data['branch_code'])
                    employee_id = random.randint(1000, 9999)
                    form_employee_company_info = {}
                    form_employee_company_info['employee_id'] = employee_id

                    # employeeDesignation = EmployeeDesignation.objects.create(company = companyMeta, company_branch = company_branch, name=userAuthentication.admin_registration_designation, is_admin=True)
                    # employeeDepartment = CompanyDepartment.objects.create(company = companyMeta, company_branch = company_branch, name="Management")
    # , department = employeeDepartment, designation = employeeDesignation, company=companyMeta, company_branch= company_branch,
                    EmployeeCompanyInfo.objects.create(
                        user=user, company=companyBranchInfo.company, company_branch=companyBranchInfo, **form_employee_company_info)
                except:
                    pass
            set_mobile_otp(userAuthentication, is_login=False)
            return Response(get_success_response("Registration Successful"))
        else:
            print("validationvalidation02")
            print("validationvalidation", validation.errors)
            return Response(get_validation_failure_response(validation.errors))


class AttachUserAccounts(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        print(data)

        validateRequest = ValidateRequest(
            request=request, request_serializer=AttachUserAccountsSerializer)
        if not validateRequest.is_valid():
            return Response(get_validation_failure_response(None, validateRequest.errors_formatted()))

        employeeCompanyInfo = validateRequest.employee_company_info()
        employeePersonalInfo = validateRequest.employee_personal_info()
        employeePersonalInfo.attached_users = data['attached_users']
        employeePersonalInfo.save()

        return Response(get_success_response("User Attached Successfully"))


class GetAttachedUserAccounts(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        print(data)

        validateRequest = ValidateRequest(
            request=request, request_serializer=AttachUserAccountsSerializer)
        if not validateRequest.is_valid():
            return Response(get_validation_failure_response(None, validateRequest.errors_formatted()))

        employeePersonalInfo = validateRequest.employee_personal_info()
        attached_users = employeePersonalInfo.attached_users

        response = {'attached_users': attached_users}
        return Response(get_success_response("User Attached Successfully", details=response))


class RegisterCompany(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):

        validateRequest = ValidateRequest(
            request=request, request_serializer=RegisterCompanySerializer)
        if not validateRequest.is_valid_open_request():
            return Response(get_validation_failure_response(None, validateRequest.errors_formatted()))

        data = request.data
        request_info = get_user_company_from_request(request)

        user = get_user_from_request(request_info, data)
        # print(user.first_name)
        # return Response(get_validation_failure_response([]))

        # if validateRequest.is_valid():
        #     return Response(get_validation_failure_response(None, "Invalid Request. Company already exist1"))
        # elif validateRequest.is_admin() == False:
        #     return Response(get_validation_failure_response(None, "Action not permitted by user1"))

        form_company_meta = {}
        form_company_meta['brand_name'] = data['brand_name']
        form_company_meta['display_name'] = data['brand_name']
        form_company_meta['registered_name'] = data['registered_name']
        form_company_meta['is_active'] = False
        # form_company_meta['type_of_business_id'] = data['brand_service_type_id']
        form_company_meta['sector_id'] = data['brand_sector_id']

        validation_form_company_meta = CompanyMetaSerializer(
            data=form_company_meta)

        if validation_form_company_meta.is_valid():
            companyMeta = CompanyMeta.objects.create(**form_company_meta)
            companyMeta.sector_id = data['brand_sector_id']
            # companyMeta.type_of_business_id = data['business_type_id']
            companyMeta.save()

            # adding company contact
            form_company_contact = {}
            form_company_contact['is_default'] = True
            form_company_contact['communication_address'] = data['communication_address']
            form_company_contact['pincode'] = data['pincode']
            form_company_contact['country'] = 'IN'
            form_company_contact['mobile_number_01'] = data['mobile_number1']

            if 'mobile_number2' in form_company_contact:
                form_company_contact['mobile_number_02'] = data['mobile_number2']

            company_contact = CompanyContactInfo.objects.create(
                **form_company_contact)

            # adding company branch
            form_company_branch = {}
            form_company_branch['name'] = data['brand_name']
            form_company_branch['display_name'] = data['brand_name']
            form_company_branch['is_parent'] = True
            form_company_branch['is_active'] = True

            if 'provider_company_branch_id' in data:
                # providerCompanyBranchInfo = CompanyBranchInfo.objects.get(
                #     data['provider_company_branch_id'])
                form_company_branch['provider_company_branch_id'] = data['provider_company_branch_id']

            company_branch = CompanyBranchInfo.objects.create(
                company_contact=company_contact,  company=companyMeta, **form_company_branch)

            # user = EmployeePersonalInfo.objects.all().last().user
            if 'mobile_number1' in data:
                employeePersonalInfo = EmployeePersonalInfo.objects.get(
                    mobile_number=data['mobile_number1'])
                userAuthentication = UserAuthentication.objects.get(
                    user=employeePersonalInfo.user, is_admin=True)
                user = employeePersonalInfo.user
                print("====1")
            else:
                user = get_user_from_request(request_info, data)
                print("useruser", user.first_name)
                userAuthentication = UserAuthentication.objects.get(
                    user=user, is_admin=True)
                print("====133333")
            # adding employee
            form_company_branch = {}
            form_company_branch['name'] = data['brand_name']
            form_company_branch['display_name'] = data['brand_name']
            form_company_branch['is_parent'] = True
            form_company_branch['is_active'] = True

            employee_id = random.randint(1000, 9999)
            form_employee_company_info = {}
            form_employee_company_info['employee_id'] = employee_id

            employeeDesignation = EmployeeDesignation.objects.create(
                company=companyMeta, company_branch=company_branch, name=userAuthentication.admin_registration_designation, is_admin=True)
            employeeDepartment = CompanyDepartment.objects.create(
                company=companyMeta, company_branch=company_branch, name="Management")

            EmployeeCompanyInfo.objects.create(user=user, authentication=userAuthentication, department=employeeDepartment,
                                               designation=employeeDesignation, company=companyMeta, company_branch=company_branch, **form_employee_company_info)

            return Response(get_success_response("Registration Successful"))


class ValidateRegistrationUser(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        print("dddaaa", data)
        validation_mobile = ValidateUserMobileSerializer(data=request.data)
        if validation_mobile.is_valid():
            user = getuser_by_mobile(data['mobile_number'])
            if user is not None:
                return Response(get_validation_failure_response(None, 'User with this mobile number already exist. Please login to continue'))
            else:
                set_mobile_otp_registation(data['mobile_number'])
                return Response(get_success_response(""))
        else:
            return Response(get_validation_failure_response(validation_mobile.errors))


class ValidateUser(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        print("dddaaa", data)
        validation_mobile = ValidateUserMobileSerializer(data=request.data)
        if validation_mobile.is_valid():
            user = getuser_by_mobile(data['mobile_number'])
            if user is not None:
                try:
                    userAuthentication = UserAuthentication.objects.get(
                        user=user, is_active=True)
                    set_mobile_otp(userAuthentication, is_login=True)
                    return Response(get_success_response("User Validated Successfully"))
                except Exception as e:
                    return Response(get_validation_failure_response(None, 'User not active. Please contact Admin'))
            else:
                set_mobile_otp_registation_customer(data['mobile_number'])
                return Response(get_validation_failure_response(None, 'T'))
        else:
            return Response(get_validation_failure_response(validation_mobile.errors, error_message="Failure"))


class ValidateUserBusiness(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        print("dddaaa", data)
        validation_mobile = ValidateUserMobileSerializer(data=request.data)
        if validation_mobile.is_valid():
            user = getuser_by_mobile(data['mobile_number'])
            if user is not None:
                try:
                    userAuthentication = UserAuthentication.objects.get(
                        user=user, is_active=True)
                    set_mobile_otp(userAuthentication, is_login=True)
                    return Response(get_success_response("User Validated Successfully"))
                except Exception as e:
                    return Response(get_validation_failure_response(None, 'User not active. Please contact Admin'))
            else:
                return Response(get_validation_failure_response(None, 'User not registered. Please tap on register, to register a business', -1, 'A'))
        else:
            return Response(get_validation_failure_response(validation_mobile.errors))


class ValidateUserWeb(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        print("dddaaa", data)
        validation_email = ValidateUserEmailSerializer(data=request.data)
        validation_mobile = ValidateUserMobileSerializer(data=request.data)
        if validation_email.is_valid():
            user = getuser_by_email(data['email'])
            if user is not None:
                try:
                    userAuthentication = UserAuthentication.objects.get(
                        user=user, is_active=True)
                    if userAuthentication.is_admin:
                        set_mobile_otp(userAuthentication, is_login=True)
                        return Response(get_success_response("User Validated Successfully"))
                    else:
                        try:
                            EmployeeCompanyInfo.objects.get(
                                user=userAuthentication.user, designation__is_admin=True)
                            set_mobile_otp(userAuthentication, is_login=True)
                            return Response(get_success_response("User Validated Successfully"))
                        except:
                            return Response(get_validation_failure_response(None, 'User not authorized'))
                except Exception as e:
                    return Response(get_validation_failure_response(None, 'User not registered. Please contact Admin'))
            else:
                return Response(get_validation_failure_response(None, 'User not registered. Please contact Admin'))
        elif validation_mobile.is_valid():
            user = getuser_by_mobile(data['mobile_number'])
            if user is not None:
                try:
                    userAuthentication = UserAuthentication.objects.get(
                        user=user, is_active=True)
                    set_mobile_otp(userAuthentication, is_login=True)
                    return Response(get_success_response("User Validated Successfully"))
                except Exception as e:
                    return Response(get_validation_failure_response(None, 'User not registered. Please contact Admin'))
            else:
                return Response(get_validation_failure_response(None, 'User not registered. Please contact Admin'))
        else:
            return Response(get_validation_failure_response(validation_mobile.errors))


class GetBusinessPlaces(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        validation = GetBusinessPlacesSerializer(data=data)
        print("=======================001")
        if validation.is_valid():

            q = data['q']

            # from ttext
            if data['type'] == 'phone':
                list_google_places = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?fields=formatted_address%2Cname%2Cplace_id&input=%2B91' + \
                    q+'&inputtype=phonenumber&country=in&key=AIzaSyCxiyjYNDLQ4D1HZkm4g4M0D6XEsDgbHHo&fields=formatted_address%2Cplace_id'

                r = requests.post(url=list_google_places)
                print("from phone")

                formatted_list = json.loads(r.content)

                print("formatted_listformatted_list=============p")
                print(formatted_list)
                # formatted_list = formatted_list['predictions']
                formatted_list = formatted_list['candidates']

                response_data = []
                for place in formatted_list:
                    response_data.append(
                        {"place_id": place['place_id'], 'title': place['name'], 'address': place['formatted_address']})
                return Response(get_success_response(None, None, response_data))

            elif data['type'] == 'address':
                list_google_places = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?fields=formatted_address%2Cname%2Cplace_id&input=' + \
                    q+'&inputtype=textquery&country=in&key=AIzaSyCxiyjYNDLQ4D1HZkm4g4M0D6XEsDgbHHo'

                r = requests.post(url=list_google_places)
                print("from address")

                formatted_list = json.loads(r.content)
                # formatted_list = formatted_list['predictions']
                formatted_list = formatted_list['candidates']

                response_data = []
                for place in formatted_list:
                    response_data.append(
                        {"place_id": place['place_id'], 'title': place['name'], 'address': place['formatted_address']})
                    # response_data.append({"place_id":place['place_id'], 'title': place['formatted_address']})
                return Response(get_success_response(None, None, response_data))

                # list_google_places = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?input='+q+'&country=in&key=AIzaSyCxiyjYNDLQ4D1HZkm4g4M0D6XEsDgbHHo'

            # else:angel%20clinic%20gummidipoondi
            # list_google_places = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?input=Leora%20infotech&radius=500&types=establishment&key=AIzaSyCxiyjYNDLQ4D1HZkm4g4M0D6XEsDgbHHo'

            # l1 pChIJRYvgiteBTToR6uFg2XQPACE

            # l3
            # list_google_places = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?fields=formatted_address%2Cplace_id%2Cname%2Crating%2Copening_hours%2Cgeometry&input='+q+'&inputtype=textquery&key=AIzaSyCxiyjYNDLQ4D1HZkm4g4M0D6XEsDgbHHo'
            # try:
            #     r = requests.post(url=list_google_places)
            #     print("dfsdfdsfdsfr")
            #     print(r.content)
            #     formatted_list = json.loads(r.content)
            #     # formatted_list = formatted_list['predictions']
            #     formatted_list = formatted_list['candidates']

            #     response_data = []
            #     for place in formatted_list:
            #         response_data.append({"place_id":place['place_id'], 'title': place['formatted_address']})
            #     return Response(get_success_response(None,None, response_data))

            # except HTTPError as e:
            #     print("ererr44")
            #     print(e.response.text)

            return Response(get_validation_failure_response(validation.errors, "Invalid Request1"))
        else:
            return Response(get_validation_failure_response(validation.errors, "Invalid Request2"))


class GetBusinessPlaceDetails(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        validation = GetBusinessPlaceDetailsSerializer(data=data)
        if validation.is_valid():

            try:
                place_id = data['id']
                r = requests.get(url='https://maps.googleapis.com/maps/api/place/details/json?place_id=' +
                                 place_id+'&key=AIzaSyCxiyjYNDLQ4D1HZkm4g4M0D6XEsDgbHHo')
                print("dfsdfdsfdsfr")
                print(r.content)
                formatted_list = json.loads(r.content)
                formatted_list = formatted_list['result']
                # response_data = formatted_list
                response_data = {}
                response_data['business_name'] = formatted_list['name']
                response_data['business_address'] = formatted_list['formatted_address']

                if 'address_components' in formatted_list:
                    for address_break in formatted_list['address_components']:
                        for a in address_break['types']:
                            if a == 'postal_code':
                                response_data['pin_code'] = address_break['short_name']
                                break
                                break
                if 'formatted_phone_number' in formatted_list:
                    response_data['contact_number'] = formatted_list['formatted_phone_number'].replace(
                        " ", '')[-10:]
                response_data['maps_url'] = formatted_list['url']

                # response_data['business_name'] = ''

                return Response(get_success_response(None, None, response_data))

            except HTTPError as e:
                print("ererr44")
                print(e.response.text)
            response_data = {}
            return Response(get_success_response(None, None, response_data))
        else:
            return Response(get_validation_failure_response(validation.errors))


class ResendRegistationOtp(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        validation = ValidateUserSerializer(data=data)
        if validation.is_valid():
            user = getuser_by_mobile(data['mobile_number'])
            if user is None:
                set_mobile_otp_registation(data['mobile_number'])
                return Response(get_success_response("Otp Sent Successfully"))
            else:
                return Response(get_validation_failure_response(None, "User Already registered"))

        else:
            return Response(get_validation_failure_response(validation.errors))


class ResendLoginOtp(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        validation = ValidateUserSerializer(data=data)
        if validation.is_valid():
            user = getuser_from_params(data)
            if user is not None:
                userAuthentication = UserAuthentication.objects.get(user=user)
                set_mobile_otp(userAuthentication, is_login=True)
                return Response(get_success_response("Otp Sent Successfully"))
            else:
                return Response(get_validation_failure_response(None, 'Invalid user'))
        else:
            return Response(get_validation_failure_response(None, 'Invalid user'))


class DeleteUser(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        request_info = get_user_company_from_request(request)
        if request_info['user'] is not None:
            try:
                userAuthentication = UserAuthentication.objects.get(
                    user=request_info['user'], is_active=True)
                userAuthentication.is_active = False
                userAuthentication.save()
                return Response(get_success_response(None))
            except:
                pass
        return Response(get_validation_failure_response(None, 'Invalid User'))


class OtpLogin(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        validation = OtpLoginSerializer(data=request.data)
        if validation.is_valid():
            user = getuser_from_params(data)
            if user is not None:
                userAuthentication = get_active_user(user=user, is_active=True)
                # is_otp_verified=True
                if userAuthentication is not None:
                    if userAuthentication.mobile_otp == data['otp']:
                        token = get_user_token(user.username)
                        response = {"success": True, "token": token,
                                    "message": "User Loggedin Successfully"}

                        user_company_info = get_user_company_from_user(user)
                        response['employee_id']=user_company_info['employee_id']
                        response['name'] = user_company_info['name']
                        response['mobile_number'] = user_company_info['mobile_number']
                        response['photo'] = user_company_info['photo']
                        
                        response['is_faculty'] = user_company_info['is_admin']
                        
                        # response['type_is_provider'] = user_company_info['company']
                        response['company_branch'] = user_company_info['company_branch']
                        return Response(get_success_response(None, None, response))

                        # return Response(response)
                    else:
                        return Response(get_validation_failure_response(None, "Invalid Otp"))
                else:
                    return Response(get_validation_failure_response(None, "User Approval pending. Please contact Admin"))
            else:
                return Response(get_validation_failure_response(None, "Invalid User"))
        else:
            return Response(get_validation_failure_response(validation.errors))


class OtpRegister(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        validation = OtpRegisterSerializer(data=request.data)
        if validation.is_valid():
            userCredentialValidations = UserCredentialValidation.objects.filter(
                mobile_number=data['mobile_number'])
            if userCredentialValidations.count() == 0:
                return Response(get_validation_failure_response(None, "Invalid user"))
            userCredentialValidation = userCredentialValidations.last()
            if userCredentialValidation.mobile_otp == data['otp']:
                # current_time = get_current_time_aware()
                # datetime.now()
                current_time = timezone.now()
                otp_expiry = (userCredentialValidation.otp_expiry)
                # if current_time < otp_expiry:
                # if current_time < userCredentialValidations.last().otp_expiry:
                return Response(get_success_response("OTP validated Successfully"))
                # else:
                # return Response(get_validation_failure_response(None, "OTP Expired"))
            else:
                return Response(get_validation_failure_response(None, "Invalid OTP"))
        else:
            return Response(get_validation_failure_response(validation.errors))


class SubmitRegistationOtp(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        validation = SubmitRegistationOtpSerializer(data=request.data)
        if validation.is_valid():
            user = getuser_from_params(data)
            if user is not None:
                userAuthentication = UserAuthentication.objects.get(user=user)
                current_time = timezone.now()
                otp_expiry = (userAuthentication.otp_expiry)
                if True:
                    if userAuthentication.mobile_otp == data['otp']:
                        userAuthentication.is_active = True
                        userAuthentication.is_otp_verified = True
                        userAuthentication.is_admin = True
                        userAuthentication.save()
                        response = get_success_response(
                            "Admin registered Successfully")
                        response['token'] = get_user_token(user.username)
                        user_company_info = get_user_company_from_user(user)
                        response['is_admin'] = user_company_info['is_admin']
                        response['is_branch_admin'] = user_company_info['is_branch_admin']
                        data = {}
                        data['token'] = response['token']
                        data['is_admin'] = user_company_info['is_admin']
                        data['is_branch_admin'] = user_company_info['is_branch_admin']
                        response['details'] = data
                        return Response(response)
                    else:
                        return Response(get_validation_failure_response(None, "Invalid Otp"))
                else:
                    return Response(get_validation_failure_response(None, "Otp Expired2"))
            else:
                return Response(get_validation_failure_response(None, 'Invalid user'))
        else:
            return Response(get_validation_failure_response(validation.errors))


class MobileAppConfig(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        print(data)
        details = {}
        appBaseConfig = AppBaseConfig.objects.all().first()
        app_config = {}

        app_config['partial_update'] = False
        app_config['force_update'] = False

        if data['device_platform'] == 'android':
            app_config['current_version'] = appBaseConfig.current_version_android
            app_config['minimum_version'] = appBaseConfig.minimum_support_version_android

            if float(data['app_version']) < float(app_config['minimum_version']):
                app_config['force_update'] = True
        else:
            app_config['current_version'] = appBaseConfig.current_version_ios
            app_config['minimum_version'] = appBaseConfig.minimum_support_version_ios

        # app_config['force_update'] = True
        details['app_config'] = app_config

        return Response(get_success_response(None, None, details))


class Dashboard(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        print("details=====================001")
        data = request.data
        request_info = get_user_company_from_request(request)
        if request_info['company_info'] is not None:

            try:
                employeeCompanyInfo = EmployeeCompanyInfo.objects.get(
                    user=request_info['user'])
                if employeeCompanyInfo.authentication.is_active == False:
                    print("details=====================002")
                    return Response(get_validation_failure_response(None, 'Please login to continue'))
            except Exception as e:
                print("details=====================003", e)
                return Response(get_validation_failure_response(None, 'Please login to continue'))

            res = get_success_response()
            res["success"] = True
            user_details = {}
            user_details["employee_id"]=employeeCompanyInfo.id
            user_details["name"] = request_info['user'].first_name
            user_details["designation"] = request_info['designation']
            user_details["email"] = request_info['user'].email  
            user_details["is_faculty"]=employeeCompanyInfo.authentication.is_faculty
            employeePersonalInfo = EmployeePersonalInfo.objects.get(
                user=request_info['user'])
            
            user_details["mobile_number"] = employeePersonalInfo.mobile_number
            user_details["gender"] = employeePersonalInfo.gender

            if employeeCompanyInfo.photo and hasattr(employeeCompanyInfo.photo, 'url'):
                user_details["photo"] = employeeCompanyInfo.photo.url
            else:
                user_details["photo"] = None

            permission_details = {}
            permission_details["is_admin"] = request_info["is_admin"]
            permission_details["is_branch_admin"] = request_info["is_branch_admin"]

            # company_branch = request_info["company_info"].company_branch
            # permission_details["branch_id"] =  request_info["company_info"].company_branch.id
            permission_details["company_id"] = request_info["company_info"].company.id
            

            details = {"user_details": user_details,
                       "permission_details": permission_details}

            details['company'] ={
                "name": employeeCompanyInfo.company.brand_name,"id":employeeCompanyInfo.company.id}
            # details['company_branch'] = {
            #     "name":employeeCompanyInfo.company_branch.name, "id":employeeCompanyInfo.company_branch.id}            
            if employeeCompanyInfo.company.attachment_logo and hasattr(employeeCompanyInfo.company.attachment_logo, 'url'):
                details["company_logo"] = employeeCompanyInfo.company.attachment_logo.url
            else:
                details["company_logo"] = None

            # details['ticket_status'] = Ticket.TICKET_STATUS_CHOICES

            print("details")
            print("details=====================004")
            print(details)
            return Response(get_success_response(None, None, details))
        else:
            details = {}
            print("details2")
            print(details)
            return Response(get_validation_failure_response(None, 'Please login to continue'))
