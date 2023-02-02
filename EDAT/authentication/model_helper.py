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
import uuid

def set_mobile_otp_registation(mobile_number):
    userCredentialValidation = {}
    userCredentialValidation['mobile_number'] = mobile_number
    otp = 1234
    # random.randint(1000,9999)
    userCredentialValidation['mobile_otp'] = otp
    otp_expiry = timezone.now() + timezone.timedelta(minutes=2)
    current_tz = timezone.get_current_timezone()
    userCredentialValidation['otp_expiry'] = otp_expiry
    UserCredentialValidation.objects.create(**userCredentialValidation)


def set_mobile_otp_registation_customer(mobile_number):
    userCredentialValidation = {}
    userCredentialValidation['mobile_number'] = mobile_number
    otp = 1234
    # random.randint(1000,9999)
    userCredentialValidation['mobile_otp'] = otp
    otp_expiry = timezone.now() + timezone.timedelta(minutes=2)
    current_tz = timezone.get_current_timezone()
    userCredentialValidation['otp_expiry'] = otp_expiry
    UserCredentialValidation.objects.create(**userCredentialValidation)


def set_mobile_otp(userAuthentication, is_login):

    is_local = True
    otp = random.randint(1000, 9999)
    # try:
    #     employeePersonalInfo = EmployeePersonalInfo.objects.get(user=userAuthentication.user)
    #     if employeePersonalInfo.mobile_number == '8342999555':
    #         otp = 1234
    # except:
    #     pass

    if is_local:
        otp = 1234

    userAuthentication.mobile_otp = otp
    otp_expiry = timezone.now() + timezone.timedelta(minutes=2)
    current_tz = timezone.get_current_timezone()
    userAuthentication.otp_expiry = otp_expiry
    userAuthentication.save()

    if is_local == False:
        try:
            employeePersonalInfo = EmployeePersonalInfo.objects.get(
                user=userAuthentication.user)
            if is_login:
                send_company_login_OTP(
                    userAuthentication.user.first_name, employeePersonalInfo.mobile_number, otp)
            else:
                send_company_registration_OTP(
                    userAuthentication.user.first_name, employeePersonalInfo.mobile_number, otp)
        except Exception as e:
            print("exceeppp")
            print("eee", e)
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
    context = {'page_obj': page_obj, 'num_pages': p.num_pages}
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
        obj = model.objects.filter(user=user)
        if obj.count() > 0:
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
        ep = EmployeePersonalInfo.objects.get(mobile_number=username)
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
        user = User.objects.get(username=username)
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
        "user": None,
        "company_info": None,
        "is_admin": False,
        'is_branch_admin': False
    }
    print("tokensss")
    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        print("token")
        print(token)
        token = token.replace("Token ", "")
        print("token=====>", token)
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
        "user": None,
        "company_info": None,
        "employee_id" : None,
        "is_admin": False,
        'is_branch_admin': False,
        'has_company': False,
        'has_company_branch_location': False,
        'company': None,
        'company_branch': None,
        'company_branch_location': None,
        'can_update_location': False,
        'photo':None,
        'name':None,
        'mobile_number':None
    }

    try:
        response['user'] = user
        user_auth = get_active_user(user=user)
        response['is_admin'] = user_auth.is_active and user_auth.is_admin
        response['designation'] = '-'
        try:
            employee_company_info = EmployeeCompanyInfo.objects.get(user=user)
            response['company_info'] = employee_company_info
            response['employee_id'] = employee_company_info.id
            response['photo'] = employee_company_info.photo.url
            response['name'] = employee_company_info.user.username
            

            employee_personal_info = EmployeePersonalInfo.objects.get(
                user=user)
            response['personal_info'] = employee_personal_info
            response['mobile_number'] = employee_personal_info.mobile_number

            try:
                response['is_branch_admin'] = user_auth.is_active and employee_company_info.designation.is_admin
                response['designation'] = employee_company_info.designation.name
            except:
                pass
            response['has_company'] = True
            response['company'] = {
                "name": employee_company_info.company.brand_name, "id": employee_company_info.company.id, 'type_is_provider': employee_company_info.company.type_is_provider}
            response['company_branch'] = {
                "name": employee_company_info.company_branch.name, "id": employee_company_info.company_branch.id}

            response['can_update_location'] = employee_company_info.company_branch.can_update_location

            if employee_company_info.company_branch.company_geolocation is not None:
                response['has_company_branch_location'] = True
                company_geolocation = employee_company_info.company_branch.company_geolocation
                response['company_branch_location'] = {'id': company_geolocation.id, "location_latitude": company_geolocation.location_latitude,
                                                       "location_longitude": company_geolocation.location_longitude, 'fencing_radius': company_geolocation.fencing_radius}

        except Exception as e:
            print(e)
            response['has_company'] = False
            pass

    except:
        pass

    print("responseresponseresponseHeader=======================")
    print(response)
    return response



def get_user_from_request(request_info, data):
    user = request_info['user']
    if 'user_id' in data:
        try:
            employeeCompanyInfo = get_object_by_pk(
                EmployeeCompanyInfo, data['user_id'])
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
        employee_personal_info = EmployeePersonalInfo.objects.get(
            user=self.request_info['user'])
        print('employee_personal_info=====', employee_personal_info.id)
        return employee_personal_info

    def is_admin(self):
        print("c0001")
        if self.is_valid():
            print("c00013")
            userAuthentication = UserAuthentication.objects.get(
                user=self.request_info['user'])
            print("c00014")
            return userAuthentication.is_admin
        # and userAuthentication.is_active
        return False

    def is_valid_open_request(self):
        if self.request_serializer is not None:
            print("444", self.request_data)
            request_serializer_response = self.request_serializer(
                data=self.request_data)
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
            request_serializer_response = self.request_serializer(
                data=self.request_data)
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

def get_attachment(data, key):
    response = {}
    response['has_attachment'] = False
    if key in data:
        attachment = data[key]
        if attachment[-1] == '/':
            file_name = 'a'+str(random.randint(1000, 9999))+".png"
        else:
            file_name = 'a'+str(random.randint(1000, 9999))+".jpg"

        data = ContentFile(base64.b64decode(attachment))
        response['file_name'] = file_name
        response['file'] = data 
        response['has_attachment'] = True
    return response

def create_update_model_response(model_class, data={}, update_to_q={}, unique_fields=[], unique_q_extra_pram={}, api_instance=None):

    create_update_model_response = create_update_model(
        model_class, data=data, update_to_q=update_to_q, unique_fields=unique_fields, unique_q_extra_pram=unique_q_extra_pram, api_instance=api_instance)
    if create_update_model_response['status'] == True:
        return Response(get_success_response(message=create_update_model_response['message'], details=create_update_model_response['ids']))
    else:
        return Response(get_validation_failure_response(None, error_message=create_update_model_response['error']))

def create_update_model(model_class, data={}, update_to_q={}, unique_fields=[], unique_q_extra_pram={}, api_instance=None):

    response = {}
    response['status'] = False

    model_columns = map(
        lambda model_column: model_column.name, model_class._meta.fields)

    model_columns_types = map(
        lambda model_column: model_column.get_internal_type(), model_class._meta.fields)
    many_to_many_fields = model_class.many_to_many_fields

    # model_class_i = model_class()
    # print("====aassd1", model_class.many_to_many_fields)
    # # ((model_class._meta.many_to_many.remote_field)))
    # print("====aassd1", list(model_columns))
    # print("====aassd", list(model_columns_type))


    model_columns_l = list(model_columns)
    model_columns_types_l = list(model_columns_types)

    file_fields = []
    file_field_data = {}

    '''seperating base64 file values from data '''
    for i, v in (enumerate(model_columns_types_l)):
        if v == 'FileField' or v == 'ImageField':
            file_fields.append(model_columns_l[i])
            if model_columns_l[i] in data:
                file_field_data[model_columns_l[i]] = data[model_columns_l[i]]  
                del data[model_columns_l[i]]

    print("dfsfdddd", file_fields)

    default_meta_params = {}

    if 'company' in model_columns and 'company_id' not in data:
        default_meta_params['company_id'] = api_instance.get_employee_company_info(
        ).company.id

    if 'company_branch' in model_columns and 'company_branch_id' not in data:
        default_meta_params['company_branch_id'] = api_instance.get_employee_company_info(
        ).company_branch.id

    if 'employee_company' in model_columns and 'employee_company_id' not in data:
        default_meta_params['employee_company'] = api_instance.get_employee_company_info(
        ).id

    many_to_many_datas = {}

    for many_to_many_field in many_to_many_fields:
        data_key = many_to_many_field+'_ids'
        if data_key in data:
            many_to_many_datas[many_to_many_field] = data[data_key]
            del data[data_key]

    '''
    creating a new record
    '''
    if 'id' not in data and update_to_q == {}:
        print("came createe2")

        try:
            model_class_instance = model_class.objects.create(
                **data, **default_meta_params)
            model_class_instance.save()

            
            '''handling file fields'''
            for file_field_name in file_fields:
                print("file_field_namefile_field_name====================", file_field_name)
                if file_field_name in file_field_data: 
                    e_file_field = get_attachment(file_field_data, file_field_name)
                    if e_file_field is not None:
                            file_field_i = getattr(model_class_instance, file_field_name)                        
                            file_field_i.save(e_file_field['file_name'], e_file_field['file'], save=True)

            '''handling many to many'''
            if many_to_many_datas != {}:

                for key in many_to_many_datas:
                    print("fdsfdsfsdf", key)
                    print("fdsfdsfsdf",  many_to_many_datas[key])
                    model_class_instance_m = getattr(model_class_instance, key)
                    '''to add in many to many'''
                    if 'add' in many_to_many_datas[key]:
                        to_add = many_to_many_datas[key]['add']
                        for value_id in to_add:
                            model_class_instance_m.add(value_id)

                    if 'create_update' in many_to_many_datas[key]:
                        print("555444")
                        create_update_records = many_to_many_datas[key]['create_update']
                        for create_update_item in create_update_records:
                            class_in = model_class_instance.get_many_to_many_class(
                                key)
                            print("555444333", class_in, create_update_item)
                            class_in_instance = create_update_model(
                                class_in, data=create_update_item, api_instance=api_instance)
                            print("fdsdfdsddd", class_in_instance)
                            class_in_instance_ids = class_in_instance['ids']
                            for class_in_instance_id in class_in_instance_ids:
                                model_class_instance_m.add(
                                    class_in_instance_id)

            response['ids'] = []
            response['ids'].append(model_class_instance.id)
            response['status'] = True
            response['message'] = 'Details created successfully'
            return response
        except Exception as e:
            print("eeeee", e)
            response['error'] = "Error creating Record"
            return response

    else:
        print("came createe")

        if update_to_q == {}:
            update_to_q = {'id': data['id']}
            del data['id']

        response['ids'] = []

        if check_if_exist(model_class, update_to_q) == True:

            for f in unique_fields:
                obj_c = {f: data[f]}
                print("=======qqqqqq", obj_c)
                count = model_class.objects.filter(
                    **obj_c, **unique_q_extra_pram).exclude(**update_to_q).count()
                if count > 0:
                    response['error'] = '' + f + \
                        ' with the given value already exist'
                    return response
            model_class_instance = model_class.objects.filter(**update_to_q)
            model_class_instance.update(**data, **default_meta_params)
            for model_class_instance_e in model_class_instance:
                response['ids'].append(model_class_instance_e.id)
            
            '''handling file fields'''

            model_class_instances = model_class_instance 
            for file_field_name in file_fields:
                print("file_field_namefile_field_name====================", file_field_name)
                if file_field_name in file_field_data: 
                    e_file_field = get_attachment(file_field_data, file_field_name)
                    if e_file_field is not None:
                        for model_class_instance in model_class_instances:
                            file_field_i = getattr(model_class_instance, file_field_name)                        
                            file_field_i.save(e_file_field['file_name'], e_file_field['file'], save=True)


            '''handling many to many'''
            if many_to_many_datas != {} and model_class_instance.count() > 0:

                for model_class_instance_i in model_class_instance:
                    for key in many_to_many_datas:
                        model_class_instance_m = getattr(
                            model_class_instance_i, key)
                        '''to add in many to many'''
                        if 'add' in many_to_many_datas[key]:
                            to_add = many_to_many_datas[key]['add']
                            for value_id in to_add:
                                model_class_instance_m.add(value_id)

                        '''to remove in many to many'''
                        if 'remove' in many_to_many_datas[key]:
                            to_add = many_to_many_datas[key]['remove']
                            for value_id in to_add:
                                model_class_instance_m.remove(value_id)

                        if 'create_update' in many_to_many_datas[key]:
                            create_update_records = many_to_many_datas[key]['create_update']
                            for create_update_item in create_update_records:
                                class_in = model_class_instance_i.get_many_to_many_class(
                                    key)
                                class_in_instance = create_update_model(
                                    class_in, data=create_update_item, api_instance=api_instance)
                                class_in_instance_ids = class_in_instance['ids']
                                for class_in_instance_id in class_in_instance_ids:
                                    model_class_instance_m.add(
                                        class_in_instance_id)

            response['status'] = True
            response['message'] = 'Details updated successfully'
            return response

        response['error'] = "Matching Data doesn't exist"
        return response

def get_file_name():    
    return "file-" + str(uuid.uuid4())

def get_attachment(data, key):
    response = {}
    response['has_attachment'] = False
    try:
        if key in data:
            attachment = data[key]

            start_letter = attachment[0:1]              
            if start_letter == 'J':           
                print("============02", attachment[-1])                                   
                file_name = get_file_name()+".pdf"

            elif start_letter == '/':            
                file_name = get_file_name()+".png"
            else:
                file_name = get_file_name()+".jpg"
            data = ContentFile(base64.b64decode(attachment))
            response['file_name'] = file_name
            response['file'] = data
            response['has_attachment'] = True
    except:
        pass
    return response
