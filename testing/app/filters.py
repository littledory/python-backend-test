import django_filters
from .models import Transaction

class TransactionFilter(django_filters.FilterSet):
    created_date = django_filters.DateFromToRangeFilter(
        field_name='created_date',
        label='Диапазон дат'
    )
    status = django_filters.CharFilter(
        field_name='status',
        label='Статус'
    )
    transaction_type = django_filters.CharFilter(
        field_name='transaction_type',
        label='Тип'
    )
    category = django_filters.NumberFilter(
        field_name='category__id',
        label='Категория'
    )
    subcategory = django_filters.NumberFilter(
        field_name='subcategory__id',
        label='Подкатегория'
    )
    
    class Meta:
        model = Transaction
        fields = ['created_date', 'status', 'transaction_type', 'category', 'subcategory']