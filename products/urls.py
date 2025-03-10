from django.urls import path
from .views import ProductAPI, index

urlpatterns = [
    path('api/search/', ProductAPI.as_view(), name='product-search'),
    path('', index, name='index'),
]
