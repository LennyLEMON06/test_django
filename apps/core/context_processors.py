from .models import ContactInfo, Slider


def contacts(request):
    """Добавляет контактную информацию в контекст всех шаблонов"""
    contact = ContactInfo.objects.first()
    return {'contact': contact}


def slider(request):
    """Добавляет активные слайды в контекст всех шаблонов"""
    slides = Slider.objects.filter(is_active=True).order_by('order')
    return {'slides': slides}
