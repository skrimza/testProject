from django.urls import path
from .views import (
    NetworkNodeList, 
    NetworkNodeByCountry, 
    DebtAboveAverage,
    NetworkNodeByProduct, 
    NetworkNodeCreate, 
    NetworkNodeDelete,
    NetworkNodeUpdate, 
    ProductCreate, 
    ProductDelete, 
    ProductUpdate
)

urlpatterns = [
    path('nodes/', NetworkNodeList.as_view(), name='node-list'),
    path('nodes/country/<str:country>/', NetworkNodeByCountry.as_view(), name='node-by-country'),
    path('nodes/debt-above-average/', DebtAboveAverage.as_view(), name='debt-above-average'),
    path('nodes/product/<int:product_id>/', NetworkNodeByProduct.as_view(), name='node-by-product'),
    path('nodes/create/', NetworkNodeCreate.as_view(), name='node-create'),
    path('nodes/delete/<int:pk>/', NetworkNodeDelete.as_view(), name='node-delete'),
    path('nodes/update/<int:pk>/', NetworkNodeUpdate.as_view(), name='node-update'),
    path('products/create/', ProductCreate.as_view(), name='product-create'),
    path('products/delete/<int:pk>/', ProductDelete.as_view(), name='product-delete'),
    path('products/update/<int:pk>/', ProductUpdate.as_view(), name='product-update'),
]