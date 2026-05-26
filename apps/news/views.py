from django.shortcuts import render, get_object_or_404
from .models import News


def news_list(request):
    """Список новостей"""
    news = News.objects.filter(is_active=True)
    return render(request, 'news/news_list.html', {'news': news})


def news_detail(request, pk):
    """Детальная страница новости"""
    news_item = get_object_or_404(News, pk=pk, is_active=True)
    return render(request, 'news/news_detail.html', {'news_item': news_item})
