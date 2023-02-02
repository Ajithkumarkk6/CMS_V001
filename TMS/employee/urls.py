from django.urls import path

from . import views

urlpatterns = [
    path('addEmployee', views.AddEmployeeV1.as_view(), name='addEmployee'),
    path('updateEmployeeStatus', views.UpdateEmployeeStatus.as_view(), name='addEmployee'),
    path('getEmployeeDetails', views.GetEmployeeDetails.as_view(), name='getEmployeeDetails'),
    path('getEmployeeCheckinAssociations', views.GetEmployeeCheckinAssociations.as_view(), name='getEmployeeCheckinAssociations'),
    path('getDesignations', views.GetDesignations.as_view(), name='getDesignations'),
    path('getEmployees', views.GetEmployeesV1.as_view(), name='getEmployees'),
    # path('updateEmployeeProfilePhoto', views.UpdateEmployeeProfilePhoto.as_view(), name='updateEmployeeProfilePhoto'),
    path('addDesignation', views.AddDesignation.as_view(), name='addDesignation'),
    path('updateEmployeeCheckinAssociations', views.UpdateEmployeeCheckinAssociations.as_view(), name='updateEmployeeCheckinAssociations'),
    path('web/v1/getEmployees', views.GetEmployeesV1Web.as_view(), name='web/v1/getEmployees'),
]

