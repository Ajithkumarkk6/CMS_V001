from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('getSectorServiceTypes', views.GetSectorServiceTypes.as_view(), name='getSectorServiceTypes'),

    path('addBrandCategory', views.AddBrandCategory.as_view(), name='addBrandCategory'),
    path('addBrandService', views.AddBrandService.as_view(), name='addBrandService'),

    path('updateBrandBranchService', views.UpdateBrandBranchService.as_view(), name='updateBrandBranchService'),
    path('updateBrandService', views.UpdateBrandService.as_view(), name='updateBrandService'),

    
    path('getPredefinedCategories', views.GetPredefinedCategories.as_view(), name='getPredefinedCategories'),
    path('getMasterUomPredefinedFormFields', views.GetMasterUomPredefinedFormFields.as_view(), name='getMasterUomPredefinedFormFields'),
    path('getPredefinedServices', views.GetPredefinedServices.as_view(), name='getPredefinedServices'),
    path('submitBrandMasterUom', views.SubmitBrandMasterUom.as_view(), name='submitBrandMasterUom'),
    path('submitBrandServices', views.SubmitBrandServices.as_view(), name='submitBrandServices'),
    path('submitBrandBranchCalendarWeek', views.SubmitBrandBranchCalendarWeek.as_view(), name='submitBrandBranchCalendarWeek'),
    path('getBrandCategories', views.GetBrandCategories.as_view(), name='getBrandCategories'),

    path('getBrandBranchCategories', views.GetBrandBranchCategories.as_view(), name='getBrandBranchCategories'),
    path('getBrandBranchServices', views.GetBrandBranchServices.as_view(), name='getBrandBranchServices'),


]
