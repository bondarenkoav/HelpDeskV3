from django.contrib.auth.models import User
from django.db import models

from autoslug import AutoSlugField
from django.urls import reverse
from django_currentuser.db.models import CurrentUserField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Menu(MPTTModel):
    name = models.CharField('Название', max_length=50)
    slug = models.SlugField('Ключ категории')
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name="Родитель",
                            related_name='child', db_index=True,  on_delete=models.CASCADE)
    class_icon = models.CharField('Класс иконки bootstrap', max_length=30, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Ветка '
        verbose_name_plural = u'Дерево меню '

    class MPTTMeta:
        level_attr = 'mptt_level'


class City(models.Model):
    CITY_TYPE_CHOICES = [
        ('city', 'г.'),
        ('pgt', 'пгт.'),
        ('pos', 'п.'),
        ('der', 'д.'),
        ('slo', 'c.'),
    ]
    name = models.CharField(u'Населённый пункт', max_length=100)
    type = models.CharField(u'Тип',  choices=CITY_TYPE_CHOICES, max_length=100, default='city')
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.type + ' ' + self.name

    class Meta:
        verbose_name = u'Населённый пункт '
        verbose_name_plural = u'Населённые пункты '


class Post(models.Model):
    name = models.CharField(u'Должность', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Должность '
        verbose_name_plural = u'Должности '


class ServiceCompany(models.Model):
    name = models.CharField(u'Наименование', max_length=100)
    city = models.ForeignKey(City, models.SET_NULL, verbose_name=u'Город', null=True)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Сервисная компания '
        verbose_name_plural = u'Сервисные компании '


class Profile(models.Model):
    GENDER_CHOICES = [
        ('man', u'Мужской'),
        ('woman', u'Женский')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    scompany = models.ManyToManyField(ServiceCompany, related_name='scompany_select',
                                      verbose_name=u'Сервисные компании (доступные)',
                                      help_text='Выбрать сервисные компании доступные пользователю')
    scompany_default = models.ForeignKey(ServiceCompany, models.SET_NULL, related_name='scompany_default',
                                         verbose_name=u'Сервисная компания (по умолчанию)', null=True, blank=True)
    scompany_current = models.ForeignKey(ServiceCompany, models.SET_NULL, related_name='scompany_current',
                                         verbose_name=u'Сервисные компании (текущая)', null=True, blank=True)
    location = models.ForeignKey(City, models.SET_NULL, verbose_name=u'Место нахождения', null=True, blank=True)
    birthday = models.DateField(u'Дата рождения', null=True, blank=True)
    phone = models.CharField(u'Номер телефона', blank=True, max_length=10,
                             help_text=u'Вводить номер в федеральном формате, без кода страны 8 или +7')
    gender = models.CharField(u'Пол', choices=GENDER_CHOICES, max_length=50, blank=True, default='man')
    personal_data = models.BooleanField(u'Согласие на обработку персональных данных', default=False)
    executor = models.BooleanField(u'Исполнитель', default=False)
    post = models.ForeignKey(Post, models.SET_NULL, verbose_name=u'Должность', null=True)

    class Meta:
        ordering = ["user__last_name"]
        verbose_name = u'Профиль '
        verbose_name_plural = u'Профили пользователей '

    @property
    def list_scompany(self):
        return self.scompany.all()

    @property
    def current_scompany(self):
        return self.scompany_current

    @property
    def executors(self):
        list_executors = Profile.objects.\
            filter(scompany_current=self.user.profile.scompany_current, executor=True, user__is_active=True).\
            distinct().order_by('user__last_name')
        return list_executors

    @property
    def short_fio(self):
        split_fio = self.user.first_name.split(' ')
        if len(split_fio) == 2:
            return self.user.last_name + ' ' + split_fio[0] + ' ' + split_fio[1][:1] + '.'
        else:
            return self.user.last_name + ' ' + split_fio[0]

    def __str__(self):
        return self.user.last_name + ' ' + self.user.first_name


# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()


class TypeRequest(models.Model):
    name = models.CharField(u'Наименование', max_length=100)
    short_name = models.CharField(u'Аббревиатура', max_length=10)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Тип заявки '
        verbose_name_plural = u'Типы заявок '


class TypeDocument(models.Model):
    name = models.CharField(u'Наименование', max_length=100)
    shortname = models.CharField(u'Аббревиатура', max_length=10)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Тип документа '
        verbose_name_plural = u'Типы документов '


class TypeBuild(models.Model):
    name = models.CharField(u'Наименование', max_length=100)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Тип '
        verbose_name_plural = u'Типы работ '


class Client(models.Model):
    TYPE_CLIENT_CHOICES = [
        ('company', u'ЮЛ'),
        ('employer', u'ИП'),
        ('individual', u'ФЛ'),
    ]
    type = models.CharField(u'Тип',  choices=TYPE_CLIENT_CHOICES, max_length=20, default='company')
    name = models.CharField(u'Контрагент', max_length=100)
    inn = models.CharField(u'ИНН', max_length=12, blank=True)
    kpp = models.CharField(u'КПП', max_length=9, blank=True)

    date_time_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    date_time_upd = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    create_user = CurrentUserField(on_update=False, related_name='bc_creator')
    update_user = CurrentUserField(on_update=True, related_name='bc_modifying')

    def __str__(self):
        if self.type == 'company':
            return self.type + ' ' + self.name + ' (' + self.inn + '/' + self.kpp + ')'
        elif self.type == 'employer':
            return self.type + ' ' + self.name + ' (' + self.inn + ')'
        else:
            return self.type + ' ' + self.name

    @property
    def select_type(self):
        return self.get_type_display()

    def get_absolute_url(self):
        return reverse('base:upd-client', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['name']
        verbose_name = u'Контрагент '
        verbose_name_plural = u'Контрагенты '


class TypeSecurity(models.Model):
    name = models.CharField(u'Аббревиатура', max_length=10)
    descript = models.CharField(u'Полное наименование', max_length=100)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Тип системы охраны '
        verbose_name_plural = u'Системы охраны '


class MonthList(models.Model):
    name = models.CharField(u'Название месяца', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = u'Месяц '
        verbose_name_plural = u'Месяцы '


class Status(models.Model):
    name = models.CharField(u'Состояние', max_length=100)
    slug = AutoSlugField(populate_from='name')
    view_form = models.BooleanField(u'Отображать в форме')
    returned_form = models.BooleanField(u'Отображать в форме "Возврат оборудования"')
    tr_color = models.CharField(u'Цвет строки', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Статус заявки '
        verbose_name_plural = u'Статусы заявок '


class StatusTask(models.Model):
    name = models.CharField(u'Состояние', max_length=100)
    slug = AutoSlugField(populate_from='name')
    tr_color = models.CharField(u'Цвет строки', max_length=50, blank=True, null=True,
                                help_text=u'Классы: active, primary, secondary, success, '
                                          u'danger, warning, info, light, dark')
    view_list = models.BooleanField(u'Выводить в список', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Статус '
        verbose_name_plural = u'Статусы задач '


# Маршруты
class RoutesMaintenance(models.Model):
    name = models.CharField(u'Наименование маршрута', max_length=250)
    serving_company = models.ForeignKey(ServiceCompany, verbose_name=u'Сервисная компания', on_delete=models.CASCADE)

    date_time_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    date_time_upd = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    create_user = CurrentUserField(on_update=False, related_name='rm_creator')
    update_user = CurrentUserField(on_update=True, related_name='rm_modifying')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('base:upd-rout', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['name']
        verbose_name = u'Маршрут '
        verbose_name_plural = u'Маршруты ТО '


class Event(models.Model):
    name = models.CharField(u'Наименование события', max_length=200, unique=True)
    slug = AutoSlugField(populate_from='name')
    template = models.TextField(u'Шаблон', blank=True, null=True, help_text='Заполнять не обязательно')
    forfilter = models.BooleanField(u'Фильтр', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Событие '
        verbose_name_plural = u'События '


class ModelTransmitter(models.Model):
    name = models.CharField(u'Модель передатчика', max_length=50)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Передатчик'
        verbose_name_plural = 'Передатчики '