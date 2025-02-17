import os
from django.core.exceptions import ValidationError
from pytils import translit

def validate_img(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.png', '.jpg', '.jpeg', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Изображение должно быть в формате ".png", ".jpg", ".jpeg" или ".gif"')

def validate_format(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    if ext:
        valid_extensions = ['.txt', '.log', '.doc', '.docx', '.xls', '.xlsx', '.odt', '.rtf', '.ini', '.cfg', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.tif', '.zip', '.7z', '.rar', '.tar', '.mib']
        if not ext.lower() in valid_extensions:
            raise ValidationError('Возможна загрузка только текстовых форматов, архивов, изображений')

def validate_size(value):
     limit = 50 * 1024 * 1024

     if value.size > limit:
         raise ValidationError('Размер файла превышает 50 Мб!')
     if os.access(translit.slugify(value.name), os.X_OK):
         raise ValidationError('Загрузка исполняемых файлов запрещена!')

def validate_size_10(value):
     limit = 10 * 1024 * 1024

     if value.size > limit:
         raise ValidationError('Размер файла превышает 10 Мб!')
     if os.access(translit.slugify(value.name), os.X_OK):
         raise ValidationError('Загрузка исполняемых файлов запрещена!')

def validate_size_20(value):
     limit = 20 * 1024 * 1024

     if value.size > limit:
         raise ValidationError('Размер файла превышает 20 Мб!')
     if os.access(translit.slugify(value.name), os.X_OK):
         raise ValidationError('Загрузка исполняемых файлов запрещена!')
