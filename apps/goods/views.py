from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Product


def catalog(request, category_slug=None):
    """Каталог товаров"""
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    else:
        category = None
    
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'goods/catalog.html', {
        'categories': categories,
        'page_obj': page_obj,
        'category': category,
    })


def product_detail(request, pk):
    """Детальная страница товара"""
    product = get_object_or_404(Product, pk=pk, is_active=True)
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(pk=pk)[:4]
    
    return render(request, 'goods/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })
