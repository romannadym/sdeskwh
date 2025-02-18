from django.db import models

class ContactModel(models.Model):
    type = models.CharField('Контакты', max_length = 8, default = 'contacts', editable = False, primary_key = True)
    name = models.CharField('Наименование', max_length = 250)
    address = models.CharField('Адрес', max_length = 300)
    code = models.CharField('Код', max_length = 50)
    phone = models.CharField('Телефон', max_length = 18)

    def __str__(self):
        return "Контакты"

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'
