# Generated by Django 3.2.13 on 2023-10-03 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_auto_20230925_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Наименование')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.articlemodel')),
            ],
            options={
                'verbose_name': 'Прикрепленный файл',
                'verbose_name_plural': 'Прикрепленные файлы',
                'ordering': ['name'],
            },
        ),
    ]
