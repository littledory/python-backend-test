from django.db import models
from django.utils import timezone

#Категория

class Category(models.Model):
    name = models.CharField('Название', max_length=50)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name

#Подкатегория

class Subcategory(models.Model):
    name = models.CharField('Название', max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    
    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
    
    def __str__(self):
        return f"{self.name} ({self.category})"

#Статус

class StatusReference(models.Model):
    name = models.CharField('Название', max_length=50)
    
    class Meta:
        verbose_name = 'Справочник статусов'
        verbose_name_plural = 'Справочник статусов'
    
    def __str__(self):
        return self.name
    
#Тип

class TypeReference(models.Model):
    name = models.CharField('Название', max_length=50)
    
    class Meta:
        verbose_name = 'Справочник типов'
        verbose_name_plural = 'Справочник типов'
    
    def __str__(self):
        return self.name

#Вся транзакция

class Transaction(models.Model):
    created_date = models.DateField('Дата создания', default=timezone.now)
    status = models.CharField('Статус', max_length=20, blank=True, null=True)
    transaction_type = models.CharField('Тип', max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, verbose_name='Подкатегория')
    amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2)
    comment = models.TextField('Комментарий', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-created_date']
    
    def __str__(self):
        return f"{self.created_date.strftime('%d.%m.%Y')} - {self.amount} руб."