# Generated by Django 3.2.13 on 2023-04-21 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0052_auto_20230420_1330'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstalledBaseModel',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('applications.equipmentmodel',),
        ),
    ]
