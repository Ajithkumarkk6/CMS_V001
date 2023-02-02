from django.contrib.auth.models import User
from authentication.models import UserAuthentication
from rest_framework.authtoken.models import Token
from .models import *
from course.models import *
from authentication.model_helper import create_update_model

def get_students(company_id):
        return EmployeeCompanyInfo.objects.filter(authentication__is_student = True, company__id = company_id).order_by('user__first_name')
def get_students_details(company_id):
        emp=EmployeeCompanyInfo.objects.get(authentication__is_student=True,id= company_id)
        return emp
def get_faculty_details(company_id):
        emp=EmployeeCompanyInfo.objects.get(authentication__is_faculty=True,id= company_id)
        return emp



def get_faculties(company_id):
        return EmployeeCompanyInfo.objects.filter(authentication__is_faculty = True, company__id = company_id).order_by('user__first_name')

def get_referrer(company_id):
        return EmployeeCompanyInfo.objects.filter(company__id = company_id).order_by('user__first_name')

def get_approver(company_id):
        return EmployeeCompanyInfo.objects.filter(authentication__is_faculty = True, company__id = company_id).order_by('user__first_name')







def get_student_courses(employee_id):
        return StudentCourse.objects.filter(employee_company__id = employee_id)

def get_student_course_sections(student_course_id):
        # 
        studentCourse = StudentCourse.objects.get(id = student_course_id)
        courseSections = CourseSection.objects.filter(course__id = studentCourse.course.id).order_by('order_sequence')
        return courseSections
        # return StudentCourseSection.objects.filter(student_course_item__id = student_course_id)

def get_student_course_topic(course_section_id):
        # studentCourseSection = CourseSection.objects.get(id=course_section_id)
        topicsQ =  Topic.objects.filter(course_section__id = course_section_id).order_by('order_sequence')
        print("topicsQtopicsQ",topicsQ.count())
        return topicsQ
        # return StudentCourseTopic.objects.filter(student_course_section__id = student_course_section_id)

def get_student_course_tasks(course_topic_id):
        # studentCourseTopic = StudentCourseTopic.objects.get(id = course_topic_id)
        return Task.objects.filter(topic__id = course_topic_id).order_by('order_sequence')

def get_student_course_task(id):
        return StudentCourseTask.objects.get(id = id)

        # return StudentCourseTask.objects.filter(student_course_topic__id = student_course_topic_id)
