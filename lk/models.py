from django.db import models
from django.contrib.auth.models import User

class Order (models.Model):
    """ запрос который формирует пользователь"""

    """"дата создания"""
    date_added = models.DateTimeField(auto_now_add=True)
    """"текст заявки"""
    text_order = models.TextField()
    """"отдел"""
    CLEANING = 1
    INTERNET = 2
    SANTECHNIC = 3
    ELECTRIC = 4
    REMONT = 5
    DOCUMENTS = 6

    DEPARTAMENT = (
        (CLEANING, 'Уборка'),
        (INTERNET, 'Связь, Интернет'),
        (SANTECHNIC, 'Отопление, Вода, Туалет'),
        (ELECTRIC, 'Электрика'),
        (REMONT, 'Ремонт помещения'),
        (DOCUMENTS, 'Документы, Договора, Счета'),
    )

    department = models.PositiveSmallIntegerField(
        choices=DEPARTAMENT,
        default=DOCUMENTS,
    )

    """"дата выполнения планируемая"""
    date_plane = models.DateTimeField(blank=True, null=True, default=None)

    """"статус (-не принято;-принято;-в работе;-выполнено)"""
    AWAIT = 'не принято'
    RECEIVED = 'принято'
    PROCEDED = 'в работе'
    CANCELED = 'выполнено'
    STATUS = [
        (AWAIT, 'Ожидает рассмотрения'),
        (RECEIVED, 'Рассматривается'),
        (PROCEDED, 'Принято к исполнению'),
        (CANCELED, 'Выполенно'),
    ]

    status = models.CharField(
        max_length=32,
        choices=STATUS,
        default=AWAIT,
    )

    """"дата выполнено"""
    date_relise = models.DateTimeField(blank=True, null=True, default=None)

    """"кто создал?"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """строковое представление модели"""
        return self.text_order

class Invoice (models.Model):
    """ счет пользователя"""

    """"дата документа"""
    date_document = models.DateTimeField(blank=True, null=True, default=None)

    """номер договора"""
    number_invoice = models.CharField(max_length=20)

    """номер документа"""
    number_document = models.CharField(max_length=10)

    """заказчик"""
    client = models.CharField(max_length=100)

    """ИНН"""
    inn = models.CharField(max_length=12)

    """КПП"""
    kpp = models.CharField(max_length=12, blank=True, null=True)

    """адрес"""
    adres = models.CharField(max_length=100)

    """телефон"""
    telephon = models.CharField(max_length=12, blank=True, null=True)

    """услуга"""
    service = models.CharField(max_length=150)

    """стоимость"""
    cost = models.CharField(max_length=11)

    """стоимость текстом"""
    cost_str = models.CharField(max_length=150, default=" ")

    """месяц акта"""
    JAN = 'январь'
    FEV = 'февраль'
    MAR = 'март'
    APR = 'апрель'
    MAY = 'май'
    IUN = 'июнь'
    IUL = 'июль'
    AVG = 'август'
    SEP = 'сентябрь'
    OCT = 'октябрь'
    NOV = 'ноябрь'
    DEC = 'декабрь'
    MONTH = [
        (JAN, 'январь'),
        (FEV, 'февраль'),
        (MAR, 'март'),
        (APR, 'апрель'),
        (MAY, 'май'),
        (IUN, 'июнь'),
        (IUL, 'июль'),
        (AVG, 'август'),
        (SEP, 'сентябрь'),
        (OCT, 'октябрь'),
        (NOV, 'ноябрь'),
        (DEC, 'декабрь'),
    ]

    month = models.CharField(
        max_length=9,
        choices=MONTH,
        default=JAN,
    )

    year = models.CharField(
        max_length=4,
        default=2022,
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Act (models.Model):
    """ акт пользователя"""

    """"дата документа"""
    date_document = models.DateTimeField(blank=True, null=True, default=None)

    """номер договора"""
    number_invoice = models.CharField(max_length=20)

    """номер документа"""
    number_document = models.CharField(max_length=10)

    """заказчик"""
    client = models.CharField(max_length=100)

    """банк"""
    bank = models.CharField(max_length=100, blank=True, null=True)

    """ИНН"""
    inn = models.CharField(max_length=12)

    """КПП"""
    kpp = models.CharField(max_length=12, blank=True, null=True)

    """адрес"""
    adres = models.CharField(max_length=100)

    """телефон"""
    telephon = models.CharField(max_length=12, blank=True, null=True)

    """услуга"""
    service = models.CharField(max_length=150)

    """стоимость"""
    cost = models.CharField(max_length=11)

    """стоимость текстом"""
    cost_str = models.CharField(max_length=150, default=" ")

    """месяц акта"""
    JAN = 'январь'
    FEV = 'февраль'
    MAR = 'март'
    APR = 'апрель'
    MAY = 'май'
    IUN = 'июнь'
    IUL = 'июль'
    AVG = 'август'
    SEP = 'сентябрь'
    OCT = 'октябрь'
    NOV = 'ноябрь'
    DEC = 'декабрь'
    MONTH = [
        (JAN, 'январь'),
        (FEV, 'февраль'),
        (MAR, 'март'),
        (APR, 'апрель'),
        (MAY, 'май'),
        (IUN, 'июнь'),
        (IUL, 'июль'),
        (AVG, 'август'),
        (SEP, 'сентябрь'),
        (OCT, 'октябрь'),
        (NOV, 'ноябрь'),
        (DEC, 'декабрь'),
    ]

    month = models.CharField(
        max_length=9,
        choices=MONTH,
        default=JAN,
    )

    year = models.CharField(
        max_length=4,
        default=2022,
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)