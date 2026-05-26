from django.urls import path
from . import views

app_name = 'goods'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('<slug:category_slug>/', views.catalog, name='catalog_by_category'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]
