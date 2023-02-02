from rest_framework import serializers
from .models import *


class CourseSectionListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CourseSection
        fields = ['id', 'name', 'description', 'thumbnail']


class CourseItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'thumbnail']



class CourseListSerializer(serializers.ModelSerializer):
    
    
    ide = serializers.SerializerMethodField()
    sections = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'sections','ide']



    def get_sections(self, obj):
        courseSections = CourseSection.objects.filter(course__id = obj.id).order_by('order_sequence')
        courseSectionListSerializer = CourseSectionListSerializer(courseSections, many=True)
        return courseSectionListSerializer.data
    def get_ide(self, obj):
        try:
            return {'id':obj.ide.id,'course_ide_type':obj.ide.course_ide_types}
        except:
            return None


class CourseTopicListSerializer(serializers.ModelSerializer):

    parent_id = serializers.SerializerMethodField()
    
    class Meta:
        model = Topic
        fields = ['id', 'name', 'description', 'is_parent', 'parent_id', 'order_sequence','thumbnail']

    def get_parent_id(self, obj):
        if obj.parent != None:
            return obj.parent.id
        return None

class GetCourseTopicDetailsSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = Topic
        fields = ['id','name']


class GetCourseTopicTasksSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = Task
        fields = ['id', 'name', 'is_manditory']



class GetTaskDetailsSerializer(serializers.ModelSerializer):
    ide = serializers.SerializerMethodField()


    
    class Meta:
        model = Task
        fields = ['id', 'name', 'problem_statement', 'rules', 'sample_io', 'is_manditory','ide']

    def get_ide(self, obj):
        return {'id':obj.ide.id,'course_ide_type':obj.ide.course_ide_types}
