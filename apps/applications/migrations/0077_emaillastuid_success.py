# Generated by Django 3.2.13 on 2024-05-28 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0076_appcommentmodel_email_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='emaillastuid',
            name='success',
            field=models.BooleanField(default=False, verbose_name='Попытка удачная'),
        ),
    ]
