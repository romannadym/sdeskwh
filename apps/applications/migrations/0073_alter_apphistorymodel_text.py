# Generated by Django 3.2.13 on 2023-12-12 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0072_applicationmodel_changed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apphistorymodel',
            name='text',
            field=models.TextField(verbose_name='Текст'),
        ),
    ]
