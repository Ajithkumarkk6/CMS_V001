from django.db import models
from authentication.models import BaseModelMixin,ProgressModelMixin
from django.contrib.auth.models import User
from course.models import Course,CourseSection,Task,Topic
from employee.models import EmployeeCompanyInfo

# Create your models here.



class EducationalItem(BaseModelMixin):
    EDUCATION_STATUS_CHOICES = [
        ("P2", 'p2'),
        ("UE", 'ue'),
        ("UG", 'ug'),
        ("PG", 'pg'),
        ("DP", 'dp'),
    ]
    graduation = models.CharField(max_length=5,choices=EDUCATION_STATUS_CHOICES,default="ue") 
    employee_company = models.ForeignKey(EmployeeCompanyInfo, on_delete=models.CASCADE)
    institution = models.CharField(max_length=220, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    year_of_passing = models.DateField(auto_now=False, null=True, blank=True)

    def __str__(self):
        return self.employee_company.user.first_name + "=====" + str(self.id)



class StudentCourse(ProgressModelMixin):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    employee_company = models.ForeignKey(EmployeeCompanyInfo, on_delete=models.CASCADE)
    student_course_id = models.CharField(max_length=30, null=True, blank=True)
    faculty = models.ForeignKey(EmployeeCompanyInfo, related_name='StudentCourse_faculty', on_delete=models.SET_NULL, null=True, blank=True)
    approver = models.ForeignKey(EmployeeCompanyInfo, related_name='StudentCourse_approver', on_delete=models.SET_NULL, null=True, blank=True)
    referrer = models.ForeignKey(EmployeeCompanyInfo, related_name='StudentCourse_referrer', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.employee_company.user.first_name +"======="+ str(self.id)

class StudentCourseSection(ProgressModelMixin):
    course_section = models.ForeignKey(CourseSection, on_delete=models.CASCADE)
    student_course_item = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    approver = models.ForeignKey(EmployeeCompanyInfo, on_delete=models.SET_NULL,null=True,blank=True)
    employee_company = models.ForeignKey(EmployeeCompanyInfo, related_name='student_course_student', on_delete=models.CASCADE, null=True, blank=True)

class StudentCourseTopic(ProgressModelMixin):
    course_topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    student_course_section = models.ForeignKey(StudentCourseSection, on_delete=models.CASCADE)
    approver = models.ForeignKey(EmployeeCompanyInfo, on_delete=models.SET_NULL,null=True,blank=True)
    employee_company = models.ForeignKey(EmployeeCompanyInfo, related_name='student_course_topic_student', on_delete=models.CASCADE, null=True, blank=True)
    student_course_item = models.ForeignKey(StudentCourse, on_delete=models.CASCADE,blank=True,null=True)
    
class StudentCourseTask(ProgressModelMixin):
    course_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student_course_topic = models.ForeignKey(StudentCourseTopic, on_delete=models.SET_NULL,null=True,blank=True)
    formulated_question = models.TextField(null=True, blank=True)
    procedure = models.JSONField(default=[], null=True, blank=True)                              
    flow_diagram = models.JSONField(default=[], null=True, blank=True)
    program = models.TextField(null=True, blank=True)
    approver = models.ForeignKey(EmployeeCompanyInfo, on_delete=models.SET_NULL,null=True,blank=True)
    employee_company = models.ForeignKey(EmployeeCompanyInfo, related_name='student_course_task_student', on_delete=models.CASCADE, null=True, blank=True)
    student_course_item = models.ForeignKey(StudentCourse, on_delete=models.CASCADE,null=True,blank=True)
    


# class StudentCourses(BaseModelMixin):
#     # many_to_many_fields =['course']
#     start_date = models.DateField(auto_now=False, null=True, blank=True)
#     course_name= models.ManyToManyField(StudentCourseItem)

#     def __str__(self):
#         return self.course_name

