from django.contrib.auth.models import User
from authentication.models import UserAuthentication, UserCredentialValidation
from rest_framework.authtoken.models import Token
from employee.models import EmployeeCompanyInfo, EmployeePersonalInfo
from company.models import CompanyBranchInfo
import random
from django.utils import timezone
import base64
from django.core.files.base import ContentFile
from authentication.message_utils import send_company_registration_OTP, send_company_login_OTP
from django.core.paginator import Paginator

from rest_framework.response import Response
from authentication.response_serializer import get_validation_failure_response, get_success_response

def set_mobile_otp_registation(mobile_number):
            userCredentialValidation = {}
            userCredentialValidation['mobile_number'] = mobile_number
            otp = 1234 
            # random.randint(1000,9999)
            userCredentialValidation['mobile_otp'] = otp
            otp_expiry = timezone.now() + timezone.timedelta(minutes = 2)
            current_tz = timezone.get_current_timezone() 
            userCredentialValidation['otp_expiry'] = otp_expiry 
            UserCredentialValidation.objects.create(**userCredentialValidation)

def set_mobile_otp_registation_customer(mobile_number):
            userCredentialValidation = {}
            userCredentialValidation['mobile_number'] = mobile_number
            otp = 1234 
            # random.randint(1000,9999)
            userCredentialValidation['mobile_otp'] = otp
            otp_expiry = timezone.now() + timezone.timedelta(minutes = 2)
            current_tz = timezone.get_current_timezone() 
            userCredentialValidation['otp_expiry'] = otp_expiry 
            UserCredentialValidation.objects.create(**userCredentialValidation)


def set_mobile_otp(userAuthentication, is_login):
    
    is_local = True
    otp = random.randint(1000,9999)
    # try:
    #     employeePersonalInfo = EmployeePersonalInfo.objects.get(user=userAuthentication.user)
    #     if employeePersonalInfo.mobile_number == '8342999555':
    #         otp = 1234
    # except:
    #     pass
    
    if is_local:
        otp = 1234

    userAuthentication.mobile_otp = otp
    otp_expiry = timezone.now() + timezone.timedelta(minutes = 2)
    current_tz = timezone.get_current_timezone() 
    userAuthentication.otp_expiry = otp_expiry 
    userAuthentication.save()

    if is_local == False:
        try:
            employeePersonalInfo = EmployeePersonalInfo.objects.get(user=userAuthentication.user)
            if is_login:
                send_company_login_OTP(userAuthentication.user.first_name, employeePersonalInfo.mobile_number, otp)
            else:
                send_company_registration_OTP(userAuthentication.user.first_name, employeePersonalInfo.mobile_number, otp)
        except Exception as e:
            print("exceeppp")
            print("eee",e)
            pass

def get_paginated_objects(objects, page_number, page_count=30):

    p = Paginator(objects, page_count)  # creating a paginator object

    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj, 'num_pages':p.num_pages}
    print(context)
    return context


def get_paginated_results_set(objects, serializer, page_number, page_count):

    response = {}
    response['total'] = objects.count()

    page_obj = get_paginated_objects(objects, page_number, page_count)
    response['num_pages'] = page_obj['num_pages']
    
    if page_obj['page_obj'].has_next():
        response['next_page'] = page_number+1
    else:
        response['next_page'] = -1
    
    response['data'] = serializer(page_obj['page_obj'], many=True).data

    return response

def get_paginated_results_set_ser_fun(objects, serializer, page_number, page_count, extra_data, functionpost):

    response = {}
    response['total'] = objects.count()

    page_obj = get_paginated_objects(objects, page_number, page_count)
    response['num_pages'] = page_obj['num_pages']
    
    if page_obj['page_obj'].has_next():
        response['next_page'] = page_number+1
    else:
        response['next_page'] = -1
    # response['has_previous'] = page_obj.has_previous()
    response['data'] = serializer(page_obj['page_obj'], many=True).data

    return response

def check_if_exist_count(model, query):
    try:
        return model.objects.filter(**query).count()
    except Exception as e:
        print("exxxx=====================================================s")
        print(e)
        return 0

def check_if_exist(model, query):
    try:
        # print(query)
        if model.objects.filter(**query).exists():
            return True
        return False
    except Exception as e:
        print("exxxx=====================================================s")
        print(e)
        return False


def get_first_object_by_user(model, user):
    try:
        obj = model.objects.filter(user = user)
        if obj.count()>0:
            return obj.first()            
        return None
    except:
        return None

def username_exists(username):
    if User.objects.filter(username=username).exists():
        return True
    return False

def getuser_from_params(params):
    res = None
    try:
        if 'email' in params:   
            return getuser_by_email(params['email'])
        if 'mobile_number' in params:   
            return getuser_by_mobile(params['mobile_number'])
    except:
        return None
    return res

def getuser_by_email(username):
    try: 
        return User.objects.get(username=username)
    except:
        return None


def get_user_by_id(pk):
    try: 
        return User.objects.get(pk=pk)
    except:
        return None

def get_object_by_pk(model, pk):
    try: 
        return model.objects.get(pk=pk)
    except:
        return None

def getuser_by_mobile(username):
    try: 
        ep =  EmployeePersonalInfo.objects.get(mobile_number = username) 
        return ep.user
    except:
        return None

def get_active_user(**kargs):
    try: 
        return UserAuthentication.objects.get(**kargs)
    except:
        return None

def get_user_token(username):
    try:
        user = User.objects.get(username = username)
        try:
            token = Token.objects.get(user=user)
            return token.key
        except:
            token = Token.objects.create(user=user)
            return token.key
    except:
        return None

def get_user_from_request(request):
    token = request.META.get('HTTP_AUTHORIZATION') 
    token = token.replace("Token ", "")
    try:
        user = Token.objects.get(key=token).user
        return user
    except:
        return None

def get_user_company_from_request(request):
    response = {
        "user":None,
        "company_info":None,
        "is_admin":False,
        'is_branch_admin':False
    }

    try:
        token = request.META.get('HTTP_AUTHORIZATION') 
        print("token")
        print(token)
        token = token.replace("Token ", "")

        try:
            user = Token.objects.get(key=token).user
            response = get_user_company_from_user(user)                            
        except:
            pass
    except:
        pass
    return response

def get_user_company_from_user(user):                

    response = {
        "user":None,
        "company_info":None,
        "is_admin":False,
        'is_branch_admin':False,
        'has_company':False,
        'has_company_branch_location':False,
        'company':None,
        'company_branch':None,
        'company_branch_location':None,
        'can_update_location':False
    }
    
    try:
        response['user'] = user
        user_auth = get_active_user(user=user)
        response['is_admin'] = user_auth.is_active and user_auth.is_admin
        response['designation'] = '-'
        try:
            employee_company_info = EmployeeCompanyInfo.objects.get(user = user)
            response['company_info'] = employee_company_info

            employee_personal_info = EmployeePersonalInfo.objects.get(user = user)
            response['personal_info'] = employee_personal_info
                        
            try:
                response['is_branch_admin'] = user_auth.is_active and employee_company_info.designation.is_admin
                response['designation'] = employee_company_info.designation.name
            except:
                pass
            response['has_company'] = True
            response['company'] = {"name":employee_company_info.company.brand_name, "id":employee_company_info.company.id}
            response['company_branch'] = {"name":employee_company_info.company_branch.name, "id":employee_company_info.company_branch.id}
            
            response['can_update_location'] =  employee_company_info.company_branch.can_update_location

            if employee_company_info.company_branch.company_geolocation is not None:
                response['has_company_branch_location'] = True
                company_geolocation = employee_company_info.company_branch.company_geolocation    
                response['company_branch_location'] = {'id':company_geolocation.id, "location_latitude":company_geolocation.location_latitude, "location_longitude":company_geolocation.location_longitude, 'fencing_radius': company_geolocation.fencing_radius}
            
        except  Exception as e: 
            print(e)
            response['has_company'] = False
            pass

    except:
        pass

    print("responseresponseresponseHeader=======================")
    print(response)
    return response

def get_attachment(data, key):
    response = {}
    response['has_attachment'] = False
    if key in data:
        attachment = data[key]
        if attachment[-1] == '/':            
            file_name = 'a'+str(random.randint(1000,9999))+".png"
        else:
            file_name = 'a'+str(random.randint(1000,9999))+".jpg"

        data = ContentFile(base64.b64decode(attachment))
        response['file_name'] = file_name
        response['file'] = data
        response['has_attachment'] = True
    return response

def get_user_from_request(request_info, data):
    user = request_info['user']
    if 'user_id' in data:
        try:
            employeeCompanyInfo = get_object_by_pk(EmployeeCompanyInfo, data['user_id'])
            user = employeeCompanyInfo.user
        except:
            pass
    return user

class ValidateRequest():

    def __init__(self, request, request_serializer=None):

        self.request = request
        self.request_data = request.data
        print("22232rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr", request.data)
        self.request_info = get_user_company_from_request(request)
        print("32232rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr", self.request_info)

        self.request_serializer = request_serializer
        self.errors = {}

    def employee_company_info(self):
        return self.request_info['company_info']

    def employee_personal_info(self):
        employee_personal_info = EmployeePersonalInfo.objects.get(user = self.request_info['user'])
        print('employee_personal_info=====', employee_personal_info.id)
        return employee_personal_info 

    def is_admin(self):
        if self.is_valid():
            userAuthentication = UserAuthentication.objects.get(user = self.request_info['user'])
            return userAuthentication.is_admin and userAuthentication.is_active 
        return False
        
    def is_valid_open_request(self):
        if self.request_serializer is not None:
            print("444", self.request_data)
            request_serializer_response = self.request_serializer(data=self.request_data)
            if request_serializer_response.is_valid() == True:
                print("35444", self.request_data)

                return True
            else:
                print("5444", self.request_data)

                self.errors = request_serializer_response.errors
                print("errors======", request_serializer_response.errors)
        return False

    def is_valid(self):
        print("001")
        if self.is_valid_user() == False:
            print("002")

            return False
        elif self.request_serializer is not None:
            print("444", self.request_data)
            request_serializer_response = self.request_serializer(data=self.request_data)
            if request_serializer_response.is_valid() == True:
                return True
            else:
                print("003")

                self.errors = request_serializer_response.errors
                print("errors======", request_serializer_response.errors)
                return False
        else:
            print("004")

            return True


    def is_valid_user(self):
        if self.request_info['company_info']:
            return True
        else:
            return False

    def is_valid_admin(self):
        if self.request_info['company_info']:
            if self.request_info['is_admin']:
                return True
        return False

    def is_valid_branch_admin(self):
        if self.is_valid() == False:
            return False
        if self.request_info['company_info'] or self.request_info['is_branch_admin']:
            if self.request_info['is_admin']:
                return True
        return False

    def errors(self):
        return self.errors

    def errors_formatted(self):
        return "Invalid Request Info"
        # self.errors


def create_update_model_response(model_class, data={}, update_to_q = {}, unique_fields=[], unique_q_extra_pram = {}):

    create_update_model_response = create_update_model(model_class, data, update_to_q, unique_fields, unique_q_extra_pram)
    if create_update_model_response['status'] == True:
            return Response(get_success_response(message=create_update_model_response['message']))
    else:
        return Response(get_validation_failure_response(None,error_message = create_update_model_response['error'] ))

def create_update_model(model_class, data={}, update_to_q = {}, unique_fields=[], unique_q_extra_pram = {}):

    response = {}
    response['status'] = False
    
    '''
    creating a new record
    '''
    if 'id' not in data and update_to_q == {}:
        try:
            model_class_instance = model_class.objects.create(**data)
            response['status'] = True
            response['message'] = 'Details created successfully'
            return response
        except Exception as e:
            print("eeeee", e)
            response['error'] = "Error creating Record"
            return response

    else:

        if update_to_q == {}:
           update_to_q = {'id':data['id']}
           del data['id']
            
        if check_if_exist(model_class, update_to_q) == True:
        
            for f in unique_fields:
                obj_c = {f:data[f]}
                print("=======qqqqqq", obj_c)
                count = model_class.objects.filter(**obj_c, **unique_q_extra_pram).exclude(**update_to_q).count()
                if count > 0:
                    response['error'] = '' + f + ' with the given value already exist'
                    return response
            model_class_instance = model_class.objects.filter(**update_to_q)
            model_class_instance.update(**data)
            response['status'] = True
            response['message'] = 'Details updated successfully'
            return response

        response['error'] = "Matching Data doesn't exist"
        return response
        # for k, v in data.items():
        #     setattr(brandBranchService, k, v)
        # brandBranchService.save()

