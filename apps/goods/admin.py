from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'product_type', 'is_popular', 'is_active')
    list_filter = ('category', 'product_type', 'is_popular', 'is_active', 'material')
    search_fields = ('name', 'description')
    list_editable = ('is_popular', 'is_active')
    
    fieldsets = (
        ('Основное', {
            'fields': ('category', 'name', 'description', 'price', 'image', 'product_type', 'is_popular', 'is_active')
        }),
        ('Характеристики памятника', {
            'fields': ('monument_length', 'monument_width', 'monument_thickness', 'material'),
            'classes': ('collapse',)
        }),
        ('Характеристики плитки', {
            'fields': ('tile_length', 'tile_width', 'coating_type', 'tiles_per_pack'),
            'classes': ('collapse',)
        }),
    )
