from django.shortcuts import render, get_object_or_404
from apps.news.models import News


def news_list(request):
    """Список новостей"""
    news = News.objects.all()
    
    context = {
        'news': news,
    }
    return render(request, 'news/news_list.html', context)


def news_detail(request, pk):
    """Детальная страница новости"""
    news_item = get_object_or_404(News, pk=pk)
    
    context = {
        'news_item': news_item,
    }
    return render(request, 'news/news_detail.html', context)
