from django.urls import path

from . import views

urlpatterns = [

    path('', views.Index.as_view(), name='index'),
    # path('getBrandBranchCategories', views.GetBrandBranchCategories.as_view(), name='getBrandBranchCategories'),

]
