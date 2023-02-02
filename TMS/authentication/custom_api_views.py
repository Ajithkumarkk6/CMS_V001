
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from authentication.model_helper import create_update_model_response, create_update_model, check_if_exist, ValidateRequest, get_paginated_results_set, get_user_company_from_request
from authentication.response_serializer import get_validation_failure_response, get_success_response
from abc import ABC, abstractmethod


class GenericAPIView(APIView):

    ACCESS_TYPE_OPEN = 1
    ACCESS_TYPE_EMPLOYEE = 2
    ACCESS_TYPE_ADMIN = 3
    access_rights = ACCESS_TYPE_ADMIN

    def __init__(self):
        print("qqqrrrrrrrrrrr", self.access_rights)

        if self.access_rights == self.ACCESS_TYPE_OPEN:
            self.authentication_classes = []
            self.permission_classes = []
        else:
            self.authentication_classes = [authentication.TokenAuthentication]
            self.permission_classes = [permissions.IsAuthenticated]

        self.request_serializer = None
        self.payload = []

    def get_employee_company_info(self):
        return self.validateRequest.employee_company_info()

    def post(self, request):

        data = request.data
        self.payload = data

        print("rrrrrrrrrrr", self.access_rights)
        self.validateRequest = ValidateRequest(
            request=request, request_serializer=self.request_serializer)

        if self.access_rights == self.ACCESS_TYPE_ADMIN and not self.validateRequest.is_admin():
            return Response(get_validation_failure_response(None, self.validateRequest.errors_formatted()))
        elif self.access_rights == self.ACCESS_TYPE_EMPLOYEE and not self.validateRequest.is_valid():
            return Response(get_validation_failure_response(None, self.validateRequest.errors_formatted()))

        return self.proceed_post(request)


class GenericCrudApiView(GenericAPIView):

    base_model = None

    def proceed_post(self, request):
        print("0000111")
        if self.base_model is not None:
            return create_update_model_response(self.base_model, data=self.payload, api_instance=self)
        return Response(get_validation_failure_response(None, self.validateRequest.errors_formatted()))


class GenericItemDetailApiView(GenericAPIView):

    item_serializer = None

    @abstractmethod
    def get_item_query(self):
        raise NotImplementedError("Item Query not Implemented")

    def proceed_post(self, request):
        print("0011", self.get_item_query())
        if self.get_item_query() is not None and self.item_serializer is not None:
            print("0021")

            item_query = self.get_item_query()
            serializer = self.item_serializer(item_query, many=False)
            print("0031")
            return Response(get_success_response(message=None, details=serializer.data))
        return Response(get_validation_failure_response([], "Invalid Request"))


class GenericListAPIView(GenericAPIView):

    list_serializer = None
    per_page_count = -1
    search_contains = []
    order_by = None

    @abstractmethod
    def get_list_query(self):
        raise NotImplementedError("List Query not Implemented")

    def proceed_post(self, request):
        if self.get_list_query() is not None and self.list_serializer is not None:
            list_query = self.get_list_query()
            if 'q' in self.payload and self.payload['q'] != '':
                for esearch_contains in self.search_contains:
                    each_s = {each_s+'__istartswith': self.payload['q']}
                    list_query = list_query.filter()
            if self.per_page_count == -1:
                serializer = self.list_serializer(
                    self.get_list_query(), many=True)
                return Response(get_success_response(message=None, details=serializer.data))
            else:
                page_number = 1
                if 'page_number' in self.payload:
                    page_number = self.payload['page_number']
                res = get_paginated_results_set(self.get_list_query(
                ), self.list_serializer, page_number, self.per_page_count)
                return Response(get_success_response(message=None, details=res))

        return Response(get_validation_failure_response([], "Invalid Request"))
