from mmap import PAGESIZE
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from company.models import CompanyBranchInfo, CompanyDocument

import employee
from .request_serializer import AddEmployeeSerializerV1, EnableFaceReRegisterSerializer, UpdateEmployeeCheckinAssociationsSerializer, GetEmployeeDetailsSerializer, RaiseAnonymousComplaintSerializer,UpdateEmployeeProfilePhotoSerializer, AddEmployeeSerializer, AddDesignationSerializer, UpdateEmployeeStatusSerializer, ValidateUserByFaceSerializer
from authentication.model_helper import get_paginated_results_set, username_exists, get_first_object_by_user
from employee.models import EmployeeDesignation,AnonymousComplaintTicket, EmployeeDocument, EmployeeDocumentGroup, EmployeeDocumentLocker, EmployeeFacePhoto, EmployeePersonalInfo, EmployeeFinancialInfo, EmployeeCompanyInfo
from .form_serializer import EmployeePersonalInfoSerializer
from authentication.models import UserAuthentication
import random
from authentication.message_utils import send_employee_registration
from authentication.model_helper import get_user_from_request, getuser_by_mobile, get_object_by_pk, get_user_company_from_request, check_if_exist
from employee.model_helper import get_designations, get_employee_document_tags, get_employees, get_employees_each_branch
from employee.response_serializer import EmployeeCompanyInfoSerializerWeb, EmployeeDocumentsSerializer, EmployeesDocumentsSerializer, EmployeesTimeSheetsSerializer, DesignationDropdownSerializer, EmployeeCompanyInfoSerializer, EmployeeDetailsSerializer
from authentication.response_serializer import get_validation_failure_response, get_success_response
import base64
from django.core.files.base import ContentFile 
from authentication.date_utils import get_start_end_date_today, get_start_end_date_per_month_from_request, get_start_end_date_from_request, get_start_end_date_month, get_current_time_aware
from authentication.constants import LIST_DEFAULT_COUNT

class GetEmployeesV1Web(APIView):
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        print(data)
        request_info = get_user_company_from_request(request)
        if request_info['company_info'] is not None: 
            if (request_info['is_admin'] or request_info['is_branch_admin']):
                employeesQ = get_employees(request_info['company_info'].company.id)


                if 'branch_id' in data and employeesQ.count()>0:

                    branch_ids = [data['branch_id']]
                    if 'include_child' in data and data['include_child']:
                        branch_ids = data['child_ids']
                        branch_ids.append(data['branch_id'])
                    try:
                        employeesQ = employeesQ.filter(company_branch__id__in = branch_ids)
                    except:
                        pass
                

                is_active = True

                try:
                    if 'is_active' in data:
                        is_active = data['is_active']
                except:
                    pass

                employeesQ = employeesQ.filter(authentication__is_active = is_active)
                
                if 'q' in data and employeesQ.count()>0:
                    employeesQ = employeesQ.filter(user__first_name__istartswith = data['q'])

                page_number = 1
                if 'page_number' in data:
                    page_number = data['page_number']
                res = get_paginated_results_set(employeesQ, EmployeeCompanyInfoSerializerWeb, page_number, 20)
                
                # res['re']
                return Response(get_success_response(None, "Employee List", res))
            elif request_info['is_branch_admin']:
                print("request_info")
                print(request_info)
                employeesQ = get_employees_each_branch(request_info['company_info'].company_branch.id)

                if 'q' in data and employeesQ.count()>0:
                    employeesQ = employeesQ.filter(user__first_name__istartswith = data['q'])

                page_number = 1
                if 'page_number' in data:
                    page_number = data['page_number']
                res = get_paginated_results_set(employeesQ, EmployeeCompanyInfoSerializer, page_number, 20)
                return Response(get_success_response(None, "Employee List", res))
            else:
                return Response(get_validation_failure_response(None, 'Invalid user'))
        else:
            return Response(get_validation_failure_response(None, 'Invalid user'))

class GetEmployeesV1(APIView):
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        print(data)
        request_info = get_user_company_from_request(request)
        if request_info['company_info'] is not None: 
            if (request_info['is_admin'] or request_info['is_branch_admin']):
                employeesQ = get_employees(request_info['company_info'].company.id)


                if 'branch_id' in data and employeesQ.count()>0:

                    branch_ids = [data['branch_id']]
                    if 'include_child' in data and data['include_child']:
                        branch_ids = data['child_ids']
                        branch_ids.append(data['branch_id'])
                    try:
                        employeesQ = employeesQ.filter(company_branch__id__in = branch_ids)
                    except:
                        pass
                

                is_active = True

                try:
                    if 'is_active' in data:
                        is_active = data['is_active']
                except:
                    pass

                employeesQ = employeesQ.filter(authentication__is_active = is_active)
                
                if 'q' in data and employeesQ.count()>0:
                    employeesQ = employeesQ.filter(user__first_name__istartswith = data['q'])

                page_number = 1
                if 'page_number' in data:
                    page_number = data['page_number']
                res = get_paginated_results_set(employeesQ, EmployeeCompanyInfoSerializer, page_number, 20)
                try:
                    res['data'][0]['can_reregister_face'] = False
                except:
                    pass

                return Response(get_success_response(None, "Employee List", res))
            else:
                return Response(get_validation_failure_response(None, 'Invalid user'))
        else:
            return Response(get_validation_failure_response(None, 'Invalid user'))

class GetDesignations(APIView):
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        request_info = get_user_company_from_request(request)
        if request_info['company_info'] is not None and (request_info['is_admin'] or request_info['is_branch_admin']):
                designationsQ = get_designations(request_info['company_info'].company.id)
                serializer = DesignationDropdownSerializer(designationsQ, many=True)
                res = {}
                return Response(get_success_response(None, "Designation List", serializer.data))
        else:
            return Response(get_validation_failure_response(None, 'Invalid user'))
           
class AddDesignation(APIView):
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        request_info = get_user_company_from_request(request)        
        validation = AddDesignationSerializer(data=data)
        if validation.is_valid() and request_info['company_info'] is not None and request_info['is_admin']:
            if CompanyBranchInfo.objects.get(id = request_info['company_branch']['id']).is_parent:
                if check_if_exist(EmployeeDesignation, {"name":data['name'], "company":request_info['company_info'].company}) == False:
                    form_employee_designation = {}
                    form_employee_designation['name'] = data['name']
                    employeeDesignation = EmployeeDesignation(**data)
                    employeeDesignation.company_branch = request_info['company_info'].company_branch
                    employeeDesignation.company = request_info['company_info'].company
                    employeeDesignation.save()
                    return Response(get_success_response("Designation added successfully"))
                else:
                    return Response(get_validation_failure_response(None, "Designation already exist"))
            else:
                return Response(get_validation_failure_response(None, "Please Contact Admin to Add Designation"))
        else:
            return Response(get_validation_failure_response(validation.errors))

class UpdateEmployeeStatus(APIView):
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        print("Add Employee << data================")
        print(data)
        request_info = get_user_company_from_request(request)        
        validation = UpdateEmployeeStatusSerializer(data=request.data)
        if validation.is_valid():
        #  and request_info['company_info'] is not None and (request_info['is_admin'] or request_info['is_branch_admin']):
            
            employeeCompanyInfo = get_object_by_pk(EmployeeCompanyInfo, data['id'])
            print("000")
            if employeeCompanyInfo is not None:
                print("001")
                userAuthentication = get_first_object_by_user(UserAuthentication, employeeCompanyInfo.user)
                if userAuthentication is not None:
                    print("002")
                    if data['is_active'] == False:
                        userAuthentication.is_active = False
                        userAuthentication.save()
                        return Response(get_success_response("Employee disabled"))
                    else:
                        userAuthentication.is_active = True
                        userAuthentication.save()
                        return Response(get_success_response("Employee re-activated successfully"))
            return Response(get_validation_failure_response(None, "Invalid User1"))
        else:
            return Response(get_validation_failure_response(validation.errors))

class AddEmployeeV1(APIView):
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        print("Add Employee << data================")
        print(data)
        request_info = get_user_company_from_request(request)        
        validation = AddEmployeeSerializerV1(data=request.data)
        if validation.is_valid() and request_info['company_info'] is not None and (request_info['is_admin'] or request_info['is_branch_admin']):
            if 'id' in data:
                employeeCompanyInfo = get_object_by_pk(EmployeeCompanyInfo, data['id']) 
                if employeeCompanyInfo is None:
                    return Response(get_validation_failure_response(None, "Invalid User"))

                user = employeeCompanyInfo.user
                user.first_name = data['first_name']
                if 'last_name' in data:
                    user.last_name = data['last_name']
                else:
                    user.last_name = ''

                if request_info['is_admin']:
                    user.email = data['email']
                user.save()

                employeePersonalInfo = get_first_object_by_user(EmployeePersonalInfo, user) 
                  
                employeePersonalInfo.gender = data['gender']

                if 'aadhar_number' in data:
                    employeePersonalInfo.aadhar = data['aadhar_number']

                if request_info['is_admin']:
                    employeePersonalInfo.mobile_number = data['mobile_number']
                
                if 'dob' in data:
                    employeePersonalInfo.dob = data['dob']

                if 'blood_group' in data:
                    employeePersonalInfo.blood_group = data['blood_group']

                employeePersonalInfo.save()                

                employeeFinancialInfo = get_first_object_by_user(EmployeeFinancialInfo, user) 
                if 'pan' in data:
                    employeeFinancialInfo.pan = data['pan']
                employeeFinancialInfo.save()


                employeeCompanyInfo = get_first_object_by_user(EmployeeCompanyInfo, user) 
                employeeCompanyInfo.department_id = data['department_id']
                employeeCompanyInfo.designation_id = data['designation_id'] 
                employeeCompanyInfo.company_branch_id = data['branch_id']
                
                try:
                    if 'date_of_joining' in data:
                        employeeCompanyInfo.date_of_joining = data['date_of_joining']
                except:
                    pass
                try:
                    if 'employment_type' in data:
                        employeeCompanyInfo.employment_type = data['employment_type']
                except:
                    pass

                employeeCompanyInfo.save()


                return Response(get_success_response("Employee Details updated Successfully"))

            else:
                if username_exists(data['email']):
                    return Response(get_validation_failure_response(None, "User with email already exist"))
                if getuser_by_mobile(data['mobile_number']) is not None:
                    return Response(get_validation_failure_response(None, "User with mobile number already exist"))

                user = User(username=data['email'], email=data['email'], password=data['email']+'@123')
                user.first_name = data['first_name']
                if 'last_name' in data:
                    user.last_name = data['last_name']
                else:
                    user.last_name = ''

                user.save()

                data_employee = {}    
                data_employee['gender'] = data['gender']
                if 'aadhar_number' in data:
                    data_employee['aadhar'] = data['aadhar_number']
                data_employee['mobile_number'] = data['mobile_number']
                try:
                    if 'dob' in data:
                        data_employee['dob'] = data['dob']
                except:
                    pass
                
                try:
                    if 'blood_group' in data:
                        data_employee['blood_group'] = data['blood_group']
                except:
                    pass
                    

                validation = EmployeePersonalInfoSerializer(data=request.data)
                if validation.is_valid():
                    employeePersonalInfo = EmployeePersonalInfo.objects.create(user=user,**data_employee)
                    employeePersonalInfo.save()

                    data_employee_financial = {}
                    employeeFinancialInfo = EmployeeFinancialInfo.objects.create(user=user,**data_employee_financial)
                    if 'pan' in data:
                        employeeFinancialInfo.pan = data['pan']
                    employeeFinancialInfo.save()

                    otp = random.randint(1000,9999)
                    userAuthentication = UserAuthentication.objects.create(user=user, mobile_otp=otp, is_active=True)
                    userAuthentication.save()

                    employee_id = random.randint(100000,999999)
                    form_employee_company_info = {}
                    form_employee_company_info['employee_id'] = employee_id

                    employeeCompanyInfo = EmployeeCompanyInfo.objects.create(user=user, company=request_info['company_info'].company, **form_employee_company_info)
                    employeeCompanyInfo.department_id = data['department_id']
                    employeeCompanyInfo.designation_id = data['designation_id']
                    employeeCompanyInfo.company_branch_id = data['branch_id']
                    employeeCompanyInfo.authentication = userAuthentication

                    try:
                        if 'date_of_joining' in data:
                            employeeCompanyInfo.date_of_joining = data['date_of_joining']
                    except:
                        pass

                    try:
                        if 'employment_type' in data:
                            employeeCompanyInfo.employment_type = data['employment_type']
                    except:
                        pass

                    employeeCompanyInfo.save()

                    send_employee_registration(request_info['company']['name'], data['mobile_number'])

                    return Response(get_success_response("User Added Successfully"))
                else:
                    return Response(get_validation_failure_response(validation.errors, "User with one or more provided details already exist"))
        else:
            return Response(get_validation_failure_response(validation.errors))


class AddStudent(APIView):
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        print("Add Employee << data================")
        print(data)
        request_info = get_user_company_from_request(request)        
        # validation = AddEmployeeSerializerV1(data=request.data)
        if request_info['company_info'] is not None and (request_info['is_admin'] or request_info['is_branch_admin']):
            if 'id' in data:
                employeeCompanyInfo = get_object_by_pk(EmployeeCompanyInfo, data['id']) 
                if employeeCompanyInfo is None:
                    return Response(get_validation_failure_response(None, "Invalid User"))

                user = employeeCompanyInfo.user
                user.first_name = data['first_name']
                if 'last_name' in data:
                    user.last_name = data['last_name']
                else:
                    user.last_name = ''

                if request_info['is_admin']:
                    user.email = data['email']
                user.save()

                employeePersonalInfo = get_first_object_by_user(EmployeePersonalInfo, user) 
                  
                employeePersonalInfo.gender = data['gender']

                if 'aadhar_number' in data:
                    employeePersonalInfo.aadhar = data['aadhar_number']

                if request_info['is_admin']:
                    employeePersonalInfo.mobile_number = data['mobile_number']
                
                if 'dob' in data:
                    employeePersonalInfo.dob = data['dob']

                if 'blood_group' in data:
                    employeePersonalInfo.blood_group = data['blood_group']
                if 'address' in data:
                    employeePersonalInfo.address= data['address']
                if 'pincode' in data:
                    employeePersonalInfo.pincode= data['pincode']
                

                employeePersonalInfo.save()                

                employeeFinancialInfo = get_first_object_by_user(EmployeeFinancialInfo, user) 
                if 'pan' in data:
                    employeeFinancialInfo.pan = data['pan']
                employeeFinancialInfo.save()


                employeeCompanyInfo = get_first_object_by_user(EmployeeCompanyInfo, user) 
                employeeCompanyInfo.department_id = data['department_id']
                # employeeCompanyInfo.company_branch_id = data['branch_id']

                # if parent branch and admin can send employeeCompanyInfo.company_branch_id = data['branch_id']
                
                # else get users branch from token  set at branch id
                try:
                    if 'date_of_joining' in data:
                        employeeCompanyInfo.date_of_joining = data['date_of_joining']
                except:
                    pass
                try:
                    if 'employment_type' in data:
                        employeeCompanyInfo.employment_type = data['employment_type']
                except:
                    pass

                employeeCompanyInfo.save()


                return Response(get_success_response("Employee Details updated Successfully"))

            else:
                if username_exists(data['email']):
                    return Response(get_validation_failure_response(None, "User with email already exist"))
                if getuser_by_mobile(data['mobile_number']) is not None:
                    return Response(get_validation_failure_response(None, "User with mobile number already exist"))

                user = User(username=data['email'], email=data['email'], password=data['email']+'@123')
                user.first_name = data['first_name']
                if 'last_name' in data:
                    user.last_name = data['last_name']
                else:
                    user.last_name = ''

                user.save()

                data_employee = {}    
                data_employee['gender'] = data['gender']
                if 'aadhar_number' in data:
                    data_employee['aadhar'] = data['aadhar_number']
                data_employee['mobile_number'] = data['mobile_number']
                try:
                    if 'dob' in data:
                        data_employee['dob'] = data['dob']
                except:
                    pass
                
                try:
                    if 'blood_group' in data:
                        data_employee['blood_group'] = data['blood_group']
                except:
                    pass

                try:
                    if 'address' in data:
                       data_employee['address'] = data['address']
                except:
                    pass
                try:
                    if 'pincode' in data:
                        data_employee['pincode'] = data['pincode']
                except:
                    pass
                
                    

                validation = EmployeePersonalInfoSerializer(data=request.data)
                if validation.is_valid():
                    employeePersonalInfo = EmployeePersonalInfo.objects.create(user=user,**data_employee)
                    employeePersonalInfo.save()

                    data_employee_financial = {}
                    employeeFinancialInfo = EmployeeFinancialInfo.objects.create(user=user,**data_employee_financial)
                    if 'pan' in data:
                        employeeFinancialInfo.pan = data['pan']
                    employeeFinancialInfo.save()

                    otp = random.randint(1000,9999)
                    userAuthentication = UserAuthentication.objects.create(user=user, is_student=True,  is_faculty=False, mobile_otp=otp, is_active=True)
                    userAuthentication.save()

                    employee_id = random.randint(100000,999999)
                    form_employee_company_info = {}
                    form_employee_company_info['employee_id'] = employee_id

                    employeeCompanyInfo = EmployeeCompanyInfo.objects.create(user=user, company=request_info['company_info'].company, **form_employee_company_info)
                    employeeCompanyInfo.department_id = data['department_id']
                    # employeeCompanyInfo.designation_id = data['designation_id']
                    # employeeCompanyInfo.company_branch_id = data['branch_id']
                    employeeCompanyInfo.authentication = userAuthentication

                    try:
                        if 'date_of_joining' in data:
                            employeeCompanyInfo.date_of_joining = data['date_of_joining']
                    except:
                        pass

                    try:
                        if 'employment_type' in data:
                            employeeCompanyInfo.employment_type = data['employment_type']
                    except:
                        pass

                    employeeCompanyInfo.save()

                    # send_employee_registration(request_info['company']['name'], data['mobile_number'])

                    details = {'id':employeeCompanyInfo.id}
                    return Response(get_success_response("Student Added Successfully", details=details))
                else:
                    return Response(get_validation_failure_response("User with one or more provided details already exist"))
        else:
            return Response(get_validation_failure_response('Validation error'))


class AddFaculty(APIView):
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        print("Addaaa Employee << data================")
        print(data)
        request_info = get_user_company_from_request(request)        
        # validation = AddEmployeeSerializerV1(data=request.data)
        if request_info['company_info'] is not None and (request_info['is_admin'] or request_info['is_branch_admin']):
            if 'id' in data:
                employeeCompanyInfo = get_object_by_pk(EmployeeCompanyInfo, data['id']) 
                if employeeCompanyInfo is None:
                    return Response(get_validation_failure_response(None, "Invalid User"))

                user = employeeCompanyInfo.user
                user.first_name = data['first_name']
                if 'last_name' in data:
                    user.last_name = data['last_name']
                else:
                    user.last_name = ''

                if request_info['is_admin']:
                    user.email = data['email']
                user.save()

                employeePersonalInfo = get_first_object_by_user(EmployeePersonalInfo, user) 
                  
                employeePersonalInfo.gender = data['gender']

                if 'aadhar_number' in data:
                    employeePersonalInfo.aadhar = data['aadhar_number']

                if request_info['is_admin']:
                    employeePersonalInfo.mobile_number = data['mobile_number']
                
                if 'dob' in data:
                    employeePersonalInfo.dob = data['dob']

                if 'blood_group' in data:
                    employeePersonalInfo.blood_group = data['blood_group']
                if 'address' in data:
                    employeePersonalInfo.address= data['address']
                if 'pincode' in data:
                    employeePersonalInfo.pincode= data['pincode']
                

                employeePersonalInfo.save()                

                employeeFinancialInfo = get_first_object_by_user(EmployeeFinancialInfo, user) 
                if 'pan' in data:
                    employeeFinancialInfo.pan = data['pan']
                employeeFinancialInfo.save()


                employeeCompanyInfo = get_first_object_by_user(EmployeeCompanyInfo, user) 
                employeeCompanyInfo.department_id = data['course_id']
                employeeCompanyInfo.designation_id=data['role_id']
                # employeeCompanyInfo.company_branch_id = data['branch_id']
                
                try:
                    if 'date_of_joining' in data:
                        employeeCompanyInfo.date_of_joining = data['date_of_joining']
                except:
                    pass
                try:
                    if 'employment_type' in data:
                        employeeCompanyInfo.employment_type = data['employment_type']
                except:
                    pass

                employeeCompanyInfo.save()


                return Response(get_success_response("Employee Details updated Successfully"))

            else:
                if username_exists(data['email']):
                    return Response(get_validation_failure_response(None, "User with email already exist"))
                if getuser_by_mobile(data['mobile_number']) is not None:
                    return Response(get_validation_failure_response(None, "User with mobile number already exist"))

                user = User(username=data['email'], email=data['email'], password=data['email']+'@123')
                user.first_name = data['first_name']
                if 'last_name' in data:
                    user.last_name = data['last_name']
                else:
                    user.last_name = ''

                user.save()

                data_employee = {}    
                data_employee['gender'] = data['gender']
                if 'aadhar_number' in data:
                    data_employee['aadhar'] = data['aadhar_number']
                data_employee['mobile_number'] = data['mobile_number']
                try:
                    if 'dob' in data:
                        data_employee['dob'] = data['dob']
                except:
                    pass
                
                try:
                    if 'blood_group' in data:
                        data_employee['blood_group'] = data['blood_group']
                except:
                    pass
                try:
                    if 'address' in data:
                       data_employee['address'] = data['address']
                except:
                    pass
                try:
                    if 'pincode' in data:
                        data_employee['pincode'] = data['pincode']
                except:
                    pass
                
                    

                validation = EmployeePersonalInfoSerializer(data=request.data)
                if validation.is_valid():
                    employeePersonalInfo = EmployeePersonalInfo.objects.create(user=user,**data_employee)
                    employeePersonalInfo.save()

                    data_employee_financial = {}
                    employeeFinancialInfo = EmployeeFinancialInfo.objects.create(user=user,**data_employee_financial)
                    if 'pan' in data:
                        employeeFinancialInfo.pan = data['pan']
                    employeeFinancialInfo.save()

                    otp = random.randint(1000,9999)
                    userAuthentication = UserAuthentication.objects.create(user=user,is_faculty=True, is_student=False, mobile_otp=otp, is_active=True)
                    userAuthentication.save()

                    employee_id = random.randint(100000,999999)
                    form_employee_company_info = {}
                    form_employee_company_info['employee_id'] = employee_id

                    employeeCompanyInfo = EmployeeCompanyInfo.objects.create(user=user, company=request_info['company_info'].company, **form_employee_company_info)
                    employeeCompanyInfo.department_id = data['course_id']
                    employeeCompanyInfo.designation_id=data['role_id']

                    # employeeCompanyInfo.company_branch_id = data['branch_id']
                    employeeCompanyInfo.authentication = userAuthentication

                    try:
                        if 'date_of_joining' in data:
                            employeeCompanyInfo.date_of_joining = data['date_of_joining']
                    except:
                        pass

                    try:
                        if 'employment_type' in data:
                            employeeCompanyInfo.employment_type = data['employment_type']
                    except:
                        pass
                    

                    employeeCompanyInfo.save()

                    # send_employee_registration(request_info['company']['name'], data['mobile_number'])

                    details = {'id':employeeCompanyInfo.id}
                    return Response(get_success_response("Faculty Added Successfully", details=details))
                else:
                    return Response(get_validation_failure_response(validation.errors, "User with one or more provided details already exist"))
        else:
            return Response(get_validation_failure_response(validation.errors))



class AddEmployeeV1Old(APIView):
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        print("Add Employee << data================")
        print(data)
        request_info = get_user_company_from_request(request)        
        validation = AddEmployeeSerializerV1(data=request.data)
        if validation.is_valid() and request_info['company_info'] is not None and (request_info['is_admin'] or request_info['is_branch_admin']):
            if 'id' in data:
                employeeCompanyInfo = get_object_by_pk(EmployeeCompanyInfo, data['id']) 
                if employeeCompanyInfo is None:
                    return Response(get_validation_failure_response(None, "Invalid User"))

                user = employeeCompanyInfo.user
                user.first_name = data['first_name']
                if 'last_name' in data:
                    user.last_name = data['last_name']
                else:
                    user.last_name = ''

                if request_info['is_admin']:
                    user.email = data['email']
                user.save()

                employeePersonalInfo = get_first_object_by_user(EmployeePersonalInfo, user) 
                  
                employeePersonalInfo.gender = data['gender']

                if 'aadhar_number' in data:
                    employeePersonalInfo.aadhar = data['aadhar_number']

                if request_info['is_admin']:
                    employeePersonalInfo.mobile_number = data['mobile_number']
                
                if 'dob' in data:
                    employeePersonalInfo.dob = data['dob']

                if 'blood_group' in data:
                    employeePersonalInfo.blood_group = data['blood_group']

                employeePersonalInfo.save()                

                employeeFinancialInfo = get_first_object_by_user(EmployeeFinancialInfo, user) 
                if 'pan' in data:
                    employeeFinancialInfo.pan = data['pan']
                employeeFinancialInfo.save()


                employeeCompanyInfo = get_first_object_by_user(EmployeeCompanyInfo, user) 
                employeeCompanyInfo.department_id = data['department_id']
                employeeCompanyInfo.designation_id = data['designation_id'] 
                employeeCompanyInfo.company_branch_id = data['branch_id']
                
                try:
                    if 'date_of_joining' in data:
                        employeeCompanyInfo.date_of_joining = data['date_of_joining']
                except:
                    pass
                try:
                    if 'employment_type' in data:
                        employeeCompanyInfo.employment_type = data['employment_type']
                except:
                    pass

                employeeCompanyInfo.save()

                employeeAttendanceSetting = get_first_object_by_user(EmployeeAttendanceSetting, user) 
                attendance_settings = data['attendance_settings']
                employeeAttendanceSetting.start_time = attendance_settings['start_time']
                employeeAttendanceSetting.end_time = attendance_settings['end_time']
                employeeAttendanceSetting.is_excempt_allowed = attendance_settings['is_excempt_allowed']
                employeeAttendanceSetting.save()

                return Response(get_success_response("Employee Details updated Successfully"))

            else:
                if username_exists(data['email']):
                    return Response(get_validation_failure_response(None, "User with email already exist"))
                if getuser_by_mobile(data['mobile_number']) is not None:
                    return Response(get_validation_failure_response(None, "User with mobile number already exist"))

                user = User(username=data['email'], email=data['email'], password=data['email']+'@123')
                user.first_name = data['first_name']
                if 'last_name' in data:
                    user.last_name = data['last_name']
                else:
                    user.last_name = ''

                user.save()

                data_employee = {}    
                data_employee['gender'] = data['gender']
                if 'aadhar_number' in data:
                    data_employee['aadhar'] = data['aadhar_number']
                data_employee['mobile_number'] = data['mobile_number']
                try:
                    if 'dob' in data:
                        data_employee['dob'] = data['dob']
                except:
                    pass
                
                try:
                    if 'blood_group' in data:
                        data_employee['blood_group'] = data['blood_group']
                except:
                    pass
                    

                validation = EmployeePersonalInfoSerializer(data=request.data)
                if validation.is_valid():
                    employeePersonalInfo = EmployeePersonalInfo.objects.create(user=user,**data_employee)
                    employeePersonalInfo.save()

                    data_employee_financial = {}
                    employeeFinancialInfo = EmployeeFinancialInfo.objects.create(user=user,**data_employee_financial)
                    if 'pan' in data:
                        employeeFinancialInfo.pan = data['pan']
                    employeeFinancialInfo.save()

                    otp = random.randint(1000,9999)
                    userAuthentication = UserAuthentication.objects.create(user=user, mobile_otp=otp, is_active=True)
                    userAuthentication.save()

                    employee_id = random.randint(100000,999999)
                    form_employee_company_info = {}
                    form_employee_company_info['employee_id'] = employee_id

                    employeeCompanyInfo = EmployeeCompanyInfo.objects.create(user=user, company=request_info['company_info'].company, **form_employee_company_info)
                    employeeCompanyInfo.department_id = data['department_id']
                    employeeCompanyInfo.designation_id = data['designation_id']
                    employeeCompanyInfo.company_branch_id = data['branch_id']
                    employeeCompanyInfo.authentication = userAuthentication

                    try:
                        if 'date_of_joining' in data:
                            employeeCompanyInfo.date_of_joining = data['date_of_joining']
                    except:
                        pass

                    try:
                        if 'employment_type' in data:
                            employeeCompanyInfo.employment_type = data['employment_type']
                    except:
                        pass

                    employeeCompanyInfo.save()

                    form_employee_attendance_settings = data['attendance_settings']
                    associated_branch =  form_employee_attendance_settings['associated_branch']

                    send_employee_registration(request_info['company']['name'], data['mobile_number'])

                    return Response(get_success_response("User Added Successfully"))
                else:
                    return Response(get_validation_failure_response(validation.errors, "User with one or more provided details already exist"))
        else:
            return Response(get_validation_failure_response(validation.errors))


class UpdateEmployeeCheckinAssociations(APIView):
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        print("Add Employee << data================")
        print(data)
        request_info = get_user_company_from_request(request)
        validation = UpdateEmployeeCheckinAssociationsSerializer(data=request.data)
        if validation.is_valid():
            try:
                associated_branch =  data['associated_branch']
                employeeAttendanceSetting = EmployeeAttendanceSetting.objects.get(id=data['id'])
                employeeAttendanceSetting.associated_branch.clear()
                for eachb in associated_branch:
                    employeeAttendanceSetting.associated_branch.add(eachb)
                employeeAttendanceSetting.save()
                
                print("exxxxxxxxx33")
                return Response(get_success_response(None, "CheckIn Branches updated successfully"))
            except Exception as e:
                print("exxxxxxxxx")
                print(e)
                return Response(get_validation_failure_response(None, 'Invalid User'))
        else:
            return Response(get_validation_failure_response(validation.errors))

class GetEmployeeDetails(APIView):
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        print("Add Employee << data================")
        print(data)
        request_info = get_user_company_from_request(request)        
        validation = GetEmployeeDetailsSerializer(data=request.data)
        if validation.is_valid():
            try:
                employeeCompany = EmployeeCompanyInfo.objects.get(id = data['user_id']) 
                serializer = EmployeeDetailsSerializer(employeeCompany)
                employee_data = serializer.data
                print("employee_data===>sent")
                print(employee_data)
                return Response(get_success_response(None, "", employee_data))
            except Exception as e:
                print("exxxxxxxxx")
                print(e)
                return Response(get_validation_failure_response(None, 'Invalid user'))
        else:
            return Response(get_validation_failure_response(validation.errors))

class GetEmployeeCheckinAssociations(APIView):
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        print("Add Employee << data================")
        print(data)
        request_info = get_user_company_from_request(request)        
        validation = GetEmployeeDetailsSerializer(data=request.data)
        if validation.is_valid():
            try:
                employeeCompany = EmployeeCompanyInfo.objects.get(id = data['user_id']) 
                response_data = {}
                associated_branches = []
                employeeAttendanceSetting = EmployeeAttendanceSetting.objects.get(user=employeeCompany.user)
                response_data['id'] = employeeAttendanceSetting.id
                response_data['branch_id'] = employeeCompany.company_branch.id
                for associated_branch in employeeAttendanceSetting.associated_branch.all():
                    each_branch =  {"name":associated_branch.display_name, "id":associated_branch.id}
                    associated_branches.append(each_branch)
                response_data['associated_branch'] = associated_branches
                return Response(get_success_response(None, "", response_data))
            except Exception as e:
                print("exxxxxxxxx")
                print(e)
                return Response(get_validation_failure_response(None, 'Invalid user'))
        else:
            return Response(get_validation_failure_response(validation.errors))


# ================

class RaiseAnonymousComplaint(APIView):
    
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        data = request.data
        request_info = get_user_company_from_request(request)        
        validation = RaiseAnonymousComplaintSerializer(data=data)
        if validation.is_valid() and request_info['company_info']:
            employeeCompanyInfo=EmployeeCompanyInfo.objects.get(id = request_info['employee_id'])
            form_AnonymousComplaint = {}
            form_AnonymousComplaint['title'] = data['title']
            if employeeCompanyInfo.authentication.is_faculty:
                form_AnonymousComplaint['user_type'] =AnonymousComplaintTicket.FACULTY
            elif employeeCompanyInfo.authentication.is_admin:
                form_AnonymousComplaint['user_type']=AnonymousComplaintTicket.ADMIN
            else:
                form_AnonymousComplaint['user_type']=AnonymousComplaintTicket.STUDENT
            form_AnonymousComplaint['ticket_status'] = AnonymousComplaintTicket.RAISED
            form_AnonymousComplaint['description'] = data['description']
            form_AnonymousComplaint['brand_branch'] = request_info['company_info'].company_branch
            form_AnonymousComplaint['code'] = str((random.randint(1000000000,9999999999)))
            form_AnonymousComplaint['tags'] = data['tags']

            AnonymousComplaintTicket.objects.create(**form_AnonymousComplaint)
            return Response(get_success_response("Anonymous complaint raised successfully"))
        else:
            return Response(get_validation_failure_response(validation.errors))

