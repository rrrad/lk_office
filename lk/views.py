from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Order, Invoice, Act
from .forms import OrderForm, EditOrderForm, InvoiceForm, ActForm
from django.http import Http404
from django.db.models import Q
import datetime
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
from .views_helper import *

from weasyprint import HTML

@login_required
def generate_act_pdf(request, act_id):
    """Создание pdf."""
    # Данные модели
    actt = Act.objects.get(id=act_id)
    if actt.owner.username == request.user.username :
        context = {'data': actt}

    # Обработка шаблона
        html_string = render_to_string('lk/act_template.html', context=context)
        html = HTML(string=html_string)
        result = html.write_pdf()

    # Создание http ответа
        response = HttpResponse(result, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="act.pdf"'
    else:
        raise Http404
    return response

@login_required
def generate_invoice_pdf(request, invoice_id):
    """Создание pdf."""
    # Данные модели
    inv = Invoice.objects.get(id=invoice_id)
    if inv.owner.username == request.user.username :
        context = {'data': inv}

    # Обработка шаблона
        html_string = render_to_string('lk/invoice_template.html', context=context)
        html = HTML(string=html_string)
        result = html.write_pdf()

    # Создание http ответа
        response = HttpResponse(result, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="invoice.pdf"'
    else:
        raise Http404
    return response




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
        orders = Order.objects.filter(department__in=[3, 4, 5]).filter(~Q(status='выполнено')).order_by('-date_added')
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
    service_name = [
        'remont', 'electric', 'santechnic', 'documents', 'cleaning', 'internet', 'lk_admin'
    ]
    if request.user.username in service_name:
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
#
# создание и редактирование счетов пользователем ответственным за заполнение документов
#
@login_required
def invoiced(request, invoice_id):
    if request.user.username == 'documents':
        invoice = Invoice.objects.get(id=invoice_id)
        if request.method != 'POST':
            # Данные не отправлялись; создается пустая форма.
            form = InvoiceForm(instance=invoice)
        else:
            # Отправлены данные POST; обработать данные.
            form = InvoiceForm(data=request.POST)
            if form.is_valid():
                new_invoice = form.save(commit=False)
                new_invoice.service = union_string(new_invoice.service, new_invoice.month, new_invoice.year)
                new_invoice.owner = invoice.owner
                new_invoice.save()
                return redirect('lk:user_invoices', invoice.owner.id)

        # Вывести пустую или недействительную форму
        context = {'id': invoice_id, 'metod': 'd', 'form': form}
    else:
        raise Http404
    return render(request, 'lk/invoice.html', context)

@login_required
def invoicee(request, invoice_id):
    if request.user.username == 'documents':
        invoice = Invoice.objects.get(id=invoice_id)
        if request.method != 'POST':
            # Данные не отправлялись; создается пустая форма.
            form = InvoiceForm(instance=invoice)
        else:
            # Отправлены данные POST; обработать данные.
            form = InvoiceForm(instance=invoice, data=request.POST)
            if form.is_valid():
                new_invoice = form.save(commit=False)
                new_invoice.service = union_string(new_invoice.service, new_invoice.month, new_invoice.year)
                new_invoice.owner = invoice.owner
                new_invoice.save()
                return redirect('lk:user_invoices', invoice.owner.id)

    # Вывести пустую или недействительную форму
        context = {'id': invoice_id, 'metod': 'e', 'form': form}
    else:
        raise Http404
    return render(request, 'lk/invoice.html', context)


@login_required
def invoice(request, user_id):
    if request.user.username == 'documents':
        user = User.objects.get(id=user_id)
        if request.method != 'POST':
         # Данные не отправлялись; создается пустая форма.
            form = InvoiceForm()
        else:
            # Отправлены данные POST; обработать данные.
            form = InvoiceForm(data=request.POST)
            if form.is_valid():
                new_invoice = form.save(commit=False)
                new_invoice.service = union_string(new_invoice.service, new_invoice.month, new_invoice.year)
                new_invoice.owner = user
                new_invoice.save()
                return redirect('lk:user_invoices', user_id)

        # Вывести пустую или недействительную форму
        context = {'id': user_id, 'metod': 'n', 'form': form}
    else:
        raise Http404
    return render(request, 'lk/invoice.html', context)

#
# создание и редактирование актов пользователем ответственным за заполнение документов
#

login_required
def actd(request, act_id):
    if request.user.username == 'documents':
        invoice = Act.objects.get(id=act_id)
        if request.method != 'POST':
            # Данные не отправлялись; создается пустая форма.
            form = ActForm(instance=invoice)
        else:
            # Отправлены данные POST; обработать данные.
            form = ActForm(data=request.POST)
            if form.is_valid():
                new_invoice = form.save(commit=False)
                new_invoice.service = union_string(new_invoice.service, new_invoice.month, new_invoice.year)
                new_invoice.owner = invoice.owner
                new_invoice.save()
                return redirect('lk:user_invoices', invoice.owner.id)

        # Вывести пустую или недействительную форму
        context = {'id': act_id, 'metod': 'd', 'form': form}
    else:
        raise Http404
    return render(request, 'lk/act_new.html', context)

@login_required
def acte(request, act_id):
    if request.user.username == 'documents':
        invoice = Act.objects.get(id=act_id)
        if request.method != 'POST':
            # Данные не отправлялись; создается пустая форма.
            form = ActForm(instance=invoice)
        else:
            # Отправлены данные POST; обработать данные.
            form = ActForm(instance=invoice, data=request.POST)
            if form.is_valid():
                new_invoice = form.save(commit=False)
                new_invoice.service = union_string(new_invoice.service, new_invoice.month, new_invoice.year)
                new_invoice.owner = invoice.owner
                new_invoice.save()
                return redirect('lk:user_invoices', invoice.owner.id)

    # Вывести пустую или недействительную форму
        context = {'id': act_id, 'metod': 'e', 'form': form}
    else:
        raise Http404
    return render(request, 'lk/act_new.html', context)


@login_required
def act_new(request, user_id):
    if request.user.username == 'documents':
        user = User.objects.get(id=user_id)
        if request.method != 'POST':
         # Данные не отправлялись; создается пустая форма.
            form = ActForm()
        else:
            # Отправлены данные POST; обработать данные.
            form = ActForm(data=request.POST)
            if form.is_valid():
                new_invoice = form.save(commit=False)
                new_invoice.service = union_string(new_invoice.service, new_invoice.month, new_invoice.year)
                new_invoice.owner = user
                new_invoice.save()
                return redirect('lk:user_invoices', user_id)

        # Вывести пустую или недействительную форму
        context = {'id': user_id, 'metod': 'n', 'form': form}
    else:
        raise Http404
    return render(request, 'lk/act_new.html', context)


@login_required()
def users(request):
    """вывод списка пользователей для пользователя DOCUMENTS"""
    service_name = [
        'remont', 'electric', 'santechnic', 'documents', 'cleaning', 'internet', 'lk_admin'
    ]
    if request.user.username == 'documents':
        users = User.objects.exclude(username__in=service_name).order_by('username')
        context = {'users_list': users}
    else:
        raise Http404
    return render(request, 'lk/users.html', context)


#
# вывод счетов и актов для пользователей-арендаторов
#

@login_required()
def user_invoices(request, user_id):
    """вывод списка счетов арендатора для пользователя DOCUMENTS """
    if request.user.username == 'documents':
        user = User.objects.get(id=user_id)
        invoices = Invoice.objects.filter(owner=user).order_by('-date_document')
        acts = Act.objects.filter(owner=user).order_by('-date_document')

        context = {'orders': invoices, 'name': user.username.upper(), 'acts': acts, 'user_id': user.id}
    else:
        raise Http404
    return render(request, 'lk/user_invoices.html', context)

@login_required
def invoices(request):
    """вывод списка счетов пользователя """
    invoices = Invoice.objects.filter(owner=request.user).order_by('-date_document')
    p = Paginator(invoices, 20)
    page = request.GET.get('page')
    orders_page = p.get_page(page)
    context = {'orders': orders_page, 'type': 'СПИСОК CЧЕТОВ'}
    return render(request, 'lk/invoices.html', context)

@login_required
def acts(request):
    acts = Act.objects.filter(owner=request.user).order_by('-date_document')
    p = Paginator(acts, 20)
    page = request.GET.get('page')
    orders_page = p.get_page(page)
    context = {'orders': orders_page, 'type': 'СПИСОК АКТОВ'}
    return render(request, 'lk/invoices.html', context)
