from email.policy import default
from django.db import models
from authentication import constants
from authentication.models import BaseModelMixin
from authentication.constants import DEFAULT_RADIUS
from django.contrib.auth.models import User  # new
# from .models import EmployeeCompanyInfo
from django.utils.timezone import now

class CourseIde(BaseModelMixin):
    JAVA_SCRIPT = 'JS'
    HTML = 'HTML'
    REACT_NATIVE = 'RN'
    REACT_JS = 'RJS'

    COURSE_IDE_TYPE_CHOICES = [
        (JAVA_SCRIPT, 'Java script'),
        (HTML, 'Html'),
        (REACT_NATIVE, 'React Native'),
        (REACT_JS, 'React JS')
    ]

    course_ide_types=models.CharField(
        max_length=5,
        choices=COURSE_IDE_TYPE_CHOICES,
        default=JAVA_SCRIPT,
    )

    def __str__(self):
     return  self.course_ide_types+ "==="+str(self.id)



class Course(BaseModelMixin):
    
    course_id = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=220, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to='coursemeta', null=True, blank=True)
    ide =models.ForeignKey(CourseIde,on_delete=models.CASCADE, null=True, blank=True)
    

    def __str__(self):
        return self.name + "==="+str(self.id)



class CourseSection(BaseModelMixin):

    name = models.CharField(max_length=220, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to='coursemeta', null=True, blank=True)
    order_sequence = models.IntegerField(
        default=1, null=True, blank=True)
    course = models.ForeignKey(
        Course, related_name='course_section_course', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.name + "==="+str(self.id)

class Topic(BaseModelMixin):

    name = models.CharField(max_length=220, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to='coursemeta', null=True, blank=True)
    order_sequence = models.IntegerField(
        default=1, null=True, blank=True)
    course = models.ForeignKey(
        Course, related_name='topic_course', on_delete=models.CASCADE, null=True, blank=True)
    course_section = models.ForeignKey(
        CourseSection, related_name='topic_course_section', on_delete=models.CASCADE, null=True, blank=True)
    is_parent = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name + "==="+str(self.id)


class TopicTaskType(BaseModelMixin):

    name = models.CharField(max_length=220, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to='coursemeta', null=True, blank=True)
    order_sequence = models.IntegerField(
        default=1, null=True, blank=True)

    def __str__(self):
        return self.name + "==="+str(self.id)


class Task(BaseModelMixin):

    TYPE_BASIC = 'TBS'
    TYPE_RE = 'RTE'

    TASK_TYPE_CHOICES = [
        (TYPE_BASIC, 'Basic Tasks'),
        (TYPE_RE, 'Real Time Tasks'),
    ]
    task_type = models.CharField(
        max_length=5,
        choices=TASK_TYPE_CHOICES,
        default=TYPE_BASIC,
    )
    name = models.CharField(max_length=220, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tag = models.CharField(max_length=220, null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to='coursemeta', null=True, blank=True)
    problem_statement = models.TextField(null=True, blank=True)
    rules = models.JSONField(default={}, null=True, blank=True)
    sample_io = models.JSONField(default=[], null=True, blank=True)
    is_manditory = models.BooleanField(default=False)
    topic = models.ForeignKey(
        Topic, on_delete=models.SET_NULL, null=True, blank=True)
    task_type = models.ForeignKey(
        TopicTaskType, on_delete=models.SET_NULL, null=True, blank=True)
    order_sequence = models.IntegerField(
        default=1, null=True, blank=True)
    ide =models.ForeignKey(CourseIde,on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return  "==="+str(self.id)

