from django.db import models
from ckeditor.fields import RichTextField

class ArticleModel(models.Model):
    title = models.TextField('Заголовок')
    number = models.CharField('Номер статьи', max_length = 10)
    header = models.TextField('Заголовок статьи')
    summary = models.TextField('Содержание', null = True, blank = True)
    text = RichTextField('Информация', null = True, blank = True, config_name = 'default')
    attachments = models.TextField('Прикрепленные файлы', null = True, blank = True)
    products = models.TextField('Связанные продукты', null = True, blank = True)
    pubdate = models.CharField('Дата публикации', max_length = 15, null = True, blank = True)
    status = models.CharField('Статус публикации', max_length = 50, null = True, blank = True)
    version = models.CharField('Версия', max_length = 5, null = True, blank = True)
    type = models.CharField('Тип статьи', max_length = 100, null = True, blank = True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['id',]
        indexes = [
            models.Index(fields = ['id',]),
            models.Index(fields = ['number',]),
            models.Index(fields = ['title',]),
            models.Index(fields = ['header',]),
            models.Index(fields = ['summary',]),
            models.Index(fields = ['text',]),
            models.Index(fields = ['products',]),
        ]
