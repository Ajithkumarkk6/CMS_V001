from django.urls import path

from . import views

urlpatterns = [
    # path('', views.Index.as_view(), name='index'),
    path('getCourses', views.GetCourses.as_view(), name='getCourses'),
    path('getCourseSections', views.GetCourseSections.as_view(), name='getCourseSections'),
    path('getCourseTopics', views.GetCourseTopics.as_view(), name='getCourseTopics'),
    path('getCourseTopicDetails', views.GetCourseTopicDetails.as_view(), name='getCourseTopicDetails'),
    path('getCourseTopicTasks', views.GetCourseTopicTasks.as_view(), name='getCourseTopicTasks'),
    path('getTaskDetails', views.GetTaskDetails.as_view(), name='getTaskDetails'),
    path('genericCRUD', views.GenericCRUD.as_view(), name='GenericCRUD'),
    path('genericBatchCRUD', views.GenericBatchCRUD.as_view(), name='genericBatchCRUD'),
    path('genericAttachmentCRUD', views.GenericAttachmentCRUD.as_view(), name='genericAttachmentCRUD'),
    path('genericList', views.GenericDynamicListApi.as_view(), name='GenericCRUD'),

]