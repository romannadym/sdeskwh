# Generated by Django 3.2.13 on 2023-02-02 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0047_remove_sparemodel_equipment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EquipmentStatusModel',
        ),
        migrations.DeleteModel(
            name='ProviderModel',
        ),
    ]
