# Generated by Django 3.2.13 on 2022-09-26 09:53

import applications.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import integrator.apps.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem', models.TextField(verbose_name='Описание проблемы')),
                ('fio', models.CharField(max_length=250, verbose_name='ФИО заказчика')),
                ('email', models.CharField(max_length=100, verbose_name='Электронная почта заказчика')),
                ('phone', models.CharField(max_length=18, verbose_name='Телефон заказчика')),
                ('pubdate', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appclients', to=settings.AUTH_USER_MODEL, verbose_name='Заказчик')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creators', to=settings.AUTH_USER_MODEL, verbose_name='Создано')),
                ('engineer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='engineers', to=settings.AUTH_USER_MODEL, verbose_name='Инженер')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
                'ordering': ['-pubdate'],
            },
        ),
        migrations.CreateModel(
            name='AppPriorityModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Наименование')),
                ('priority', models.IntegerField(default=0, verbose_name='Приоритет')),
            ],
            options={
                'verbose_name': 'Приоритет заявки',
                'verbose_name_plural': 'Приоритеты заявок',
                'ordering': ['priority', 'name'],
            },
        ),
        migrations.CreateModel(
            name='BrandModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Бренд оборудования',
                'verbose_name_plural': 'Бренды оборудования',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='StatusModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Наименование')),
                ('priority', models.IntegerField(default=0, verbose_name='Приоритет')),
            ],
            options={
                'verbose_name': 'Статус заявки',
                'verbose_name_plural': 'Статусы заявок',
                'ordering': ['priority', 'name'],
            },
        ),
        migrations.CreateModel(
            name='VendorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Вендор',
                'verbose_name_plural': 'Вендоры',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ModelModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Наименование')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='brands', to='applications.brandmodel', verbose_name='Бренд')),
            ],
            options={
                'verbose_name': 'Модель оборудования',
                'verbose_name_plural': 'Модели оборудования',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='EquipmentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=50, unique=True, verbose_name='Серийный номер')),
                ('pn', models.CharField(blank=True, max_length=50, null=True, verbose_name='Номер партии')),
                ('warranty', models.DateField(blank=True, null=True, verbose_name='Гарантийный период')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eqbrands', to='applications.brandmodel', verbose_name='Бренд')),
                ('client', models.ForeignKey(limit_choices_to=models.Q(('groups__name', 'Заказчик')), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eqclient', to=settings.AUTH_USER_MODEL, verbose_name='Заказчик')),
                ('model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='models', to='applications.modelmodel', verbose_name='Модель')),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vendors', to='applications.vendormodel', verbose_name='Вендор')),
            ],
            options={
                'verbose_name': 'Оборудование',
                'verbose_name_plural': 'Оборудование',
                'ordering': ['brand', 'model', 'sn'],
            },
        ),
        migrations.CreateModel(
            name='ContractModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50, verbose_name='Номер договора')),
                ('signed', models.DateField(verbose_name='Дата подписания договора')),
                ('enddate', models.DateField(verbose_name='Дата окончания договора')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contracts', to=settings.AUTH_USER_MODEL, verbose_name='Заказчик')),
            ],
            options={
                'verbose_name': 'Договор',
                'verbose_name_plural': 'Договоры',
            },
        ),
        migrations.CreateModel(
            name='AppStatusModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pubdate', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('application', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appstatuses', to='applications.applicationmodel')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='statuses', to='applications.statusmodel', verbose_name='Статус заявки')),
            ],
            options={
                'ordering': ['-pubdate'],
            },
        ),
        migrations.AddField(
            model_name='applicationmodel',
            name='equipment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipments', to='applications.equipmentmodel', verbose_name='Оборудование'),
        ),
        migrations.AddField(
            model_name='applicationmodel',
            name='priority',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='priorities', to='applications.appprioritymodel', verbose_name='Приоритет заявки'),
        ),
        migrations.AddField(
            model_name='applicationmodel',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='applications.statusmodel', verbose_name='Статус заявки'),
        ),
        migrations.CreateModel(
            name='AppHistoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'Изменение статуса'), (2, 'Изменение значения поля'), (3, 'Отправка сообщения на адрес электронной почты'), (4, 'Отправка сообщения в телеграм-канал')], verbose_name='Тип события')),
                ('text', models.CharField(max_length=300, verbose_name='Текст')),
                ('pubdate', models.DateTimeField(auto_now_add=True, verbose_name='Дата записи')),
                ('number', models.IntegerField(blank=True, null=True, verbose_name='Номер заявки')),
                ('application', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='applications.applicationmodel', verbose_name='Заявка')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'ordering': ['-pubdate'],
            },
        ),
        migrations.CreateModel(
            name='AppDocumentsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Наименование файла')),
                ('document', models.FileField(upload_to=applications.models.file_name, validators=[integrator.apps.validators.validate_format, integrator.apps.validators.validate_size], verbose_name='Файл')),
                ('application', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='applications.applicationmodel', verbose_name='Заявка')),
            ],
        ),
        migrations.CreateModel(
            name='AppCommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Комментарий')),
                ('pubdate', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='applications.applicationmodel', verbose_name='Заявка')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authors', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'ordering': ['-pubdate'],
            },
        ),
    ]
