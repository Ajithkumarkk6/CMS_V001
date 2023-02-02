from django.contrib import admin
from .models import * 
# Student,Course,Courses

# Register your models here.
admin.site.register(StudentCourse)
admin.site.register(StudentCourseSection)
admin.site.register(StudentCourseTask)
admin.site.register(StudentCourseTopic)
admin.site.register(EducationalItem)