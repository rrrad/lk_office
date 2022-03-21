from django import forms
from  .models import Order


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
