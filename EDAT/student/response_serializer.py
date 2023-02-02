from rest_framework import serializers
from .models import *
from employee.models import EmployeePersonalInfo
from course.response_serializer import *



class GetStudentCoursesSerializer(serializers.ModelSerializer):

    course = serializers.SerializerMethodField()
    # course_description = serializers.SerializerMethodField()

    class Meta:
        model = StudentCourse
        fields = ['id', 'course']

    def get_course(self, obj):
        return CourseItemSerializer(obj.course).data

class GetStudentDetailSerializer(serializers.ModelSerializer):
    first_name=serializers.SerializerMethodField()
    last_name=serializers.SerializerMethodField()
    email=serializers.SerializerMethodField()

   
    class Meta:
        model = EmployeePersonalInfo
        fields = ['id','first_name','last_name','email','gender','dob','mobile_number','aadhar','address','pincode']
    def get_first_name(self, obj):
        return obj.user.first_name
    def get_last_name(self, obj):
        return obj.user.last_name
    def get_email(self, obj):
        return obj.user.email



class GetStudentEducationalItemSerializer(serializers.ModelSerializer):

   
    class Meta:
        model = EducationalItem
        fields = ['id','graduation','institution','details','year_of_passing']



class GetFacultyDetailSerializer(serializers.ModelSerializer):
    first_name=serializers.SerializerMethodField()
    last_name=serializers.SerializerMethodField()
    email=serializers.SerializerMethodField()

   
    class Meta:
        model = EmployeePersonalInfo
        fields = ['id','first_name','last_name','email','gender','dob','mobile_number','aadhar','address','pincode']
    def get_first_name(self, obj):
        return obj.user.first_name
    def get_last_name(self, obj):
        return obj.user.last_name
    def get_email(self, obj):
        return obj.user.email

class GetFacultyEducationalItemSerializer(serializers.ModelSerializer):

   
    class Meta:
        model = EducationalItem
        fields = ['id','graduation','institution','details','year_of_passing']




class GetStudentsSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    # course_description = serializers.SerializerMethodField()
    student_course = serializers.SerializerMethodField()
   

    class Meta:
        model = EmployeeCompanyInfo
        fields = ['id', 'name', 'photo', 'student_course' , 'last_active_time','date_of_joining']

    def get_name(self, obj):
        try:
            return obj.user.first_name
        except:
            return  None

    def get_student_course(self, obj):
        studentCourses = StudentCourse.objects.filter(employee_company__id = obj.id)
        return GetStudentCoursesSerializer(studentCourses, many=True).data
    
class GetStudentsDetailedSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    student_course = serializers.SerializerMethodField()
    student_personal_info=serializers.SerializerMethodField()
    student_educational_items=serializers.SerializerMethodField()


    class Meta:
        model = EmployeeCompanyInfo
        fields = ['id', 'name', 'photo', 'last_active_time','date_of_joining','student_personal_info','student_educational_items','student_course']

    def get_name(self, obj):
        try:
            return obj.user.first_name
        except:
            return  None

    def get_student_course(self, obj):
        studentCourses = StudentCourse.objects.filter(employee_company__id = obj.id)
        return GetStudentCoursesSerializer(studentCourses, many=True).data
    def get_student_personal_info(self,obj):
        student_personal_info=EmployeePersonalInfo.objects.filter(user=obj.user)
        return GetStudentDetailSerializer(student_personal_info, many=True).data
    def get_student_educational_items(self,obj):
       
        student_educational_items=EducationalItem.objects.filter(employee_company__id=obj.id)
        return GetStudentEducationalItemSerializer(student_educational_items, many=True).data





class GetFacultiesSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    role_id=  serializers.SerializerMethodField()
    role_name=  serializers.SerializerMethodField()
    course_id= serializers.SerializerMethodField()
    course_name= serializers.SerializerMethodField()
    faculty_personal_info=serializers.SerializerMethodField()
    faculty_educational_items=serializers.SerializerMethodField()
    # course_description = serializers.SerializerMethodField()
    class Meta:
        model = EmployeeCompanyInfo
        fields = ['id', 'name', 'last_active_time', 'photo','role_id','role_name','course_id','course_name','faculty_personal_info','faculty_educational_items']

    def get_name(self, obj):
        return obj.user.first_name
    def get_role_id(self, obj):
        try:
            return obj.designation.id 
        except:
            return None
    def get_role_name(self, obj):
        try:
            return obj.designation.name
        except:
            return None
    def get_course_id(self, obj):
        try:
            return obj.department.id
        except:
            return None
    def get_course_name(self, obj):
        try:
            return obj.department.name
        except:
            return None
    def get_faculty_personal_info(self,obj):
        faculty_personal_info=EmployeePersonalInfo.objects.filter(user=obj.user)
        return GetFacultyDetailSerializer(faculty_personal_info, many=True).data
    def get_faculty_educational_items(self,obj):
        faculty_educational_items=EducationalItem.objects.filter(employee_company__id=obj.id)
        return GetFacultyEducationalItemSerializer(faculty_educational_items, many=True).data


 

        
        


class GetReferrerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    # course_description = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeCompanyInfo
        fields = ['id', 'name']

    def get_name(self, obj):
        return obj.user.first_name


class GetApproverSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    # course_description = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeCompanyInfo
        fields = ['id', 'name']

    def get_name(self, obj):
        return obj.user.first_name




class StudentCourseSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentCourseSection
        fields = ['id', 'is_inprogress', 'start_date', 'end_date', 'progress_code', 'base_status']

# class StudentCourseTopicSerializer01(serializers.ModelSerializer):

#     class Meta:
#         model = StudentCourseTopic
#         fields = ['id', 'is_inprogress', 'start_date', 'end_date', 'progress_code', 'base_status']

class GetStudentCourseSectionsSerializer(serializers.ModelSerializer):

    student_course_section = serializers.SerializerMethodField()
    # course_section_description = serializers.SerializerMethodField()

    class Meta:
        model = CourseSection
        fields = ['id', 'name', "description", 'student_course_section', 'order_sequence']

    def get_student_course_section(self, obj):
        studentCourseSections  = StudentCourseSection.objects.filter(student_course_item__id = self.context.get("student_course_id"), course_section__id=obj.id)
        if studentCourseSections.count() > 0:
            studentCourseSection = studentCourseSections.first()
            return StudentCourseSectionSerializer(studentCourseSection).data
        return None


class StudentCourseTopicSerializer(serializers.ModelSerializer):

    approver =  serializers.SerializerMethodField()

    class Meta:
        model = StudentCourseTopic
        fields = ['id', 'start_date', 'end_date', 'progress_code', 'base_status', 'approver']

    def get_approver(self, obj):
        if obj.approver is not None:
            return obj.approver.user.first_name
        return 'N/A'

class GetStudentCourseTopicsSerializer(serializers.ModelSerializer):

    student_course_topic = serializers.SerializerMethodField()
    # course_topic_description = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['id', 'name', "description", 'is_parent', 'parent', 'order_sequence', 'student_course_topic']

    def get_student_course_topic(self, obj):
        print("serializer_extra_data=====", self.context.get('student_id'))

        try:
            studentCourseTopic  = StudentCourseTopic.objects.get(employee_company = self.context.get("student_id"), course_topic__id=obj.id)
            return StudentCourseTopicSerializer(studentCourseTopic).data
        except:
            pass

        # if studentCourseTopics.count() > 0:
        #     studentCourseTopic = studentCourseTopics.first()
        #     return StudentCourseSectionSerializer(studentCourseTopic).data
        return None 



class StudentCourseTaskSerializer(serializers.ModelSerializer):

    approver =  serializers.SerializerMethodField()

    class Meta:
        model = StudentCourseTask
        fields = ['id', 'start_date', 'end_date', 'progress_code', 'base_status', 'approver']

    def get_approver(self, obj):
        if obj.approver is not None:
            return obj.approver.user.first_name
        return 'N/A'


class GetStudentCourseTasksSerializer(serializers.ModelSerializer):

    student_course_task = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'is_manditory', 'order_sequence', 'student_course_task']

    def get_student_course_task(self, obj):
        try:
            studentCourseTasks  = StudentCourseTask.objects.get(employee_company = self.context.get("student_id"), course_task__id=obj.id)
            return StudentCourseTaskSerializer(studentCourseTasks).data
        except:
            pass

        # if studentCourseTopics.count() > 0:
        #     studentCourseTopic = studentCourseTopics.first()
        #     return StudentCourseTaskSerializer(studentCourseTopic).data
        return None 

class GetStudentCourseTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentCourseTask
        fields = ['id', 'formulated_question', 'procedure', 'flow_diagram', 'program', 'approver']
