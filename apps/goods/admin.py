from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'product_type', 'is_popular', 'created_at')
    list_filter = ('category', 'product_type', 'is_popular')
    search_fields = ('name', 'description')
    prepopulated_fields = {}  # Можно добавить slug если будет
    list_editable = ('is_popular',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'name', 'description', 'price', 'image', 'product_type', 'is_popular')
        }),
        ('Характеристики памятника', {
            'fields': ('monument_length', 'monument_width', 'monument_thickness', 'monument_material'),
            'classes': ('collapse',)
        }),
        ('Характеристики плитки', {
            'fields': ('tile_length', 'tile_width', 'tile_coating', 'tile_package_quantity'),
            'classes': ('collapse',)
        }),
    )
