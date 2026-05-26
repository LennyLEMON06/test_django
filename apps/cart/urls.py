from django.urls import path
from apps.cart import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/<int:pk>/', views.cart_add, name='add'),
    path('remove/<int:pk>/', views.cart_remove, name='remove'),
    path('update/<int:pk>/', views.cart_update, name='update'),
]
