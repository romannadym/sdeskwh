# Generated by Django 3.2.13 on 2023-05-16 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0056_auto_20230512_1623'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='supportlevelmodel',
            options={'ordering': ['priority', 'name'], 'verbose_name': 'Тип поддержи', 'verbose_name_plural': 'Тип поддержи'},
        ),
    ]
