# Generated by Django 3.2.13 on 2023-01-18 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0043_applicationarchivemodel_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apphistorymodel',
            name='type',
            field=models.IntegerField(choices=[(1, 'Изменение статуса'), (2, 'Изменение значения поля'), (3, 'Отправка сообщения на адрес электронной почты'), (4, 'Отправка сообщения в телеграм-канал'), (5, 'Списание запчасти'), (6, 'Возврат запчасти'), (7, 'Добавление файлов')], verbose_name='Тип события'),
        ),
        migrations.AlterField(
            model_name='applicationmodel',
            name='contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appcontact', to='applications.contractcontactmodel', verbose_name='Контактное лицо'),
        ),
    ]
