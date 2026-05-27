from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'product_type', 'price', 'is_popular', 'created_at')
    list_filter = ('category', 'product_type', 'is_popular')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_popular', 'price')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'product_type', 'description', 'price', 'image', 'is_popular')
        }),
        ('Характеристики памятника', {
            'fields': ('length_p', 'width_p', 'thickness_p', 'material'),
            'classes': ('collapse',)
        }),
        ('Характеристики плитки', {
            'fields': ('tile_length', 'tile_width', 'tile_thickness', 'coating_type', 'quantity_per_pack'),
            'classes': ('collapse',)
        }),
        ('Информация об услуге', {
            'fields': ('service_duration', 'service_notes'),
            'classes': ('collapse',)
        }),
    )
