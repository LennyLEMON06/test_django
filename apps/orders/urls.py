from django.urls import path
from apps.orders import views

app_name = 'orders'

urlpatterns = [
    path('success/<int:pk>/', views.order_success, name='order_success'),
]
