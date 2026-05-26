from django.urls import path
from apps.users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('orders/', views.user_orders, name='user_orders'),
]
