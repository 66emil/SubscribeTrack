from django.contrib import admin
from .models import Category, Company, Subscription


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ-панель для категорий"""
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('name',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Админ-панель для компаний"""
    list_display = ('name', 'category', 'website', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('category', 'created_at')
    ordering = ('name',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'category', 'description')
        }),
        ('Дополнительные данные', {
            'fields': ('website', 'logo_url')
        }),
        ('Планы подписок', {
            'fields': ('subscription_plans',),
            'description': 'Укажите планы подписок в формате JSON: {"Базовая": "990", "Продвинутая": "1990"}'
        }),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Админ-панель для подписок"""
    list_display = ('user', 'company', 'plan_name', 'price', 'billing_period', 'status', 'next_billing_date')
    search_fields = ('user__username', 'company__name', 'plan_name')
    list_filter = ('status', 'billing_period', 'company__category', 'created_at')
    ordering = ('-start_date',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'company', 'plan_name', 'price')
        }),
        ('Детали подписки', {
            'fields': ('billing_period', 'status')
        }),
        ('Даты', {
            'fields': ('start_date', 'next_billing_date', 'end_date')
        }),
        ('Дополнительно', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Делаем created_at и updated_at только для чтения"""
        if obj:  # При редактировании
            return ('created_at', 'updated_at')
        return ()
    
    date_hierarchy = 'start_date'
