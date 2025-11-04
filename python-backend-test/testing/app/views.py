from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Transaction, Category, Subcategory, StatusReference, TypeReference
from .serializers import TransactionSerializer, CategorySerializer, SubcategorySerializer, StatusReferenceSerializer, TypeReferenceSerializer
from .filters import TransactionFilter
from .forms import TransactionForm

#Фильтр

@api_view(['GET'])
def get_transactions_api(request):
    transactions = Transaction.objects.select_related('category', 'subcategory').all()
    filterset = TransactionFilter(request.GET, queryset=transactions)
    filtered_transactions = filterset.qs
    serializer = TransactionSerializer(filtered_transactions, many=True)
    return Response(serializer.data)

#Для подкатегорий

@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

#Для категорий

@api_view(['GET'])
def get_subcategories(request):
    category_id = request.GET.get('category_id')
    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id)
    else:
        subcategories = Subcategory.objects.all()
    serializer = SubcategorySerializer(subcategories, many=True)
    return Response(serializer.data)

#Для статуса

@api_view(['GET'])
def get_statuses(request):
    statuses = StatusReference.objects.all()
    serializer = StatusReferenceSerializer(statuses, many=True)
    return Response(serializer.data)

#Для типов

@api_view(['GET'])
def get_transaction_types(request):
    types = TypeReference.objects.all() 
    serializer = TypeReferenceSerializer(types, many=True) 
    return Response(serializer.data)

#Основные для страниц

def transaction_list(request):
    return render(request, 'transactions/transaction_list.html')

def transaction_create(request, pk=None):
    if pk:
        transaction = get_object_or_404(Transaction, pk=pk)
        is_edit = True
    else:
        transaction = None
        is_edit = False
    statuses = StatusReference.objects.all()
    types = TypeReference.objects.all()
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            if transaction:
                transaction.delete()
                messages.success(request, 'Транзакция успешно удалена!')
                return redirect('app:transaction_list')
        
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Транзакция успешно сохранена!')
            return redirect('app:transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    
    return render(request, 'transactions/create.html', {
        'form': form, 
        'transaction': transaction,
        'is_edit': is_edit,
        'statuses': statuses,
        'types': types,
    })
    
#Справочник

def update(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    statuses = StatusReference.objects.all()
    types = TypeReference.objects.all()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        #Категории
        
        if action == 'add_category':
            name = request.POST.get('category_name')
            if name:
                Category.objects.create(name=name)
        
        elif action == 'edit_category':
            category_id = request.POST.get('category_id')
            new_name = request.POST.get('category_name')
            if category_id and new_name:
                category = Category.objects.get(id=category_id)
                category.name = new_name
                category.save()
        
        elif action == 'delete_category':
            category_id = request.POST.get('category_id')
            if category_id:
                category = Category.objects.get(id=category_id)
                Subcategory.objects.filter(category=category).delete()
                category.delete()
        
        #Подкатегории
        
        elif action == 'add_subcategory':
            name = request.POST.get('subcategory_name')
            category_id = request.POST.get('category_id')
            if name and category_id:
                category = Category.objects.get(id=category_id)
                Subcategory.objects.create(name=name, category=category)
        
        elif action == 'edit_subcategory':
            subcategory_id = request.POST.get('subcategory_id')
            new_name = request.POST.get('subcategory_name')
            new_category_id = request.POST.get('category_id')
            if subcategory_id and new_name and new_category_id:
                subcategory = Subcategory.objects.get(id=subcategory_id)
                category = Category.objects.get(id=new_category_id)
                subcategory.name = new_name
                subcategory.category = category
                subcategory.save()
        
        elif action == 'delete_subcategory':
            subcategory_id = request.POST.get('subcategory_id')
            if subcategory_id:
                Subcategory.objects.get(id=subcategory_id).delete()
        
        #Статусы
        
        elif action == 'add_status':
            name = request.POST.get('status_name')
            if name:
                StatusReference.objects.create(name=name)
        
        elif action == 'edit_status':
            status_id = request.POST.get('status_id')
            new_name = request.POST.get('status_name')
            if status_id and new_name:
                status = StatusReference.objects.get(id=status_id)
                status.name = new_name
                status.save()
        
        elif action == 'delete_status':
            status_id = request.POST.get('status_id')
            if status_id:
                StatusReference.objects.get(id=status_id).delete()
        
        #Типы
        
        elif action == 'add_type':
            name = request.POST.get('type_name')
            if name:
                TypeReference.objects.create(name=name)
        
        elif action == 'edit_type':
            type_id = request.POST.get('type_id')
            new_name = request.POST.get('type_name')
            if type_id and new_name:
                transaction_type = TypeReference.objects.get(id=type_id)
                transaction_type.name = new_name
                transaction_type.save()
        
        elif action == 'delete_type':
            type_id = request.POST.get('type_id')
            if type_id:
                TypeReference.objects.get(id=type_id).delete()
        
        return redirect('app:update')
    
    return render(request, 'transactions/update.html', {
        'categories': categories,
        'subcategories': subcategories,
        'statuses': statuses,
        'types': types,
    })

def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id)
    return JsonResponse(list(subcategories.values('id', 'name')), safe=False)