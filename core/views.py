from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Category, Company, Subscription
from datetime import date


# ==================== Главная страница ====================
def home(request):
    """Главная страница приложения"""
    context = {
        'categories_count': Category.objects.count(),
        'companies_count': Company.objects.count(),
        'subscriptions_count': Subscription.objects.filter(status='active').count() if request.user.is_authenticated else 0,
    }
    return render(request, 'core/home.html', context)


# ==================== CRUD для Категорий ====================
class CategoryListView(ListView):
    """Список всех категорий"""
    model = Category
    template_name = 'core/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10


class CategoryDetailView(DetailView):
    """Детальная информация о категории"""
    model = Category
    template_name = 'core/category_detail.html'
    context_object_name = 'category'


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """Создание новой категории"""
    model = Category
    template_name = 'core/category_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('category-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Категория успешно создана!')
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление категории"""
    model = Category
    template_name = 'core/category_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('category-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Категория успешно обновлена!')
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление категории"""
    model = Category
    template_name = 'core/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Категория успешно удалена!')
        return super().delete(request, *args, **kwargs)


# ==================== CRUD для Компаний ====================
class CompanyListView(ListView):
    """Список всех компаний"""
    model = Company
    template_name = 'core/company_list.html'
    context_object_name = 'companies'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Company.objects.select_related('category')
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CompanyDetailView(DetailView):
    """Детальная информация о компании"""
    model = Company
    template_name = 'core/company_detail.html'
    context_object_name = 'company'


class CompanyCreateView(LoginRequiredMixin, CreateView):
    """Создание новой компании"""
    model = Company
    template_name = 'core/company_form.html'
    fields = ['name', 'category', 'description', 'website', 'logo_url', 'subscription_plans']
    success_url = reverse_lazy('company-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Компания успешно создана!')
        return super().form_valid(form)


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление компании"""
    model = Company
    template_name = 'core/company_form.html'
    fields = ['name', 'category', 'description', 'website', 'logo_url', 'subscription_plans']
    success_url = reverse_lazy('company-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Компания успешно обновлена!')
        return super().form_valid(form)


class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление компании"""
    model = Company
    template_name = 'core/company_confirm_delete.html'
    success_url = reverse_lazy('company-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Компания успешно удалена!')
        return super().delete(request, *args, **kwargs)


# ==================== CRUD для Подписок ====================
class SubscriptionListView(LoginRequiredMixin, ListView):
    """Список подписок пользователя"""
    model = Subscription
    template_name = 'core/subscription_list.html'
    context_object_name = 'subscriptions'
    paginate_by = 10
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user).select_related('company', 'company__category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subscriptions = self.get_queryset()
        
        # Статистика
        context['total_subscriptions'] = subscriptions.count()
        context['active_subscriptions'] = subscriptions.filter(status='active').count()
        context['total_monthly_cost'] = sum(
            sub.price for sub in subscriptions.filter(status='active', billing_period='monthly')
        )
        
        return context


class SubscriptionDetailView(LoginRequiredMixin, DetailView):
    """Детальная информация о подписке"""
    model = Subscription
    template_name = 'core/subscription_detail.html'
    context_object_name = 'subscription'
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)


class SubscriptionCreateView(LoginRequiredMixin, CreateView):
    """Создание новой подписки"""
    model = Subscription
    template_name = 'core/subscription_form.html'
    fields = ['company', 'plan_name', 'price', 'billing_period', 'status', 'start_date', 'next_billing_date', 'end_date', 'notes']
    success_url = reverse_lazy('subscription-list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Подписка успешно создана!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Company.objects.all()
        return context


class SubscriptionUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление подписки"""
    model = Subscription
    template_name = 'core/subscription_form.html'
    fields = ['company', 'plan_name', 'price', 'billing_period', 'status', 'start_date', 'next_billing_date', 'end_date', 'notes']
    success_url = reverse_lazy('subscription-list')
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Подписка успешно обновлена!')
        return super().form_valid(form)


class SubscriptionDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление подписки"""
    model = Subscription
    template_name = 'core/subscription_confirm_delete.html'
    success_url = reverse_lazy('subscription-list')
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Подписка успешно удалена!')
        return super().delete(request, *args, **kwargs)
