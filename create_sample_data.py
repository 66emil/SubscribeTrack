#!/usr/bin/env python
"""
Скрипт для создания тестовых данных в приложении Менеджер Подписок
Запуск: python create_sample_data.py
"""

import os
import django
from datetime import date, timedelta
from decimal import Decimal

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'subscribe_track.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Category, Company, Subscription


def create_sample_data():
    print("🚀 Создание тестовых данных...")
    
    # Создание пользователя (если не существует)
    user, created = User.objects.get_or_create(
        username='demo',
        defaults={
            'email': 'demo@example.com',
            'is_active': True
        }
    )
    if created:
        user.set_password('demo123')
        user.save()
        print(f"✅ Создан пользователь: {user.username} (пароль: demo123)")
    else:
        print(f"ℹ️  Пользователь {user.username} уже существует")
    
    # Создание категорий
    categories_data = [
        {
            'name': 'Стриминг видео',
            'description': 'Онлайн-платформы для просмотра фильмов и сериалов'
        },
        {
            'name': 'Облачные хранилища',
            'description': 'Сервисы для хранения файлов в облаке'
        },
        {
            'name': 'Музыка',
            'description': 'Сервисы потоковой музыки'
        },
        {
            'name': 'Онлайн-обучение',
            'description': 'Образовательные платформы'
        },
        {
            'name': 'Продуктивность',
            'description': 'Инструменты для повышения продуктивности'
        }
    ]
    
    print("\n📁 Создание категорий...")
    categories = {}
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        categories[cat_data['name']] = category
        if created:
            print(f"  ✅ Создана категория: {category.name}")
        else:
            print(f"  ℹ️  Категория {category.name} уже существует")
    
    # Создание компаний
    companies_data = [
        {
            'name': 'Netflix',
            'category': 'Стриминг видео',
            'description': 'Крупнейший сервис потокового видео с огромной библиотекой фильмов и сериалов',
            'website': 'https://www.netflix.com',
            'subscription_plans': {
                'Базовая': '990',
                'Стандартная': '1490',
                'Премиум': '2490'
            }
        },
        {
            'name': 'Яндекс Плюс',
            'category': 'Стриминг видео',
            'description': 'Российский сервис с фильмами, музыкой и доставкой',
            'website': 'https://plus.yandex.ru',
            'subscription_plans': {
                'Мульти': '399',
                'Семейная': '599'
            }
        },
        {
            'name': 'Google One',
            'category': 'Облачные хранилища',
            'description': 'Облачное хранилище от Google',
            'website': 'https://one.google.com',
            'subscription_plans': {
                '100 GB': '139',
                '200 GB': '219',
                '2 TB': '799'
            }
        },
        {
            'name': 'Яндекс Диск',
            'category': 'Облачные хранилища',
            'description': 'Российское облачное хранилище',
            'website': 'https://disk.yandex.ru',
            'subscription_plans': {
                '100 GB': '129',
                '1 TB': '899',
                '3 TB': '2490'
            }
        },
        {
            'name': 'Spotify',
            'category': 'Музыка',
            'description': 'Крупнейший музыкальный стриминговый сервис',
            'website': 'https://www.spotify.com',
            'subscription_plans': {
                'Индивидуальная': '269',
                'Duo': '349',
                'Семейная': '429'
            }
        },
        {
            'name': 'Яндекс Музыка',
            'category': 'Музыка',
            'description': 'Российский музыкальный сервис',
            'website': 'https://music.yandex.ru',
            'subscription_plans': {
                'Подписка': '299',
                'Семейная': '399'
            }
        },
        {
            'name': 'Coursera',
            'category': 'Онлайн-обучение',
            'description': 'Онлайн-курсы от ведущих университетов',
            'website': 'https://www.coursera.org',
            'subscription_plans': {
                'Coursera Plus': '4999'
            }
        },
        {
            'name': 'Skillbox',
            'category': 'Онлайн-обучение',
            'description': 'Российская платформа онлайн-образования',
            'website': 'https://skillbox.ru',
            'subscription_plans': {
                'Премиум': '1990',
                'Безлимит': '3990'
            }
        },
        {
            'name': 'Notion',
            'category': 'Продуктивность',
            'description': 'Система управления проектами и заметками',
            'website': 'https://www.notion.so',
            'subscription_plans': {
                'Plus': '800',
                'Business': '1500'
            }
        }
    ]
    
    print("\n🏢 Создание компаний...")
    companies = {}
    for comp_data in companies_data:
        category = categories[comp_data['category']]
        company, created = Company.objects.get_or_create(
            name=comp_data['name'],
            defaults={
                'category': category,
                'description': comp_data['description'],
                'website': comp_data['website'],
                'subscription_plans': comp_data['subscription_plans']
            }
        )
        companies[comp_data['name']] = company
        if created:
            print(f"  ✅ Создана компания: {company.name}")
        else:
            print(f"  ℹ️  Компания {company.name} уже существует")
    
    # Создание подписок для demo пользователя
    subscriptions_data = [
        {
            'company': 'Netflix',
            'plan_name': 'Стандартная',
            'price': '1490',
            'billing_period': 'monthly',
            'status': 'active',
            'start_date': date(2024, 1, 15),
            'next_billing_date': date(2025, 11, 15),
            'notes': 'Семейная подписка, делим на 3 человека'
        },
        {
            'company': 'Spotify',
            'plan_name': 'Индивидуальная',
            'price': '269',
            'billing_period': 'monthly',
            'status': 'active',
            'start_date': date(2024, 3, 1),
            'next_billing_date': date(2025, 11, 1),
            'notes': 'Музыка для работы и тренировок'
        },
        {
            'company': 'Google One',
            'plan_name': '200 GB',
            'price': '219',
            'billing_period': 'monthly',
            'status': 'active',
            'start_date': date(2024, 2, 10),
            'next_billing_date': date(2025, 11, 10),
            'notes': 'Резервное копирование фото'
        },
        {
            'company': 'Notion',
            'plan_name': 'Plus',
            'price': '800',
            'billing_period': 'monthly',
            'status': 'active',
            'start_date': date(2024, 6, 1),
            'next_billing_date': date(2025, 11, 1),
            'notes': 'Для управления проектами'
        },
        {
            'company': 'Яндекс Плюс',
            'plan_name': 'Мульти',
            'price': '399',
            'billing_period': 'monthly',
            'status': 'paused',
            'start_date': date(2024, 4, 15),
            'next_billing_date': date(2025, 12, 15),
            'notes': 'Приостановлено на время отпуска'
        }
    ]
    
    print("\n💳 Создание подписок...")
    for sub_data in subscriptions_data:
        company = companies[sub_data['company']]
        subscription, created = Subscription.objects.get_or_create(
            user=user,
            company=company,
            plan_name=sub_data['plan_name'],
            defaults={
                'price': Decimal(sub_data['price']),
                'billing_period': sub_data['billing_period'],
                'status': sub_data['status'],
                'start_date': sub_data['start_date'],
                'next_billing_date': sub_data['next_billing_date'],
                'notes': sub_data['notes']
            }
        )
        if created:
            print(f"  ✅ Создана подписка: {company.name} - {sub_data['plan_name']}")
        else:
            print(f"  ℹ️  Подписка {company.name} уже существует")
    
    print("\n" + "="*60)
    print("✨ Тестовые данные успешно созданы!")
    print("="*60)
    print("\n📊 Статистика:")
    print(f"  • Категорий: {Category.objects.count()}")
    print(f"  • Компаний: {Company.objects.count()}")
    print(f"  • Подписок: {Subscription.objects.count()}")
    print(f"  • Пользователей: {User.objects.count()}")
    
    print("\n🔑 Данные для входа:")
    print(f"  Логин: demo")
    print(f"  Пароль: demo123")
    
    print("\n🌐 Запустите сервер:")
    print(f"  python manage.py runserver")
    print(f"\n  Затем откройте: http://127.0.0.1:8000/")
    print(f"  Админка: http://127.0.0.1:8000/admin/")


if __name__ == '__main__':
    try:
        create_sample_data()
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

