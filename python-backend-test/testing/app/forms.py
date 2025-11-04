from django import forms
from .models import Transaction, Subcategory, StatusReference, TypeReference

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['created_date', 'status', 'transaction_type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'created_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'category-select', 'required': 'required'}),
            'subcategory': forms.Select(attrs={'class': 'form-control', 'id': 'subcategory-select', 'required': 'required'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'required': 'required',
                'placeholder': '0.00'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите комментарий (необязательно)...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        status_choices = [('', '---------')]
        try:
            statuses = StatusReference.objects.all()
            status_choices += [(status.name, status.name) for status in statuses]
        except:
            pass
        self.fields['status'].choices = status_choices
        type_choices = [('', '---------')]
        try:
            types = TypeReference.objects.all()
            type_choices += [(type_ref.name, type_ref.name) for type_ref in types]
        except:
            pass
        self.fields['transaction_type'].choices = type_choices
        
        self.fields['transaction_type'].required = True
        self.fields['category'].required = True
        self.fields['subcategory'].required = True
        self.fields['amount'].required = True
        self.fields['status'].required = False
        self.fields['comment'].required = False
        
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.all()
        else:
            self.fields['subcategory'].queryset = Subcategory.objects.none()