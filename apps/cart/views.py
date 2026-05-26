from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.goods.models import Product
from apps.cart.models import Cart, CartItem
from apps.orders.models import Order, OrderItem


def get_cart(request):
    """Получить корзину пользователя (из сессии или БД)"""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


def cart_view(request):
    """Страница корзины"""
    cart = get_cart(request)
    items = cart.items.select_related('product').all()
    
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'cart/cart.html', context)


def cart_add(request, pk):
    """Добавить товар в корзину"""
    product = get_object_or_404(Product, pk=pk)
    cart = get_cart(request)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart:cart')


def cart_remove(request, pk):
    """Удалить товар из корзины"""
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=pk)
    cart_item.delete()
    
    return redirect('cart:cart')


def cart_update(request, pk):
    """Обновить количество товара в корзине"""
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=pk)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
    
    return redirect('cart:cart')


@login_required
def create_order(request):
    """Оформление заказа"""
    cart = get_cart(request)
    items = cart.items.select_related('product').all()
    
    if not items:
        return redirect('cart:cart')
    
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', ''),
            phone=request.POST.get('phone', ''),
            address=request.POST.get('address', ''),
            comment=request.POST.get('comment', ''),
        )
        
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
        
        # Очистить корзину
        cart.items.all().delete()
        
        return redirect('orders:order_success', pk=order.pk)
    
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'orders/create_order.html', context)
