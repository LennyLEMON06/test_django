from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'quantity', 'price', 'total_price')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'phone', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'total_price')
    inlines = [OrderItemInline]
    list_editable = ('status',)
    
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('user', 'first_name', 'last_name', 'phone', 'address', 'comment')
        }),
        ('Детали заказа', {
            'fields': ('status', 'total_price', 'created_at', 'updated_at')
        }),
    )
