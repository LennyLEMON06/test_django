from django.shortcuts import render, redirect
from django.contrib import messages
from apps.goods.models import Product
from apps.news.models import News
from apps.core.models import Slider, ContactInfo, ContactMessage


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
    
    # Обработка формы обратной связи
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message_text = request.POST.get('message', '').strip()
        
        # Простая валидация
        if name and email and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message_text
            )
            messages.success(request, 'Ваше сообщение успешно отправлено. Мы свяжемся с вами в ближайшее время.')
            return redirect('core:contacts')
        else:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля.')
    
    context = {
        'contact_info': contact_info,
    }
    return render(request, 'contacts.html', context)
