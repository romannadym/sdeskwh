from django.db import models

def file_name(instance, filename):
    import os
    from datetime import datetime

    path = 'services/'
    ext = filename.split('.')[-1]
    filename = datetime.now().strftime("%d%m%Y%H%M%S") + '.' + ext
    return os.path.join(path, filename)

class ServiceModel(models.Model):
    from integrator.apps.validators import validate_img
    from sorl.thumbnail import ImageField

    name = models.CharField('Наименование услуги', max_length = 300)
    description = models.TextField('Описание услуги')
    img = ImageField('Фотография', upload_to = file_name, validators = [validate_img])
    priority = models.IntegerField('Приоритет', default = 0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Сведения об услугах'
        ordering = ['priority', 'name']
