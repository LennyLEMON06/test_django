from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'get_total_price')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_total_items', 'get_total_price', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    inlines = [CartItemInline]
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        return False
