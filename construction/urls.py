from django.urls import path
from .views import AddProduct, AddSize

urlpatterns = [
    path('products/', AddProduct.as_view(), name='add-product'),
    path('sizes/', AddSize.as_view(), name='add-size'),
]
