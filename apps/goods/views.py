from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category


def catalog_view(request):
    """Каталог товаров и услуг"""
    products = Product.objects.select_related('category').all()
    
    # Фильтры
    selected_categories = request.GET.getlist('category')
    show_popular = request.GET.get('popular') == '1'
    
    if selected_categories:
        products = products.filter(category__slug__in=selected_categories)
    
    if show_popular:
        products = products.filter(is_popular=True)
    
    # Пагинация
    paginator = Paginator(products, 9)  # 9 товаров на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'products': page_obj,
        'categories': categories,
        'selected_categories': selected_categories,
        'show_popular': show_popular,
        'page_obj': page_obj,
    }
    
    return render(request, 'catalog.html', context)


def product_detail_view(request, slug):
    """Детальная страница товара"""
    product = get_object_or_404(
        Product.objects.select_related('category'), 
        slug=slug
    )
    
    # Похожие товары (из той же категории, кроме текущего)
    similar_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    
    return render(request, 'product_detail.html', context)
