# Generated by Django 3.2.13 on 2022-10-13 07:48

import applications.models
from django.db import migrations, models
import django.db.models.deletion
import integrator.apps.validators


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0020_auto_20221013_0735'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentConfigModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to=applications.models.file_conf, validators=[integrator.apps.validators.validate_format, integrator.apps.validators.validate_size_10], verbose_name='Файл')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipconf', to='applications.equipmentmodel', verbose_name='Оборудование')),
            ],
            options={
                'verbose_name': 'Файл конфигурации',
                'verbose_name_plural': 'Файлы конфигурации оборудования',
            },
        ),
    ]
