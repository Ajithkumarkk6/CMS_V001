from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Course)
admin.site.register(CourseSection)
admin.site.register(Topic)
admin.site.register(Task)
admin.site.register(TopicTaskType)
admin.site.register(CourseIde)



