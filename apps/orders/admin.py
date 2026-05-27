from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'get_subtotal')

    def get_subtotal(self, obj):
        return obj.get_subtotal()
    get_subtotal.short_description = 'Сумма'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'status', 'get_total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('phone', 'user__username', 'user__email')
    inlines = [OrderItemInline]
    readonly_fields = ('get_total_price', 'created_at', 'updated_at')
    list_editable = ('status',)

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Сумма (₽)'
