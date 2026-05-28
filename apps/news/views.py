from django.shortcuts import render, get_object_or_404
from .models import News


def news_list(request):
    """Список новостей"""
    query = request.GET.get('q', '')
    
    if query:
        news_items = News.objects.filter(
            title__icontains=query
        ).order_by('-created_at')
    else:
        news_items = News.objects.all().order_by('-created_at')
    
    context = {
        'news_list': news_items,
        'query': query,
    }
    return render(request, 'news_list.html', context)


def news_detail(request, slug):
    """Детальная страница новости"""
    news_item = get_object_or_404(News, slug=slug)
    
    context = {
        'news_item': news_item,
    }
    return render(request, 'news_detail.html', context)
