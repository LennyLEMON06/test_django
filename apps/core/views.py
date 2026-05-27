from django.shortcuts import render
from apps.goods.models import Product
from apps.news.models import News
from apps.core.models import Slider, ContactInfo


def index(request):
    """Главная страница"""
    # Получаем слайды для главной
    sliders = Slider.objects.filter(is_active=True).order_by('order')
    
    # Популярные товары
    popular_products = Product.objects.filter(is_popular=True)[:6]
    
    # Последние новости
    latest_news = News.objects.all().order_by('-created_at')[:3]
    
    context = {
        'sliders': sliders,
        'popular_products': popular_products,
        'latest_news': latest_news,
    }
    return render(request, 'index.html', context)


def contacts(request):
    """Страница контактов"""
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    context = {
        'contact_info': contact_info,
    }
    return render(request, 'contacts.html', context)
