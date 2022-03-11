from django.db import models

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
    date_added = models.DateTimeField(blank=True, null=True)

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
    date_added = models.DateTimeField(blank=True, null=True)

    """"кто создал?"""

    def __str__(self):
        """строковое представление модели"""
        return self.text_order