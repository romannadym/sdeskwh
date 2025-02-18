from django.db import models

class TypeModel(models.Model):
    name = models.CharField('Наименование', max_length = 200, unique = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип оборудования'
        verbose_name_plural = 'Типы оборудования'
        ordering = ['name']

class VendorModel(models.Model):
    name = models.CharField('Наименование', max_length = 200, unique = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вендор'
        verbose_name_plural = 'Вендоры'
        ordering = ['name']

class BrandModel(models.Model):
    name = models.CharField('Наименование', max_length = 200, unique = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренд оборудования'
        verbose_name_plural = 'Бренды оборудования'
        ordering = ['name']

class ModelModel(models.Model):
    name = models.CharField('Наименование', max_length = 300)
    brand = models.ForeignKey(BrandModel, verbose_name = 'Бренд', on_delete = models.SET_NULL, related_name = "brands", null = True)
    vendor = models.ForeignKey(VendorModel, verbose_name = 'Вендор', on_delete = models.SET_NULL, null = True, blank = True)

    def __str__(self):
        return str(self.brand) + ' ' + self.name

    class Meta:
        verbose_name = 'Модель оборудования'
        verbose_name_plural = 'Модели оборудования'
        ordering = ['name']

class EquipmentModel(models.Model):
    type = models.ForeignKey(TypeModel, verbose_name = 'Тип', on_delete = models.SET_NULL, related_name = "eqtypes", null = True, blank = True)
    brand = models.ForeignKey(BrandModel, verbose_name = 'Бренд', on_delete = models.SET_NULL, related_name = "eqbrands", null = True)
    model = models.ForeignKey(ModelModel, verbose_name = 'Модель', on_delete = models.SET_NULL, related_name = "models", null = True)
    vendor = models.ForeignKey(VendorModel, verbose_name = 'Вендор', on_delete = models.SET_NULL, related_name = "vendors", null = True, blank = True)

    def __str__(self):
        return str(self.model)

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'
        ordering = ['brand', 'model',]

class InstalledBaseModel(EquipmentModel):
    class Meta:
        proxy = True
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Инсталлированная база'
