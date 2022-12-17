from django.contrib.auth.models import User
from authentication.models import UserAuthentication
from rest_framework.authtoken.models import Token
from employee.models import EmployeeDesignation
from company.models import CompanyDepartment, CompanyBranchInfo, CompanySector, CompanyTypeOfBusiness

def get_departments(company):
    try:
        print(company)
        designations =  CompanyDepartment.objects.filter(company__id=company)
        return designations
    except:
        return None

def get_nature_of_business():
    try:
        nature_of_business =  CompanySector.objects.all()
        return nature_of_business
    except:
        return None

def get_type_of_business():
    try:
        type_of_business =  CompanyTypeOfBusiness.objects.all()
        return type_of_business
    except:
        return None


def get_all_branchs(company):
    # try:
    print(company)
    employees =  CompanyBranchInfo.objects.filter(company__id=company)
    # filter(company__id=company)
    return employees
    # except:
    #     return None

# def get_all_branchs(company_branch):
#     try:
#         print(company_branch)
#         employees =  CompanyBranchInfo.objects.filter(company__id=company_branch)
#         return employees
#     except:
#         return None

