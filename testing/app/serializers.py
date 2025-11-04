from rest_framework import serializers
from .models import Transaction, Category, Subcategory, StatusReference, TypeReference

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class SubcategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category', 'category_name']

class StatusReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusReference
        fields = ['id', 'name']

class TypeReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeReference
        fields = ['id', 'name']

class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    created_date = serializers.DateField(format='%d.%m.%Y')
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'created_date', 'status', 'transaction_type', 
            'category', 'category_name', 'subcategory', 'subcategory_name',
            'amount', 'comment'
        ]