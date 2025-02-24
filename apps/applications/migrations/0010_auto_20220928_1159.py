# Generated by Django 3.2.13 on 2022-09-28 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0009_alter_applicationarchivemodel_pubdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentStatusModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Состояние оборудования',
                'verbose_name_plural': 'Состояния оборудования',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='EquipmentTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Тип оборудования',
                'verbose_name_plural': 'Типы оборудования',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProviderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Поставщик оборудования',
                'verbose_name_plural': 'Поставщики оборудования',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='StockModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Склад',
                'verbose_name_plural': 'Склады',
                'ordering': ['name'],
            },
        ),
        migrations.RemoveField(
            model_name='equipmentmodel',
            name='pn',
        ),
        migrations.AddField(
            model_name='equipmentmodel',
            name='account',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер счета'),
        ),
        migrations.AddField(
            model_name='equipmentmodel',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='Примечание'),
        ),
        migrations.AddField(
            model_name='equipmentmodel',
            name='place',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Место на складе'),
        ),
        migrations.AddField(
            model_name='equipmentmodel',
            name='provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eqprovider', to='applications.providermodel', verbose_name='Поставщик'),
        ),
        migrations.AddField(
            model_name='equipmentmodel',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eqstatus', to='applications.equipmentstatusmodel', verbose_name='Состояние'),
        ),
        migrations.AddField(
            model_name='equipmentmodel',
            name='stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eqstock', to='applications.stockmodel', verbose_name='Склад'),
        ),
        migrations.AddField(
            model_name='equipmentmodel',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eqtypes', to='applications.equipmenttypemodel', verbose_name='Тип'),
        ),
    ]
