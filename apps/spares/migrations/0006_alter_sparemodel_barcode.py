# Generated by Django 3.2.13 on 2024-12-24 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spares', '0005_alter_sparepnmodel_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sparemodel',
            name='barcode',
            field=models.ImageField(blank=True, null=True, upload_to='barcodes/'),
        ),
    ]
