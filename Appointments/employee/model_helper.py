from django.contrib.auth.models import User
from authentication.models import UserAuthentication
from rest_framework.authtoken.models import Token
from employee.models import EmployeeDesignation, EmployeeCompanyInfo, EmployeeDocumentLocker
from company.models import CompanyBranchInfo

def get_designations(company):
    try:
        print(company)
        designations =  EmployeeDesignation.objects.filter(company__id=company)
        return designations
    except:
        return None

def get_employees(company):
    try:
        print(company)
        employees =  EmployeeCompanyInfo.objects.filter(company__id=company)
        return employees
    except:
        return None


def get_employees_each_branch(company_branch):
    try:
        print("company_branch================================================>>>>>>>>>>>>>>")
        print(company_branch)
        employees =  EmployeeCompanyInfo.objects.filter(company_branch__id=company_branch)
        return employees
    except:
        return None

def get_employee_document_tags(user):
    try:
        print("company_branch================================================>>>>>>>>>>>>>>")
        employee_documents =  EmployeeDocumentLocker.objects.filter(user=user)
        return employee_documents
    except:
        return None
