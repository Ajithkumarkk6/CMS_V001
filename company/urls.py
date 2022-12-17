from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('addBranch', views.AddBranch.as_view(), name='addBranch'),
    path('addBranchLocation', views.AddBranchLocation.as_view(), name='addBranchLocation'),
    path('updateBranchLocation', views.UpdateBranchLocation.as_view(), name='updateBranchLocation'),
    path('getDepartments', views.GetDepartments.as_view(), name='getDepartments'),
    path('addDepartment', views.AddDepartment.as_view(), name='addDepartment'),
    path('getAllBranches', views.GetAllBranches.as_view(), name='getAllBranches'),
    path('getBrandSectors', views.GetBrandSectors.as_view(), name='getBrandSectors'),
    path('getTypeOfBusiness', views.GetTypeOfBusiness.as_view(), name='getTypeOfBusiness'),
    path('getStoreDetails', views.GetStoreDetails.as_view(), name='getStoreDetails'),
    path('getCustomerHomeContent', views.GetCustomerHomeContent.as_view(), name='getCustomerHomeContent'),
    path('syncCheckInVehicles', views.SyncCheckInVehicles.as_view(), name='syncCheckInVehicles'),    
    path('syncCheckOutVehicles', views.SyncCheckOutVehicles.as_view(), name='syncCheckOutVehicles'),    
    path('getVehicleTypes', views.GetVehicleTypes.as_view(), name='getVehicleTypes'),    


]

