from .models import Cart


def cart_count(request):
    """Добавляет количество товаров в корзине в контекст"""
    cart = None
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            pass
    else:
        session_key = request.session.session_key
        if session_key:
            try:
                cart = Cart.objects.get(session_key=session_key)
            except Cart.DoesNotExist:
                pass
    
    if cart:
        return {'cart_count': cart.get_total_items(), 'cart_total': cart.get_total_price()}
    return {'cart_count': 0, 'cart_total': 0}
