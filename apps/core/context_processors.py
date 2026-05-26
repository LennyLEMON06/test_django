from apps.core.models import ContactInfo


def contact_info(request):
    """Контекстный процессор для передачи контактной информации во все шаблоны"""
    contact = ContactInfo.objects.first()
    return {
        'contact_info': contact,
    }
