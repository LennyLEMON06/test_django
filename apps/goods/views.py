from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from apps.goods.models import Product, Category


def catalog(request, category_slug=None):
    """Каталог товаров и услуг"""
    categories = Category.objects.all()
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    else:
        category = None
        products = Product.objects.all()
    
    # Пагинация
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'categories': categories,
        'products': page_obj,
        'current_category': category,
    }
    return render(request, 'goods/catalog.html', context)


def product_detail(request, pk):
    """Детальная страница товара"""
    product = get_object_or_404(Product, pk=pk)
    
    context = {
        'product': product,
    }
    return render(request, 'goods/product_detail.html', context)
