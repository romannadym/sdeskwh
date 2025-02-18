from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password = None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class OrganizationModel(models.Model):
    name = models.CharField('Наименование', max_length = 250)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['name',]
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

class OrganizationContactModel(models.Model):
    fio = models.CharField('ФИО', max_length = 300, null = False, blank = False)
    email = models.EmailField('Адрес электронной почты', blank = False, null = False)
    phone = models.CharField('Телефон', max_length = 18, null = True, blank = True)
    organization = models.ForeignKey(OrganizationModel, on_delete = models.CASCADE, related_name = 'contacts')

    def __str__(self):
        return str(self.fio)

    class Meta:
        verbose_name = 'Контактное лицо'
        verbose_name_plural = 'Информация для связи'

class User(AbstractUser):
    username = None
    email = models.EmailField(_('Адрес электронной почты'), unique = True, blank = False, null = False)
    inn = models.CharField('ИНН', max_length = 12, unique = True, null = True, blank = True)
    organization = models.ForeignKey(OrganizationModel, verbose_name = 'Организация', on_delete = models.PROTECT, related_name = 'organizations')
    address = models.CharField('Адрес', max_length = 300, null = True, blank = True)
    phone = models.CharField('Телефон', max_length = 18, null = True, blank = True)
    telegram = models.CharField('Идентификатор в телеграме', max_length = 15, null = True, blank = True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        name = ''
        if self.get_full_name():
            name = name + self.get_full_name()
        if not name:
            name = self.email
        return name.strip()

    class Meta:
        ordering = ['email',]

class UserTokenModel(models.Model):
    uid = models.CharField(max_length = 33, unique = True)
    token = models.CharField(max_length = 33)
    pubdate = models.DateTimeField(auto_now_add = True)
