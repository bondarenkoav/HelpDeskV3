from django.db import models
from django_currentuser.db.models import CurrentUserField

from base.models import Client, TypeSecurity, MonthList, ServiceCompany, Status, \
    RoutesMaintenance, TypeRequest, TypeDocument, Profile


def maintenance_type_request():
    return TypeRequest.objects.get(slug='maintenance')


def maintenance_type_document_object():
    return TypeDocument.objects.get(slug='object')


class MaintenanceObject(models.Model):
    service_company = models.ForeignKey(ServiceCompany, verbose_name='Организация', on_delete=models.CASCADE)

    type_request = models.ForeignKey(TypeRequest, models.SET_NULL, verbose_name='Тип заявки',
                                     default=maintenance_type_request, null=True)
    type_document = models.ForeignKey(TypeDocument, models.SET_NULL, verbose_name='Тип документа',
                                      default=maintenance_type_document_object, null=True)
    type_security = models.ManyToManyField(TypeSecurity, verbose_name='Тип сигнализации',
                                           help_text="Выбор нескольких позиций c нажатой кнопкой Ctrl")

    object_address = models.CharField(u'Адрес объекта', max_length=300)

    client_choices = models.ForeignKey(Client, models.SET_NULL, verbose_name='Контрагент', blank=True, null=True,
                                       help_text="Обязательно для заполнения перед закрытием заявки")

    rout = models.ForeignKey(RoutesMaintenance, models.SET_NULL, verbose_name=u'Маршрут', null=True, blank=True)

    month_schedule = models.ManyToManyField(MonthList, verbose_name=u'Месяцы обслуживания',
                                           help_text=u'Выбор нескольких позиций c нажатой кнопкой Ctrl', blank=True)

    date_start = models.DateField(u'Дата начала обслуживания')
    date_end = models.DateField(u'Дата окончания обслуживания', help_text=u'Указываем последний день обслуживания',
                                null=True, blank=True)

    status = models.BooleanField(Status, u'Обслуживается', default=False, null=True)

    date_time_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    date_time_upd = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    create_user = CurrentUserField(on_update=False, related_name='mo_creator')
    update_user = CurrentUserField(on_update=True, related_name='mo_modifying')

    def __str__(self):
        return self.object_address

    class Meta:
        app_label = 'maintenance'
        verbose_name = u'Объект '
        verbose_name_plural = u'Список объектов ТО '
        permissions = (
            ('custom_add_object', u'Добавить объект'),
            ('custom_view_object', u'Просмотреть объект'),
            ('custom_change_object', u'Изменить объект'),
        )


def maintenance_type_document_request():
    return TypeDocument.objects.get(slug='request')


class MaintenanceProposal(models.Model):
    type_request = models.ForeignKey(TypeRequest, models.SET_NULL, verbose_name='Тип заявки',
                                     default=maintenance_type_request, null=True)
    type_document = models.ForeignKey(TypeDocument, models.SET_NULL, verbose_name='Тип документа',
                                      default=maintenance_type_document_object, null=True)

    object = models.ForeignKey(MaintenanceObject, verbose_name=u'Объект', on_delete=models.CASCADE)

    date_schedule = models.DateField(u'Запланировано', null=True, blank=True)
    date_work = models.DateField(u'Дата исполнения', null=True, blank=True)

    descript_work = models.TextField(u'Что сделали', blank=True)

    coworkers = models.ManyToManyField(Profile, verbose_name='Исполнитель', blank=True)

    status = models.ForeignKey(Status, models.SET_NULL, verbose_name='Статус заявки',
                               default=maintenance_type_document_request, null=True)

    date_time_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    date_time_upd = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    create_user = CurrentUserField(on_update=False, related_name='mp_creator')
    update_user = CurrentUserField(on_update=True, related_name='mp_modifying')

    def __str__(self):
        return self.object.object_address

    class Meta:
        app_label = 'maintenance'
        verbose_name = u'Заявка '
        verbose_name_plural = u'Список заявок ТО'
        permissions = (
            ('custom_add', u'Добавить заявку ТО'),
            ('custom_view', u'Просмотреть заявку ТО'),
            ('custom_change', u'Изменить заявку ТО'),
        )