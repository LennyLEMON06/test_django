from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'get_total')
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'status', 'created_at', 'get_total_price')
    list_filter = ('status', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone', 'id')
    inlines = [OrderItemInline]
    readonly_fields = ('user', 'first_name', 'last_name', 'phone', 'address', 'comment', 'created_at')
    
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('user', 'first_name', 'last_name', 'phone', 'address', 'comment')
        }),
        ('Статус заказа', {
            'fields': ('status', 'created_at')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'get_total')
    list_filter = ('order',)
