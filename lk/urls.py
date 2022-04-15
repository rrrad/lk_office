"""Определяем схемы url для lk"""
"""Определяем схемы url для lk"""
from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

app_name = 'lk'
urlpatterns = [
    #домашняя страница
    path('', views.index, name='index'),
    #страница со списком заявок
    path('orders/', views.orders, name='orders'),
    #добавление новой заявки
    path('new_order/', views.new_order, name='new_order'),
    #страница заявки для редактирования внутренними службами
    path('edit_order/<int:order_id>/', views.edit_order, name='edit_order'),
    #
    # вызовы для арендаторов
    #
    #страница со списком счетов для арендатора
    path('acts/', views.acts, name='acts'),
    #страница со списком счетов для арендатора
    path('invoices/', views.invoices, name='invoices'),
    #акт pdf
    path('pdf_act/<int:act_id>', views.generate_act_pdf, name='pdf_act'),
    #счет pdf
    path('pdf_invoice/<int:invoice_id>', views.generate_invoice_pdf, name='pdf_invoice'),
    #
    #PDF



    #МЕТОДЫ ДЛЯ ПОЛЬЗОВАТЕЛЯ DOCUMENTS
    #список пользователей
    path('users/', views.users, name='users'),
    # страница со списком счетов пользователя
    path('user_invoices/<int:user_id>', views.user_invoices, name='user_invoices'),
    #создание дубля счета
    path('invoiced/<int:invoice_id>', views.invoiced, name='invoiced'),
    #редактирование счета
    path('invoicee/<int:invoice_id>', views.invoicee, name='invoicee'),
    #создание счета
    path('invoice/<int:user_id>', views.invoice, name='invoice'),
    #создание дубля акта
    path('actd/<int:act_id>', views.actd, name='actd'),
    #редактирование акта
    path('acte/<int:act_id>', views.acte, name='acte'),
    #создание пустого акта
    path('act_new/<int:user_id>', views.act_new, name='act_new'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)