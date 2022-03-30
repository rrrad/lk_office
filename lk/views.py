from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Order
from .forms import OrderForm, EditOrderForm
from django.http import Http404
from django.db.models import Q
import datetime
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.conf import settings
import os


def index(request):
    return render(request, 'lk/index.html')


@login_required
def orders(request):
    """вывод списка заявок"""
    editable = False
    if request.user.username == 'cleaning':
        orders = Order.objects.filter(department=1).filter(~Q(status='выполнено')).order_by('-date_added')
        editable = True
    elif request.user.username == 'internet':
        orders = Order.objects.filter(department=2).filter(~Q(status='выполнено')).order_by('-date_added')
        editable = True
    elif request.user.username == 'santechnic':
        orders = Order.objects.filter(department=3).filter(~Q(status='выполнено')).order_by('-date_added')
        editable = True
    elif request.user.username == 'electric':
        orders = Order.objects.filter(department=4).filter(~Q(status='выполнено')).order_by('-date_added')
        editable = True
    elif request.user.username == 'remont':
        orders = Order.objects.filter(department=5).filter(~Q(status='выполнено')).order_by('-date_added')
        editable = True
    elif request.user.username == 'documents':
        orders = Order.objects.filter(department=6).filter(~Q(status='выполнено')).order_by('-date_added')
        editable = True
    else:
        orders = Order.objects.filter(owner=request.user).order_by('-date_added')

    p = Paginator(orders, 20)
    page = request.GET.get('page')
    orders_page = p.get_page(page)
    context = {'orders': orders_page, 'editable': editable}
    return render(request, 'lk/orders.html', context)


@login_required
def new_order(request):
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = OrderForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = OrderForm(data=request.POST)
        if form.is_valid():
            new_o = form.save(commit=False)
            new_o.owner = request.user
            new_o.save()
            send_message_to_service(form.cleaned_data.get("department"))
            return redirect('lk:orders')

    # Вывести пустую или недействительную форму
    context = {'form': form}
    return render(request, 'lk/new_order.html', context)


def send_message_to_service(service):
    email = "rrad73@yandex.ru"
    if service == 1:
        email = settings.EMAIL_HOST_CLEANING
    if service == 2:
        email = settings.EMAIL_HOST_INTERNET
    if service == 3:
        email = settings.EMAIL_HOST_SANTECHNIC
    if service == 4:
        email = settings.EMAIL_HOST_ELECTRIC
    if service == 5:
        email = settings.EMAIL_HOST_REMONT
    if service == 6:
        email = settings.EMAIL_HOST_DOCUMENTS
    send_mail('ЛК Офисный центр',
              'новое сообщение',
              'lk@yaroffice.ru',
              [email],
              fail_silently=False, )


@login_required
def edit_order(request, order_id):
    """ответ на заявку"""
    if request.user.username == 'remont':
        order = Order.objects.get(id=order_id)
        if request.method != 'POST':
            # Данные не отправлялись; создается пустая форма.
            form = EditOrderForm(instance=order)
        else:
            # Отправлены данные POST; обработать данные.
            form = EditOrderForm(instance=order, data=request.POST)
            if form.is_valid():
                new_o = form.save(commit=False)
                if new_o.status == 'выполнено':
                    new_o.date_relise = datetime.datetime.now()
                new_o.save()
                return redirect('lk:orders')

        # Вывести пустую или недействительную форму
        context = {'order': order, 'form': form}
    else:
        raise Http404
    return render(request, 'lk/edit_order.html', context)


def act(request):
    context = {'pass': settings.EMAIL_PORT, 'email': settings.EMAIL_PORT,
               'seret': settings.EMAIL_PORT}
    return render(request, 'lk/info.html', context)