#!/usr/bin/env python
"""
Скрипт для создания пользователей с правильными паролями.
Запускать после загрузки фикстур.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password


def create_users():
    # Создаем суперпользователя admin
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@pamyat.ru',
            password='admin123',
            first_name='',
            last_name=''
        )
        print("✓ Создан суперпользователь: admin / admin123")
    else:
        admin = User.objects.get(username='admin')
        admin.set_password('admin123')
        admin.save()
        print("✓ Обновлен пароль суперпользователя: admin / admin123")

    # Создаем менеджера
    managers_group, _ = Group.objects.get_or_create(name='Managers')
    
    if not User.objects.filter(username='manager').exists():
        manager = User.objects.create_user(
            username='manager',
            email='manager@pamyat.ru',
            password='manager123',
            first_name='Менеджер',
            last_name='Магазина',
            is_staff=True
        )
        manager.groups.add(managers_group)
        print("✓ Создан менеджер: manager / manager123")
    else:
        manager = User.objects.get(username='manager')
        manager.set_password('manager123')
        manager.is_staff = True
        manager.save()
        manager.groups.add(managers_group)
        print("✓ Обновлен пароль менеджера: manager / manager123")

    # Создаем клиента
    if not User.objects.filter(username='customer').exists():
        User.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='customer123',
            first_name='Покупатель',
            last_name='Тестовый'
        )
        print("✓ Создан клиент: customer / customer123")
    else:
        customer = User.objects.get(username='customer')
        customer.set_password('customer123')
        customer.save()
        print("✓ Обновлен пароль клиента: customer / customer123")

    print("\n=== Все пользователи созданы/обновлены ===")


if __name__ == '__main__':
    create_users()
