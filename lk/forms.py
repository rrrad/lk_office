from django import forms
from  .models import Order, Invoice, Act


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['text_order', 'department',]
        labels = {
            'text_order': 'Текст заявки',
            'department': 'Департамент',
        }

class EditOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['department', 'date_plane', 'status', ]
        widgets = {
            'date_plane': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),

        }
        labels = {
            'department': 'Департамент',
            'date_plane': 'Планируемая дата выполнения',
            'status': 'статус',
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date_document', 'number_invoice',
                  'number_document', 'client', 'inn', 'kpp',
                  'adres', 'telephon', 'service', 'cost', 'cost_str', 'month', 'year',]
        widgets = {
            'date_document': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),

        }
        labels = {
            'date_document': 'Дата документа',
            'number_invoice': 'Номер счета',
            'number_document': 'Номер договора',
            'client': 'Заказчик',
            'inn': 'ИНН',
            'kpp': 'КПП',
            'adres': 'Адрес',
            'telephon': 'Телефон',
            'service': 'Услуга',
            'cost': 'Цена',
            'cost_str': 'Цена текстом',
            'month': 'Месяц',
            'year': 'Год'
        }

class ActForm(forms.ModelForm):
    class Meta:
        model = Act
        fields = ['date_document', 'number_invoice',
                  'number_document', 'client', 'bank', 'inn', 'kpp',
                  'adres', 'telephon', 'service', 'cost', 'cost_str', 'month', 'year']
        widgets = {
            'date_document': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),

        }
        labels = {
            'date_document': 'Дата документа',
            'number_invoice': 'Номер акта',
            'number_document': 'Номер договора',
            'client': 'Заказчик',
            'bank': 'Банк',
            'inn': 'ИНН',
            'kpp': 'КПП',
            'adres': 'Адрес',
            'telephon': 'Телефон',
            'service': 'Услуга',
            'cost': 'Цена',
            'cost_str': 'Цена текстом',
            'month': 'Месяц',
            'year': 'Год'
        }

