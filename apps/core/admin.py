from django.contrib import admin
from .models import ContactInfo, Slider


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
