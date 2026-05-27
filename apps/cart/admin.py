from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'get_subtotal')

    def get_subtotal(self, obj):
        return obj.get_subtotal()
    get_subtotal.short_description = 'Сумма'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'get_total_items', 'get_total_price', 'created_at')
    list_filter = ('created_at',)
    inlines = [CartItemInline]
    readonly_fields = ('get_total_items', 'get_total_price')

    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Товаров'

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Сумма (₽)'
