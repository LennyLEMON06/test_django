from django.shortcuts import render
from apps.goods.models import Product
from apps.news.models import News


def index(request):
    """Главная страница"""
    popular_products = Product.objects.filter(is_popular=True, is_active=True)[:6]
    latest_news = News.objects.filter(is_active=True)[:3]
    return render(request, 'core/index.html', {
        'popular_products': popular_products,
        'latest_news': latest_news,
    })


def contacts(request):
    """Страница контактов"""
    return render(request, 'core/contacts.html')
