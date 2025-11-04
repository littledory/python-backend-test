from django.contrib import admin
from .models import Category, Subcategory, Transaction, StatusReference, TypeReference

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']

@admin.register(StatusReference)
class StatusReferenceAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(TypeReference)
class TypeReferenceAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['created_date', 'status', 'transaction_type', 'category', 'subcategory', 'amount']
    list_filter = ['status', 'transaction_type', 'category', 'created_date']
    search_fields = ['comment', 'status', 'transaction_type']
    date_hierarchy = 'created_date'