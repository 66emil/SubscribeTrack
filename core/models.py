from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """Модель категории для группировки компаний"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name


class Company(models.Model):
    """Модель компании, предоставляющей подписки"""
    name = models.CharField(max_length=200, unique=True, verbose_name="Название компании")
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='companies',
        verbose_name="Категория"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    website = models.URLField(blank=True, null=True, verbose_name="Веб-сайт")
    logo_url = models.URLField(blank=True, null=True, verbose_name="URL логотипа")
    
    # Структура подписок как JSONField (ключ-значение: тип подписки - цена)
    subscription_plans = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Планы подписок",
        help_text='Формат: {"Базовая": "990", "Продвинутая": "1990", "Премиум": "2990"}'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_plan_names(self):
        """Возвращает список названий доступных планов"""
        return list(self.subscription_plans.keys()) if self.subscription_plans else []


class Subscription(models.Model):
    """Модель активной подписки пользователя"""
    BILLING_PERIOD_CHOICES = [
        ('monthly', 'Ежемесячно'),
        ('quarterly', 'Ежеквартально'),
        ('yearly', 'Ежегодно'),
    ]

    STATUS_CHOICES = [
        ('active', 'Активна'),
        ('cancelled', 'Отменена'),
        ('expired', 'Истекла'),
        ('paused', 'Приостановлена'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name="Пользователь"
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name="Компания"
    )
    
    # Название плана и цена (берутся из Company.subscription_plans)
    plan_name = models.CharField(max_length=100, verbose_name="Название плана")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Цена"
    )
    
    billing_period = models.CharField(
        max_length=20,
        choices=BILLING_PERIOD_CHOICES,
        default='monthly',
        verbose_name="Период оплаты"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name="Статус"
    )
    
    start_date = models.DateField(verbose_name="Дата начала")
    next_billing_date = models.DateField(verbose_name="Следующая дата оплаты")
    end_date = models.DateField(blank=True, null=True, verbose_name="Дата окончания")
    
    notes = models.TextField(blank=True, null=True, verbose_name="Заметки")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.user.username} - {self.company.name} ({self.plan_name})"

    def is_active(self):
        """Проверяет, активна ли подписка"""
        return self.status == 'active' and (
            self.end_date is None or self.end_date >= date.today()
        )
