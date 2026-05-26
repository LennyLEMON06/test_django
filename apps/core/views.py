from django.shortcuts import render
from apps.goods.models import Product
from apps.news.models import News
from apps.core.models import Slider


def index(request):
    """Главная страница"""
    slider = Slider.objects.filter(is_active=True)
    popular_products = Product.objects.filter(is_popular=True)[:6]
    latest_news = News.objects.all()[:3]
    
    context = {
        'slider': slider,
        'popular_products': popular_products,
        'latest_news': latest_news,
    }
    return render(request, 'core/index.html', context)


def contacts(request):
    """Страница контактов"""
    from apps.core.models import ContactInfo
    contacts = ContactInfo.objects.first()
    
    context = {
        'contacts': contacts,
    }
    return render(request, 'core/contacts.html', context)
