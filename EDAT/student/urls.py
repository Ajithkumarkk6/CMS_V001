from django.urls import path

from . import views

urlpatterns = [
    # path('', views.Index.as_view(), name='index'),
    # path('addStudent', views.AddStudent.as_view(), name='addStudent'),

    path('getStudents', views.GetStudents.as_view(), name='getStudents'),
    path('getFaculties', views.GetFaculties.as_view(), name='getFaculties'),
    path('getStudentCourses', views.GetStudentCourses.as_view(), name='getStudentCourses'),
    path('getStudentCourseSections', views.GetStudentCourseSections.as_view(), name='getStudentCourseSections'),
    path('getStudentCourseTopics', views.GetStudentCourseTopics.as_view(), name='getStudentCourseTopics'),
    path('getStudentCourseTasks', views.GetStudentCourseTasks.as_view(), name='getStudentCourseTasks'),
    path('getStudentCourseTaskDetails', views.GetStudentCourseTaskDetails.as_view(), name='getStudentCourseTaskDetails'),
    path('getRefferer', views.GetRefferer.as_view(), name='getRefferer'),
    path('getApprover', views.GetApprover.as_view(), name='getApprover'),
    path('getStudentDetails', views.GetStudentDetails.as_view(), name='getStudentDetails'),
    path('getFacultyDetails', views.GetFacultyDetails.as_view(), name='getFacultyDetails'),
    path('addStudentCourseTask', views.AddStudentCourseTask.as_view(), name='addStudentCourseTask'),



    path('chatbot/', views.chatbot_json, name='chatbot'),
]
