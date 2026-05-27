from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Cart, CartItem
from goods.models import Product


def get_or_create_cart(request):
    """Получить или создать корзину для текущего пользователя/сессии"""
    if request.user.is_authenticated:
        # Авторизованный пользователь - корзина привязана к пользователю
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Если была корзина из сессии, переносим товары
        if 'cart_id' in request.session and not created:
            session_cart_id = request.session['cart_id']
            try:
                session_cart = Cart.objects.get(id=session_cart_id)
                # Переносим товары из сессионной корзины
                for item in session_cart.items.all():
                    cart_item, item_created = CartItem.objects.get_or_create(
                        cart=cart,
                        product=item.product,
                        defaults={'quantity': item.quantity}
                    )
                    if not item_created:
                        cart_item.quantity += item.quantity
                        cart_item.save()
                    item.delete()
                session_cart.delete()
            except Cart.DoesNotExist:
                pass
            del request.session['cart_id']
        return cart
    else:
        # Анонимный пользователь - корзина в сессии
        cart_id = request.session.get('cart_id')
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id)
                return cart
            except Cart.DoesNotExist:
                pass
        # Создаём новую сессионную корзину
        cart = Cart.objects.create(session_key=request.session.session_key or str(request.session))
        request.session['cart_id'] = cart.id
        return cart


def cart_detail(request):
    """Страница корзины"""
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()
    
    context = {
        'cart': cart,
        'items': items,
        'total_price': cart.get_total_price(),
        'total_items': cart.get_total_items(),
    }
    return render(request, 'cart/cart.html', context)


def cart_add(request, product_id):
    """Добавить товар в корзину"""
    product = get_object_or_404(Product, id=product_id)
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
    
    messages.success(request, f'Товар "{product.name}" добавлен в корзину')
    
    # Если запрос AJAX, возвращаем JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'total_items': cart.get_total_items(),
            'message': f'Товар "{product.name}" добавлен в корзину'
        })
    
    # Иначе редирект
    next_url = request.GET.get('next', 'cart:cart_detail')
    return redirect(next_url)


def cart_remove(request, item_id):
    """Удалить товар из корзины"""
    item = get_object_or_404(CartItem, id=item_id)
    cart = get_or_create_cart(request)
    
    # Проверяем, что товар принадлежит корзине текущего пользователя
    if item.cart != cart:
        messages.error(request, 'Ошибка доступа к корзине')
        return redirect('cart:cart_detail')
    
    product_name = item.product.name
    item.delete()
    messages.success(request, f'Товар "{product_name}" удалён из корзины')
    
    return redirect('cart:cart_detail')


def cart_update(request, item_id):
    """Обновить количество товара в корзине"""
    item = get_object_or_404(CartItem, id=item_id)
    cart = get_or_create_cart(request)
    
    # Проверяем, что товар принадлежит корзине текущего пользователя
    if item.cart != cart:
        messages.error(request, 'Ошибка доступа к корзине')
        return redirect('cart:cart_detail')
    
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        item.quantity = quantity
        item.save()
        messages.success(request, 'Количество товаров обновлено')
    else:
        item.delete()
        messages.success(request, 'Товар удалён из корзины')
    
    return redirect('cart:cart_detail')


def cart_clear(request):
    """Очистить корзину"""
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    messages.success(request, 'Корзина очищена')
    return redirect('cart:cart_detail')
