from django.db import models

def file_name(instance, filename):
    import os
    from datetime import datetime

    path = 'socials/'
    ext = filename.split('.')[-1]
    filename = datetime.now().strftime("%d%m%Y%H%M%S") + '.' + ext
    return os.path.join(path, filename)

class SocialModel(models.Model):
    from integrator.apps.validators import validate_img
    from sorl.thumbnail import ImageField

    name = models.CharField('Наименование сети', max_length = 300)
    img = ImageField('Логотип', upload_to = file_name, validators = [validate_img])
    link = models.CharField('Ссылка', max_length = 300, null = True, blank = True)
    priority = models.IntegerField('Приоритет', default = 0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Социальнаые сети'
        ordering = ['priority', 'name']
