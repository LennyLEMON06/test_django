from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from apps.cart.models import Cart, CartItem
from apps.cart.views import get_or_create_cart


def create_order(request):
    """Оформление заказа"""
    if request.method == 'POST':
        # Получаем корзину
        cart = get_or_create_cart(request)
        
        # Проверяем, есть ли товары в корзине
        if not cart.items.exists():
            messages.error(request, 'Ваша корзина пуста')
            return redirect('cart:cart_detail')
        
        # Получаем данные из формы
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        comment = request.POST.get('comment', '').strip()
        
        # Валидация обязательных полей
        if not phone or not address:
            messages.error(request, 'Пожалуйста, заполните телефон и адрес доставки')
            return redirect('cart:cart_detail')
        
        # Создаём заказ
        user = request.user if request.user.is_authenticated else None
        order = Order.objects.create(
            user=user,
            phone=phone,
            address=address,
            comment=comment,
            status='new'
        )
        
        # Переносим товары из корзины в заказ
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        
        # Очищаем корзину
        cart.items.all().delete()
        
        messages.success(request, f'Заказ #{order.id} успешно оформлен! Мы свяжемся с вами в ближайшее время.')
        return redirect('orders:order_detail', order_id=order.id)
    
    # GET запрос - показываем страницу оформления
    cart = get_or_create_cart(request)
    
    if not cart.items.exists():
        messages.info(request, 'Ваша корзина пуста')
        return redirect('goods:catalog')
    
    context = {
        'cart': cart,
        'items': cart.items.select_related('product').all(),
        'total_price': cart.get_total_price(),
    }
    return render(request, 'orders/create_order.html', context)


@login_required
def order_detail(request, order_id):
    """Детальная страница заказа"""
    order = get_object_or_404(Order, id=order_id)
    
    # Проверяем права доступа: пользователь может видеть только свои заказы
    if not request.user.is_staff and order.user != request.user:
        messages.error(request, 'У вас нет доступа к этому заказу')
        return redirect('users:profile')
    
    context = {
        'order': order,
        'items': order.items.select_related('product').all(),
    }
    return render(request, 'orders/order_detail.html', context)
