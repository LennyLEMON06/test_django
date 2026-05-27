from .models import ContactInfo


def get_contact_info():
    """Получить активную контактную информацию"""
    return ContactInfo.objects.filter(is_active=True).first()


def contact_info(request):
    """Контекстный процессор для контактной информации"""
    return {
        'contact_info': get_contact_info()
    }
