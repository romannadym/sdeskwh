# Generated by Django 3.2.13 on 2024-05-28 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0075_emaillastuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='appcommentmodel',
            name='email_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата создания'),
        ),
    ]
