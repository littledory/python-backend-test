from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('create/', views.transaction_create, name='transaction_create'),
    path('create/<int:pk>/', views.transaction_create, name='transaction_create'), 
    path('references/', views.update, name='update'), 
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'),
    
    path('api/transactions/', views.get_transactions_api, name='api_transactions'),
    path('api/categories/', views.get_categories, name='api_categories'),
    path('api/subcategories/', views.get_subcategories, name='api_subcategories'),
    path('api/statuses/', views.get_statuses, name='api_statuses'),
    path('api/transaction-types/', views.get_transaction_types, name='api_transaction_types'),
]