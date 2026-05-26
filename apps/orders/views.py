from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Order, OrderItem
from apps.cart.views import get_or_create_cart


def create_order(request):
    """Оформление заказа"""
    cart = get_or_create_cart(request)
    
    if not cart.items.exists():
        messages.warning(request, 'Корзина пуста')
        return redirect('cart:cart')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        comment = request.POST.get('comment', '').strip()
        
        if not first_name or not phone:
            messages.error(request, 'Заполните обязательные поля (Имя и телефон)')
            return redirect('cart:cart')
        
        # Создаём заказ
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            comment=comment,
            total_price=cart.get_total_price(),
        )
        
        # Переносим товары из корзины в заказ
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                quantity=item.quantity,
                price=item.product.price,
            )
        
        # Очищаем корзину
        cart.clear()
        
        messages.success(request, f'Заказ №{order.id} успешно оформлен!')
        return redirect('orders:order_success', order_id=order.id)
    
    items = cart.items.select_related('product').all()
    return render(request, 'orders/create_order.html', {'cart': cart, 'items': items})


def order_success(request, order_id):
    """Страница успешного оформления заказа"""
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def my_orders(request):
    """Мои заказы"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    """Детальная страница заказа"""
    order = get_object_or_404(Order, pk=pk)
    
    # Проверка: пользователь может видеть только свои заказы
    if order.user != request.user and not request.user.is_staff:
        raise PermissionDenied
    
    return render(request, 'orders/order_detail.html', {'order': order})
