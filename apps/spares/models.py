from django.db import models
import barcode                      # additional imports
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File

class PartNumberModel(models.Model):
    number = models.CharField('Партномер', max_length = 100, unique = True)

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Партномер'
        verbose_name_plural = 'Список партномеров'
        ordering = ['number',]

class SpareModel(models.Model):
    name = models.CharField('Наименование', max_length = 250)
    sn = models.CharField('Серийный номер', max_length = 50, unique = True)
    description = models.TextField('Описание', null = True, blank = True)
    barcode = models.ImageField(upload_to = 'barcodes/', null = True, blank = True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(SpareModel, self).save(*args, **kwargs)
        if not self.barcode:
            COD128 = barcode.get_barcode_class('code128')
            rv = BytesIO()
            code = COD128(f'{self.id}', writer = ImageWriter()).write(rv)
            self.barcode.save(f'{self.id}.png', File(rv), save = False)
        return self

    class Meta:
        verbose_name = 'ЗИП'
        verbose_name_plural = 'ЗИП'
        ordering = ['name', 'sn',]

class SparePNModel(models.Model):
    number = models.ForeignKey(PartNumberModel, verbose_name = 'Партномер', on_delete = models.SET_NULL, null = True, blank = True)
    spare = models.ForeignKey(SpareModel, verbose_name = 'Запчасть', on_delete = models.CASCADE, related_name = "pnspare")

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = 'Партномер'
        verbose_name_plural = 'Партномера'
        ordering = ['number']
        unique_together = ('number', 'spare',)
