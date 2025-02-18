import os
from datetime import datetime

from django.db import models
from django.db.models import OuterRef, F
from django.conf import settings
from django.urls import reverse

from io import BytesIO
from django.core.files import File
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver

from bs4 import BeautifulSoup

import barcode                      # additional imports
from barcode.writer import ImageWriter

from pytils import translit

from accounts.models import OrganizationContactModel
from contracts.models import ContractEquipmentModel
from equipments.models import EquipmentModel
from spares.models import SpareModel

from integrator.apps.functions import send_email, send_telegram

def file_name(instance, filename):
    path = 'applications/' + str(instance.application.pk) + '/'
    ext = filename.split('.')[-1]
    filename = datetime.now().strftime("%d%m%Y%H%M%S") + '.' + ext
    return os.path.join(path, filename)

def file_conf(instance, filename):
    path = 'equipments/' + str(instance.equipment.pk) + '/'
    ext = filename.split('.')[-1]

    filename =  translit.slugify(filename.replace('.' + ext, ''))
    if ext:
        filename = filename + '.' + ext

    return os.path.join(path, filename)

def file_contract(instance, filename):
    path = 'contracts/' + str(instance.contract.pk) + '/'
    ext = filename.split('.')[-1]
    if ext:
        filename = filename.replace('.' + ext, '')
    filename =  translit.slugify(filename)
    if ext:
        filename = filename + '.' + ext
    return os.path.join(path, filename)

class AppPriorityModel(models.Model):
    name = models.CharField('Наименование', max_length = 300)
    priority = models.IntegerField('Приоритет', default = 0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Приоритет заявки'
        verbose_name_plural = 'Приоритеты заявок'
        ordering = ['priority', 'name']

class EquipmentConfigModel(models.Model):
    from integrator.apps.validators import validate_format, validate_size_10

    document = models.FileField('Файл', upload_to = file_conf, validators = [validate_format, validate_size_10])
    equipment = models.ForeignKey(EquipmentModel, verbose_name = 'Оборудование', on_delete = models.CASCADE, related_name = "equipconf")

    def __str__(self):
        return str(self.equipment)

    class Meta:
        verbose_name = 'Файл конфигурации'
        verbose_name_plural = 'Файлы конфигурации оборудования'


class StatusModel(models.Model):
    name = models.CharField('Наименование', max_length = 300)
    priority = models.IntegerField('Приоритет', default = 0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус заявки'
        verbose_name_plural = 'Статусы заявок'
        ordering = ['priority', 'name']

class ApplicationModel(models.Model):
    priority = models.ForeignKey(AppPriorityModel, verbose_name = 'Приоритет заявки', on_delete = models.PROTECT, related_name = "priorities", null = True)
    equipment = models.ForeignKey(ContractEquipmentModel, verbose_name = 'Оборудование', on_delete = models.PROTECT, related_name = "equipments", null = True)
    problem = models.TextField('Описание проблемы')
    contact = models.ForeignKey(OrganizationContactModel, verbose_name = 'Контактное лицо', on_delete = models.SET_NULL, related_name = "appcontact", null = True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = 'Заказчик', on_delete = models.PROTECT, related_name = "appclients", null = True)
    engineer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = 'Инженер', on_delete = models.PROTECT, related_name = "engineers", null = True, blank = True)
    pubdate = models.DateTimeField('Дата создания', auto_now_add = True)
    status = models.ForeignKey(StatusModel, verbose_name = 'Статус заявки', on_delete = models.PROTECT, null = True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = 'Создано', on_delete = models.PROTECT, related_name = "creators", null = True)
    changed = models.BooleanField('Оборудование изменено', default = False)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('app-details', kwargs = {'application_id': int(self.pk)})

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['status__priority', '-id',]

class AppDocumentsModel(models.Model):
    from integrator.apps.validators import validate_format, validate_size

    name = models.CharField('Наименование файла', max_length = 300, blank = True)
    document = models.FileField('Файл', upload_to = file_name, validators = [validate_format, validate_size])
    application = models.ForeignKey(ApplicationModel, verbose_name = 'Заявка', on_delete = models.CASCADE, related_name = "documents", null = True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.document.name
        super().save(*args, **kwargs)

class AppStatusModel(models.Model):
    status = models.ForeignKey(StatusModel, verbose_name = 'Статус заявки', on_delete = models.SET_NULL, related_name = "statuses", null = True)
    application = models.ForeignKey(ApplicationModel, on_delete = models.CASCADE, related_name = "appstatuses", null = True)
    pubdate = models.DateTimeField('Дата создания', auto_now_add = True)

    def __str__(self):
        return str(self.application)

    class Meta:
        ordering = ['-pubdate']

class AppCommentModel(models.Model):
    text = RichTextField('Комментарий', config_name = 'small')
    hide = models.BooleanField('Скрыть комментарий от клиента', default = False)
    pubdate = models.DateTimeField('Дата создания', auto_now_add = True)
    email_date = models.DateTimeField('Дата создания', null = True, blank = True)
    edited = models.BooleanField('Комментарий был отредактирован', default = False)
    application = models.ForeignKey(ApplicationModel, verbose_name = 'Заявка', on_delete = models.CASCADE, related_name = "comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = 'Автор', on_delete = models.SET_NULL, null = True, related_name = "authors")

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        method_type = 'created' if not self.pk else 'updated'
        super(AppCommentModel, self).save(*args, **kwargs)

        comments_send_messages(self, method_type)

    def delete(self, *args, **kwargs):
        super(AppCommentModel, self).delete(*args, **kwargs)

        comments_send_messages(self, 'deleted')

    class Meta:
        ordering = ['-pubdate']

def comments_send_messages(comment, method_type):
    application = ApplicationModel.objects.annotate(
        email = OrganizationContactModel.objects.filter(id = OuterRef('contact_id'))[:1].values('email'),
        engineer_email = F('engineer__email')).get(id = comment.application_id)

    to_emails = []
    history = []
    host = settings.ALLOWED_HOSTS[1]
    params = {
        'id': application.id,
        'url': 'https://' + host + application.get_absolute_url(),
        'status': comment.text.strip(),
        'type': 'comment'
    }
    text = ''

    if not comment.email_date:
        to_emails.append(application.email)
    if application.engineer:
        to_emails.append(application.engineer_email)

    title = ' комментарий к заявке № ' + str(application.id)

    if method_type == 'created':
        title = 'Добавлен' + title
        text_part = 'о добавлении'
    elif method_type == 'updated':
        title = 'Изменен' + title
        text_part = 'об изменении'
        params['type'] = 'comment_edit'
    else:
        title = 'Удален' + title
        text_part = 'об удалении'
        params['type'] = 'comment_delete'

    if to_emails:
        if send_email(params = params, title = title, send_to = to_emails):
            text = 'Отправлено сообщение ' + text_part + ' комментария "' + comment.text + '" на электронную почту'
        else:
            text = 'Не удалось отправить сообщение ' + text_part + ' комментария "' + comment.text + '" на электронную почту'
        history.append({'type': 4, 'text': text, 'application': application, 'author': comment.author})

    telegram_text = comment.text.replace('&nbsp;', ' ').replace('<ul>', '').replace('</ul>', '').replace('<ol>', '').replace('</ol>', '')
    Parse = BeautifulSoup(telegram_text, 'html.parser')

    tags = ['p', 'span', 'blockquote', 'sup', 'sub', 'li', 'a', 'div']

    all_the_tags = Parse.find_all()
    for tag in all_the_tags:
        if tag.has_attr('style'):
            del tag.attrs['style']
        if tag.name == "br":
            tag.replace_with("\n")
        if tag.name in tags:
            if tag.name == 'p' or tag.name == 'li':
                if tag.string:
                    tag.string = tag.string + "\n"
            tag.unwrap()

    telegram_text = str(Parse).strip()

    params['status'] = telegram_text
    params['author'] = comment.author.get_full_name() or comment.author.email

    if send_telegram(params = params):
        text = 'Отправлено сообщение ' + text_part + ' комментария в телеграм-канал'
    else:
        text = 'Не удалось отправить сообщение ' + text_part + ' комментария в телеграм-канал'
    history.append({'type': 4, 'text': text, 'application': application, 'author': comment.author})

    history_instance = [AppHistoryModel(**row) for row in history]
    AppHistoryModel.objects.bulk_create(history_instance)

class AppSpareModel(models.Model):
    spare = models.ForeignKey(SpareModel, verbose_name = 'Запчасть', on_delete = models.CASCADE, related_name = "appspare")
    application = models.ForeignKey(ApplicationModel, verbose_name = 'Заявка', on_delete = models.CASCADE, related_name = "appeqspare")
    pubdate = models.DateTimeField('Дата записи', auto_now_add = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = 'Пользователь', on_delete = models.SET_NULL, null = True, related_name = "appspauthors")

    def __str__(self):
        return str(self.spare)

    def save(self, *args, **kwargs):
        super(AppSpareModel, self).save(*args, **kwargs)
        spares_send_messages(self, 'created')

    def delete(self, *args, **kwargs):
        spares_send_messages(self, 'deleted')
        super(AppSpareModel, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'История ЗИП'
        verbose_name_plural = 'История ЗИП'
        ordering = ['-pubdate']

def spares_send_messages(spare, method_type):
    application = ApplicationModel.objects.annotate(engineer_email = F('engineer__email')).get(id = spare.application_id)

    spare_label = spare.spare.name + ' (S/n: ' + spare.spare.sn + ')'
    to_emails = []
    history = []
    host = settings.ALLOWED_HOSTS[1]
    params = {
        'id': application.id,
        'url': 'https://' + host + application.get_absolute_url(),
        'status': spare_label,
        'type': 'spare'
    }
    text = ''

    if method_type == 'created':
        title = 'Списание запчасти'
        text = 'Списание запчасти "' + spare_label + '"'
        text_part = 'списании'
        history.append({'type': 5, 'text': text, 'application': application, 'author': spare.author})
    else:
        params['type'] = 'return'
        title = 'Возврат запчасти'
        text = 'Возврат запчасти "' + spare_label + '"'
        text_part = 'возврате'
        history.append({'type': 6, 'text': text, 'application': application, 'author': spare.author})

    if application.engineer_email:
        if send_email(params = params, title = title, send_to = [application.engineer_email]):
            text = 'Отправлено сообщение о ' + text_part + ' запчасти "' + spare_label + '" на адрес электронной почты' + application.engineer_email
        else:
            text = 'Не удалось отправить сообщение о ' + text_part + ' запчасти "' + spare_label + '" на адрес электронной почты' + application.engineer_email
        history.append({'type': 4, 'text': text, 'application': application, 'author': spare.author})

    if send_telegram(params = params):
        text = 'Отправлено сообщение о ' + text_part + ' запчасти "' + spare_label + '" в телеграм-канал'
    else:
        text = 'Не удалось отправить сообщение о ' + text_part + ' запчасти "' + spare_label + '" в телеграм-канал'
    history.append({'type': 4, 'text': text, 'application': application, 'author': spare.author})

    history_instance = [AppHistoryModel(**row) for row in history]
    AppHistoryModel.objects.bulk_create(history_instance)


class AppHistoryModel(models.Model):
    types = (
        (1, 'Изменение статуса'),
        (2, 'Изменение значения поля'),
        (3, 'Отправка сообщения на адрес электронной почты'),
        (4, 'Отправка сообщения в телеграм-канал'),
        (5, 'Списание запчасти'),
        (6, 'Возврат запчасти'),
        (7, 'Добавление файлов'),
    )

    type = models.IntegerField('Тип события', choices = types)
    text = models.TextField('Текст')
    pubdate = models.DateTimeField('Дата записи', auto_now_add = True)
    number = models.IntegerField('Номер заявки', null = True, blank = True)
    application = models.ForeignKey(ApplicationModel, verbose_name = 'Заявка', on_delete = models.SET_NULL, null = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = 'Пользователь', on_delete = models.DO_NOTHING)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-pubdate']

class AppHistoryViewedModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = 'Пользователь', on_delete = models.CASCADE)
    history = models.ForeignKey(AppHistoryModel, verbose_name = 'Событие', on_delete = models.CASCADE, related_name = "viewed")

    class Meta:
        unique_together = ('user', 'history',)

class ApplicationArchiveModel(models.Model):
    from django.db.models import Q

    priority = models.ForeignKey(AppPriorityModel, verbose_name = 'Приоритет заявки', on_delete = models.SET_NULL, related_name = "archpriorities", null = True)
    equipment = models.ForeignKey(EquipmentModel, verbose_name = 'Оборудование', on_delete = models.SET_NULL, related_name = "archequipments", null = True)
    problem = models.TextField('Описание проблемы')
    contact = models.ForeignKey(OrganizationContactModel, verbose_name = 'Контактное лицо', on_delete = models.SET_NULL, related_name = "archcontact", null = True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = 'Заказчик', on_delete = models.SET_NULL, related_name = "archclients", null = True)
    engineer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = 'Инженер', on_delete = models.SET_NULL, related_name = "archengineers", null = True, blank = True)
    pubdate = models.DateTimeField('Дата создания')
    status = models.ForeignKey(StatusModel, verbose_name = 'Статус заявки', on_delete = models.SET_NULL, null = True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = 'Создано', on_delete = models.SET_NULL, related_name = "archcreators", null = True)
    old_id = models.IntegerField('Номер заявки')

    def __str__(self):
        return str(self.old_id)

    def get_absolute_url(self):
        return reverse('app-details', kwargs = {'application_id': int(self.pk)})

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Архив заявок'
        ordering = ['-pubdate']

class EmailLastUID(models.Model):
    uid = models.PositiveIntegerField('UID последнего прочитанного сообщения')
    success = models.BooleanField('Попытка удачная', default = False)
    pubdate = models.DateTimeField('Дата создания записи', auto_now_add = True)

    def has_add_permission(self, request):
        base_add_permission = super(EmailLastUID, self).has_add_permission(request)
        if base_add_permission:
            # if there's already an entry, do not allow adding
            count = EmailLastUID.objects.all().count()
            if count == 0:
                return True
        return False
