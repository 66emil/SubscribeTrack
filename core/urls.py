from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),
    
    # URL для категорий
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
    
    # URL для компаний
    path('companies/', views.CompanyListView.as_view(), name='company-list'),
    path('companies/<int:pk>/', views.CompanyDetailView.as_view(), name='company-detail'),
    path('companies/create/', views.CompanyCreateView.as_view(), name='company-create'),
    path('companies/<int:pk>/update/', views.CompanyUpdateView.as_view(), name='company-update'),
    path('companies/<int:pk>/delete/', views.CompanyDeleteView.as_view(), name='company-delete'),
    
    # URL для подписок
    path('subscriptions/', views.SubscriptionListView.as_view(), name='subscription-list'),
    path('subscriptions/<int:pk>/', views.SubscriptionDetailView.as_view(), name='subscription-detail'),
    path('subscriptions/create/', views.SubscriptionCreateView.as_view(), name='subscription-create'),
    path('subscriptions/<int:pk>/update/', views.SubscriptionUpdateView.as_view(), name='subscription-update'),
    path('subscriptions/<int:pk>/delete/', views.SubscriptionDeleteView.as_view(), name='subscription-delete'),
]

