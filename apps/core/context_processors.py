from django.conf import settings
from .models import ContactInfo
from apps.cart.models import Cart


def get_contact_info():
    """Получить активную контактную информацию"""
    return ContactInfo.objects.filter(is_active=True).first()


def get_cart_count(request):
    """Получить количество товаров в корзине"""
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            return cart.get_total_items()
    else:
        session_key = request.session.session_key
        if session_key:
            cart = Cart.objects.filter(session_key=session_key).first()
            if cart:
                return cart.get_total_items()
    return 0


def contact_info(request):
    """Контекстный процессор для контактной информации и корзины"""
    return {
        'contact_info': get_contact_info(),
        'cart_count': get_cart_count(request),
        'settings': settings,
    }
