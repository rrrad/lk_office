"""Определяем схемы url для lk"""
"""Определяем схемы url для lk"""
from django.urls import path
from . import views

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
    #act pdf
    path('act/', views.act, name='act'),
]