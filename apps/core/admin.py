from django.contrib import admin
from .models import ContactInfo, Slider, ContactMessage


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'address', 'work_hours', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('phone', 'email')


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    list_editable = ('is_processed',)
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Информация о сообщении', {
            'fields': ('name', 'email', 'message', 'created_at')
        }),
        ('Статус обработки', {
            'fields': ('is_processed',)
        }),
    )
