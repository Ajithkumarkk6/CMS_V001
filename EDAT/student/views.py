from django.shortcuts import render
from mmap import PAGESIZE
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .response_serializer import *
from .model_helper import *
import random
from authentication.model_helper import (ValidateRequest, get_active_user, get_user_by_id,
                           get_user_company_from_request,get_object_by_pk,
                           get_user_company_from_user, get_user_from_request,
                           get_user_token, getuser_by_email, getuser_by_mobile,
                           getuser_from_params, set_mobile_otp, set_mobile_otp_registation, set_mobile_otp_registation_customer,
                           username_exists)

from authentication.custom_api_views import GenericAPIView, GenericListAPIView, GenericCrudApiView, GenericItemDetailApiView
# get_paginated_results_set
from authentication.response_serializer import (get_success_response,
                                  get_validation_failure_response)
from .request_serializer import *


from django.shortcuts import render
import json
from django.http import JsonResponse
import openai

openai.api_key = "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"


class GetStudents(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_EMPLOYEE
    request_serializer = None
    list_serializer = GetStudentsSerializer
    per_page_count = -1

    def get_list_query(self):
        if self.get_employee_company_info() is not None:
            return get_students(self.get_employee_company_info().company.id)

class GetStudentDetails(GenericItemDetailApiView):

    access_rights = GenericAPIView.ACCESS_TYPE_EMPLOYEE
    request_serializer = None
    item_serializer= GetStudentsDetailedSerializer
    per_page_count = -1

    def get_item_query(self):
        if self.get_employee_company_info() is not None:
            return get_students_details(self.payload['student_id'])

class GetFacultyDetails(GenericItemDetailApiView):

    access_rights = GenericAPIView.ACCESS_TYPE_EMPLOYEE
    request_serializer = None
    item_serializer= GetFacultiesSerializer
    per_page_count = -1

    def get_item_query(self):
        if self.get_employee_company_info() is not None:
            return get_faculty_details(self.payload['faculty_id'])



class GetFaculties(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_EMPLOYEE
    request_serializer = None
    list_serializer = GetFacultiesSerializer
    per_page_count = -1

    def get_list_query(self):
        if self.get_employee_company_info() is not None:
            return get_faculties(self.get_employee_company_info().company.id)




class GetStudentCourses(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_EMPLOYEE
    request_serializer = None
    list_serializer = GetStudentCoursesSerializer
    per_page_count = -1

    def get_list_query(self):
        if self.get_employee_company_info() is not None:
            return get_student_courses(self.get_employee_company_info().id)

class GetStudentCourseSections(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_EMPLOYEE
    request_serializer = None
    list_serializer = GetStudentCourseSectionsSerializer
    per_page_count = -1

    def get_list_query(self):
        if self.get_employee_company_info() is not None:
            self.serializer_extra_data = {"student_course_id": self.payload['student_course_id']}
            return get_student_course_sections(self.payload['student_course_id'])


class GetStudentCourseTopics(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_EMPLOYEE
    request_serializer = None
    list_serializer = GetStudentCourseTopicsSerializer
    per_page_count = -1

    def get_list_query(self):
        if self.get_employee_company_info() is not None:
            self.serializer_extra_data = {"course_section_id": self.payload['course_section_id'], 'student_id':self.get_employee_company_info().id}
            return get_student_course_topic(self.payload['course_section_id'])

class GetStudentCourseTasks(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_EMPLOYEE
    request_serializer = None
    list_serializer = GetStudentCourseTasksSerializer
    per_page_count = -1

    def get_list_query(self):
        if self.get_employee_company_info() is not None:
            self.serializer_extra_data = {"course_topic_id": self.payload['course_topic_id'], 'student_id':self.get_employee_company_info().id}
            return get_student_course_tasks(self.payload['course_topic_id'])


class GetStudentCourseTaskDetails(GenericItemDetailApiView):

    access_rights = GenericAPIView.ACCESS_TYPE_EMPLOYEE
    request_serializer = None
    item_serializer = GetStudentCourseTaskSerializer

    def get_item_query(self):
        if self.get_employee_company_info() is not None:
            return get_student_course_task(self.payload['student_task_id'])




class GetRefferer(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_EMPLOYEE
    request_serializer = None
    list_serializer = GetReferrerSerializer
    per_page_count = -1

    def get_list_query(self):
        if self.get_employee_company_info() is not None:
            return get_referrer(self.get_employee_company_info().company.id)


class GetApprover(GenericListAPIView):

    access_rights = GenericAPIView.ACCESS_TYPE_EMPLOYEE
    request_serializer = None
    list_serializer = GetApproverSerializer
    per_page_count = -1

    def get_list_query(self):
        if self.get_employee_company_info() is not None:
            return get_approver(self.get_employee_company_info().company.id)


class AddStudentCourseTask(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        print(data)
        request_info = get_user_company_from_request(request)        

        validation = AddStudentCourseTaskSerializer(data=request.data)
        if validation.is_valid() and request_info['company_info'] is not None:
            if 'id' not in data:
                course_task_id = data['course_task_id']
                student_id = request_info['company_info'].id
                task = Task.objects.get(id = course_task_id)
                course = task.topic.course
                studentCourse =StudentCourse.objects.get(employee_company__id = student_id, course__id = course.id)

                '''check if student topic exist  if not create new'''
                try:
                    studentCourseTopic = StudentCourseTopic.objects.get(course_topic__id = task.topic.id, employee_company__id = student_id)
                except:
                    course_section =task.topic.course_section
                    course_topic=task.topic
                    '''check if student course section exist'''
                    try:
                        studentCourseSection = StudentCourseSection.objects.get(course_section__id = course_section.id, employee_company__id = student_id)
                    except:
                        studentCourseSectionForm = {}
                        studentCourseSectionForm['course_section_id'] = course_section.id
                        studentCourseSectionForm['student_course_item'] = studentCourse
                        studentCourseSectionForm['employee_company_id'] = student_id
                        studentCourseSection = StudentCourseSection.objects.create(**studentCourseSectionForm)


                        studentCourseTopicForm = {}
                        studentCourseTopicForm['course_topic_id']=course_topic.id
                        studentCourseTopicForm['student_course_section']=studentCourseSection.id
                        studentCourseTopicForm['employee_company_id'] = student_id
                        studentCourseTopicForm['student_course_item'] = studentCourse
                        StudentCourseTopic.objects.create(**studentCourseTopicForm)

                studentCourseTaskForm = data
                studentCourseTaskForm['employee_company']=request_info['company_info']
                studentCourseTaskForm['student_course_item']= studentCourse
                studentCourseTaskForm['course_task'] =task

                StudentCourseTask.objects.create(**studentCourseTaskForm)
                return Response("Student Course Task created successfully")


            # else:
            #     StudentCourseTaskForm['start_date']=data['start_date']
            #     StudentCourseTaskForm['base_status']=data['base_status']
            #     StudentCourseTaskForm['is_inprogress']=data['is_inprogress']
            #     StudentCourseTaskForm['approver_id']=data['approver_id']
            #     StudentCourseTaskForm['student_course_topic_id']=data['student_course_topic_id']
            #     StudentCourseTaskForm['course_task_id']=data['course_task_id']
            #     StudentCourseTaskForm['formulated_question']=data['formulated_question']
            #     StudentCourseTaskForm['procedure']=data['procedure']
            #     StudentCourseTaskForm['flow_diagram']=data['flow_diagram']
            #     StudentCourseTaskForm['program']=data['program']
            #     StudentCourseTaskForm['employee_company']=request_info['company_info']
            #     StudentCourseTaskForm['student_course_item']= studentCourse
            #     studentCourseTask=StudentCourseTask.objects.create(**StudentCourseTaskForm)


            # studentCourse= StudentCourse.objects.get(id=data['student_course_item_id'])



          


                
        else:
                return Response("error creating record")




           
           
            
            
            # user = User(
            #     username=data['email'], email=data['email'], password=data['email']+'@123')
            # user.first_name = data['first_name']
            # user.last_name = data['last_name']
            # user.save()

            # data_employee = {}
            # data_employee['gender'] = data['gender']
            # data_employee['mobile_number'] = data['mobile_number']

            # employeePersonalInfo = EmployeePersonalInfo.objects.create(
            #     user=user, **data_employee)
            # employeePersonalInfo.save()

            # userAuthentication = UserAuthentication.objects.create(user=user)
            # userAuthentication.admin_registration_designation = "Business Owner"
            # #  data['designation']
            # userAuthentication.is_admin = True
            # userAuthentication.is_active = True
            # userAuthentication.save()

            # set_mobile_otp(userAuthentication, is_login=False)

            # token = get_user_token(user.username)
            # response = {"success": True, "token": token,
        #     #             "message": "Admin registered Successfully"}

        

















promt1 = 'Prepare a question for "JavaScript - for loop" concept without involving Array,Object,JSON concepts topic and logical reasoning are the main criteria for formulating the question complexity topic represent concept, the complexity based on the variants of concept and how intensly to use it, where as logical reasoning represent the critical thinking ability required for the solving the problem lets take complexity for question for the question 1. topic as 9/10 2. logical reasoning as 10/10 Please maintain the above complexity by provided above value Each question should have these 9 parts to it 1.Problem Statement 2.Proceduce 3.Programming Procedure 4.Sample Input/Output 5.Flow Diagram 6. Snippets 7.Program 8.Tag 9.severity 10.sub_variants Dont take question context from the JSON references mentioned below. Problem statement should not have any relation and context to the previous questions generated and should not have any analogy similar to the previously generated questions and should have userpersona asked in the previously prepared questions. 1.Problem statement with the straigh forward generic lifestyle analogy that can be perceived by Indians and keep the problem statement words as plain minimal general english without any complex words and without any industry specific terminology. Problem statement should me minimum of 150 words. All the necessary inputs are pre given and problem statement should not involve any runtime input. If runtime input is required, it will be considered as a sample input 2.Procedure should not contain programming teminology, should not contain variables, procedure should be the sequencial step by step proceduce that should represent as if it is written by a 6 year old boy who is a par of the anogy working on realtime who acts as a the 1st preson or second person in the problem statement analogy and shoud not include any programming keys or terminology, it should in a way that if handded over to a 6 year old by and as him to do the task independentely. he can get the task done physically and give it as JSON eg: [ {"val":"Step1","child":[]}, {"val":"Step2","child":[{"val":"Step2Child1","child":[]},{"val":"Step2Child2","child":[]}]} ] 3.Programming Procedure should contain programming teminology, should contain variables and should replecate he above procedure steps in programming terms and give it as JSON eg: [ {"val":"Step1","child":[]}, {"val":"Step2","child":[{"val":"Step2Child1","child":[]},{"val":"Step2Child2","child":[]}]} ] 4.Sample Input/Output can be in the format of JSON where the root element is array and each item in the array represent the sample input output, each sample input output item should contain key "i" where the list of input for that particular sample input is given as a array of strings and each sample input output item should contain key "o" where the list of output for that particular sample input is given as a array of strings following the same structure in the continueing example [{"i":["let a=10","let b=20"], "o":["Here is result","Total is 30","Thank you"]},{"i":["let a=30","let b=40"], "o":["Here is result","Total is 70","Thank you"]},{"i":["let a=10","let b"], "o":["b is not defined"]}] Prepare minimum of 3 sample input/output sets 5.Flow Diagram should be a sequence of steps with hirarichy and with the key references to the flow with the control statements and give it as JSON eg: [ {"val":"Step1","child":[]}, {"val":"Step2","child":[{"val":"Step2Child1","child":[]},{"val":"Step2Child2","child":[]}]} ] 6.Code Snippet should be the multiple broken sets of code blocks that is extracted and converted from the flow diagram and programming procedure list where each block represent the flow control and Snippet should start from declaration on sample input parts and the last block should be sample output 7.Program should contain the JS program to get the output with comment added at the highest level which is picked from the procedure above 8.From the problem statement extract the tags of the concepts and prepare it as list of strings example: ["JS","array","object","arithmetic operation","for","nested for"] 9.severity : Take the scale of concept and logical reasoning provided above and also for the tags extracted and given above and give it as JSON eg:{"concept":5, "logical_reasoning":3,"forloop":7,"JSON":3} 10.sub_variants : Take the variantas and types used in the program on the provided topic exclusive to the topic provided eg:["for","nested for"] '


def ask_question(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message.strip()

def chatbot_json(request):
    if request.method == 'GET':
        # prompt = request.GET.get('prompt')

        response = ask_question(promt1)
        data = {'response': response}
    else:
        data = {'error': 'Invalid request method'}
    return JsonResponse(data)

            # import openai

# openai.api_key = "YOUR_API_KEY"

# def ask_question(prompt):
#     completions = openai.Completion.create(
#         engine="text-davinci-002",
#         prompt=prompt,
#         max_tokens=1024,
#         n=1,
#         stop=None,
#         temperature=0.5,
#     )

#     message = completions.choices[0].text
#     return message.strip()

# prompt = "What is the capital of France?"
# response = ask_question(prompt)
# print(response)