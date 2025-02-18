from django.db import models

def file_name(instance, filename):
    import os
    from datetime import datetime

    path = 'partners/'
    ext = filename.split('.')[-1]
    filename = datetime.now().strftime("%d%m%Y%H%M%S") + '.' + ext
    return os.path.join(path, filename)

class PartnerModel(models.Model):
    from integrator.apps.validators import validate_img
    from sorl.thumbnail import ImageField

    name = models.CharField('Наименование партнера', max_length = 300)
    img = ImageField('Логотип', upload_to = file_name, validators = [validate_img])
    priority = models.IntegerField('Приоритет', default = 0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Сведения о партнерах'
        ordering = ['priority', 'name']
