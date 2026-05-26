from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order


@login_required
def order_success(request, pk):
    """Страница успешного оформления заказа"""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order_success.html', context)


@login_required
def user_orders(request):
    """Личный кабинет - история заказов"""
    orders = Order.objects.filter(user=request.user)
    
    context = {
        'orders': orders,
    }
    return render(request, 'users/user_orders.html', context)
