from django.urls import path

from . import views

urlpatterns = [

    path('registerAdmin', views.RegisterAdmin.as_view(), name='RegisterAdmin'),
    path('registerCustomer', views.RegisterCustomer.as_view(), name='registerCustomer'),
    path('submitRegistationOtp', views.SubmitRegistationOtp.as_view(), name='submitRegistationOtp'),
    path('registerCompany', views.RegisterCompany.as_view(), name='registerCompany'),
    path('deleteCompany', views.DeleteCompany.as_view(), name='deleteCompany'),
    path('validateUser', views.ValidateUser.as_view(), name='validateUser'),
    path('validateUserBusiness', views.ValidateUserBusiness.as_view(), name='validateUserBusiness'),
    path('validateRegistrationUser', views.ValidateRegistrationUser.as_view(), name='validateRegistrationUser'),
    path('web/validateUser', views.ValidateUserWeb.as_view(), name='web/validateUser'),
    path('otpLogin', views.OtpLogin.as_view(), name='OtpLogin'),
    path('otpRegister', views.OtpRegister.as_view(), name='otpRegister'),

   
    path('sendRegistationOtp', views.ResendRegistationOtp.as_view(), name='sendRegistationOtp'),
    path('resendRegistationOtp', views.ResendRegistationOtp.as_view(), name='resendRegistationOtp'),

    path('getBusinessPlaces', views.GetBusinessPlaces.as_view(), name='getBusinessPlaces'),
    path('getBusinessPlaceDetails', views.GetBusinessPlaceDetails.as_view(), name='getBusinessPlaceDetails'),


    path('resendLoginOtp', views.ResendLoginOtp.as_view(), name='resendLoginOtp'),
    path('deleteUser', views.DeleteUser.as_view(), name='deleteUser'),
    path('web/deleteUser', views.DeleteUserPage.as_view(), name='web/deleteUser'),
    path('appConfig', views.MobileAppConfig.as_view(), name='v1/appConfig'),
    path('dashboard', views.Dashboard.as_view(), name='v1/dashboard'),    

    path('attachUserAccounts', views.AttachUserAccounts.as_view(), name='attachUserAccounts'),    
    path('getAttachedUserAccounts', views.GetAttachedUserAccounts.as_view(), name='getAttachedUserAccounts'),    


]
