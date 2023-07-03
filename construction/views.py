from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Size
from authentication.model_helper import *

class AddProduct(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        request_info = get_user_company_from_request(request)

        if request_info['company_info'] is not None :
                    product = Product.objects.create(
                        name=data['name'],
                        description=data['description'],
                        # Add any other fields specific to your product model
                    )
         
        return Response(get_validation_failure_response(None, "Invalid user"))

class AddSize(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        request_info = get_user_company_from_request(request)

        if request_info['company_info'] is not None and request_info['is_admin']:
            product_id = data.get('product_id')
            product = Product.objects.filter(id=product_id).first()
            if product:
                size = Size.objects.create(
                    product=product,
                    name=data['name'],
                    quantity=data['quantity'],
                    length=data['length'],
                    breadth=data['breadth'],
                    # Add any other fields specific to your size model
                )
                return Response(get_success_response("Size added successfully"))
            else:
                return Response(get_validation_failure_response(None, "Invalid product"))
        else:
            return Response(get_validation_failure_response(None, "Invalid request or insufficient permissions"))
