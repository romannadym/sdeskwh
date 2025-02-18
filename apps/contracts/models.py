from django.db import models
from django.db.models import Q
from django.conf import settings
from equipments.models import EquipmentModel

class SupportLevelModel(models.Model):
    name = models.CharField('Наименование', max_length = 300)
    priority = models.IntegerField('Приоритет', default = 0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип поддержи'
        verbose_name_plural = 'Тип поддержи'
        ordering = ['priority', 'name']

class ContractModel(models.Model):
    number = models.CharField('Номер договора', max_length = 50)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = 'Поставщик', on_delete = models.SET_NULL, null = True, related_name = "clients")
    end_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = 'Конечный пользователь', on_delete = models.SET_NULL, null = True, related_name = "endusers")
    dc_address = models.CharField('Адрес ЦОД', max_length = 250, null = True, blank = True)
    signed = models.DateField('Начало договора')
    enddate = models.DateField('Окончание договора')
    link = models.CharField('Ссылка на договор', max_length = 250, null = True, blank = True)

    def __str__(self):
        if self.client:
            return ' №' + str(self.number) + ' от ' + self.signed.strftime('%d.%m.%Y') + ' (' + str(self.client.organization) + ')'
        else:
            return 'Удалена учетная запись Ответственного лица!'

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'
        ordering = ['number', 'client__organization__name',]

class ContractEquipmentModel(models.Model):
    equipment = models.ForeignKey(EquipmentModel, verbose_name = 'Оборудование', on_delete = models.CASCADE)
    sn = models.CharField('Серийный номер', max_length = 50)
    support = models.ForeignKey(SupportLevelModel, verbose_name = 'Тип поддержки', on_delete = models.SET_NULL, null = True)
    contract = models.ForeignKey(ContractModel, verbose_name = 'Договор', on_delete = models.CASCADE, related_name = "eqcontracts")

    def __str__(self):
        return str(self.equipment)

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'
        ordering = ['equipment', 'sn',]

class ContractHistoryModel(models.Model):
    text = models.CharField('Текст', max_length = 250)
    pubdate = models.DateTimeField('Дата создания', auto_now_add = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = 'Пользователь', on_delete = models.DO_NOTHING)
    contract = models.ForeignKey(ContractModel, verbose_name = 'Договор', on_delete = models.SET_NULL, null = True)

    def __str__(self):
        return self.text + ' (' + str(self.contract) + ')'

    class Meta:
        verbose_name_plural = 'История изменений договоров'
        verbose_name = 'История изменений договора'
        ordering = ['-pubdate']
