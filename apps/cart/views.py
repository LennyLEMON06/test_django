from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from apps.goods.models import Product
from .models import Cart, CartItem


def get_or_create_cart(request):
    """Получить или создать корзину для пользователя/сессии"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Если была корзина в сессии, перенести товары
        session_key = request.session.session_key
        if session_key:
            try:
                session_cart = Cart.objects.get(session_key=session_key)
                for item in session_cart.items.all():
                    cart_item, _ = CartItem.objects.get_or_create(
                        cart=cart,
                        product=item.product,
                        defaults={'quantity': item.quantity}
                    )
                    if not _:
                        cart_item.quantity += item.quantity
                        cart_item.save()
                    item.delete()
                session_cart.delete()
            except Cart.DoesNotExist:
                pass
        return cart
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
        return cart


def cart_view(request):
    """Страница корзины"""
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()
    return render(request, 'cart/cart.html', {'cart': cart, 'items': items})


def cart_add(request, product_id):
    """Добавить товар в корзину"""
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = get_or_create_cart(request)
    
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'{product.name} добавлен в корзину')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'cart_count': cart.get_total_items()})
    
    return redirect(request.META.get('HTTP_REFERER', 'cart:cart'))


def cart_remove(request, product_id):
    """Удалить товар из корзины"""
    cart = get_or_create_cart(request)
    try:
        item = cart.items.get(product_id=product_id)
        item.delete()
        messages.success(request, 'Товар удалён из корзины')
    except CartItem.DoesNotExist:
        pass
    
    return redirect('cart:cart')


def cart_update(request, product_id):
    """Обновить количество товара"""
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    
    try:
        item = cart.items.get(product_id=product_id)
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()
    except CartItem.DoesNotExist:
        pass
    
    return redirect('cart:cart')


def cart_clear(request):
    """Очистить корзину"""
    cart = get_or_create_cart(request)
    cart.clear()
    messages.success(request, 'Корзина очищена')
    return redirect('cart:cart')
