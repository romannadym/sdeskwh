# Generated by Django 3.2.13 on 2023-02-02 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0048_auto_20230202_0830'),
    ]

    operations = [
        migrations.CreateModel(
            name='SparePartNumberModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=100, verbose_name='Партномер')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spmodelpns', to='applications.sparenamemodel', verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Партномер',
                'verbose_name_plural': 'Список партномеров',
                'ordering': ['model', 'number'],
            },
        ),
    ]
