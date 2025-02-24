# Generated by Django 3.2.13 on 2022-09-27 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0004_auto_20220927_0741'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportLevelModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Наименование')),
                ('priority', models.IntegerField(default=0, verbose_name='Приоритет')),
            ],
            options={
                'verbose_name': 'Уровень поддержи',
                'verbose_name_plural': 'Уровни поддержи',
                'ordering': ['priority', 'name'],
            },
        ),
    ]
